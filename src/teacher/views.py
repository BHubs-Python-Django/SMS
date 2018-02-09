from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
import datetime
from django.http import JsonResponse

from account import models
from . import models as teacher_model


#student dashboard access permission mixin
class TeacherPermissionMixin(object):
    def has_permissions(self, request):
        return request.user.member_type.name == 'teacher'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not self.has_permissions(request):
                return redirect('account:login')
            return super(TeacherPermissionMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return redirect('account:login')



#teacher dashboard
class Home(TeacherPermissionMixin, View):
    template_name = 'teacher/index.html'

    def get(self, request):
        return render(request, self.template_name)



#class list for attendance
class AttendanceClassList(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school=request.user.school)).all()
        count = models.Class.objects.filter(Q(school=request.user.school)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#attendance section list
class AttendanceSectionList(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-section-list.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#attendance subject list
class AttendanceSubjectList(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-subject-list.html'

    def get(self, request, classes, section):

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'subjects': subjects,
            'count': count,
            'section': section,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#attendance subject wise
class AttendanceSubjectAll(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-list.html'

    def get(self, request, classes, section, subject_id):

        now = datetime.datetime.now()

        attendance_lists = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).all()
        count = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).count()


        variables = {
            'attendance_lists': attendance_lists,
            'count': count,
            'now': now.date,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section, subject_id):
        now = datetime.datetime.now()

        attendance_lists = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).all()
        count = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).count()

        if request.POST.get('take_attendance') == 'take_attendance':
            get_object_or_404(models.Subject, pk=subject_id)

            class_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
            section_obj = models.Section.objects.get(Q(school=request.user.school) & Q(classes=class_obj) & Q(name=section))
            subject_obj = models.Subject.objects.get(Q(school=request.user.school) & Q(classes=class_obj) & Q(pk=subject_id))

            attendance = teacher_model.Attendence(school=request.user.school, classes=class_obj, section=section_obj, subject=subject_obj, teachers=request.user)
            attendance.save()

            return redirect('teacher:attendance-create', classes=classes, section=section, attendance_id=attendance.id)

        variables = {
            'attendance_lists': attendance_lists,
            'count': count,
            'now': now.date,
        }

        return render(request, self.template_name, variables)


#attendance create
class AttendanceCreate(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-create.html'

    def get(self, request, classes, section, attendance_id):
        now = datetime.datetime.now()

        students = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).order_by('student__roll').all()
        count = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).count()

        variables = {
            'now': now.date,
            'students': students,
            'count': count,
            'attendance_id': attendance_id,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::api view::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AttendanceAPIPresent(TeacherPermissionMixin, View):
    def get(self, request):

        message = False

        if request.user.is_authenticated:
            if request.GET.get('student') and request.GET.get('attendance_id'):
                stu_username = request.GET.get('student')
                attendance_id = request.GET.get('attendance_id')
                status = request.GET.get('status')

                student_obj = get_object_or_404(models.UserProfile, username=stu_username)
                attendance_obj = get_object_or_404(teacher_model.Attendence, id=attendance_id)

                #present for student when checked
                if status == 'take_present':
                    if student_obj and attendance_obj:
                        stu_exists_in_present = attendance_obj.students.filter(username=stu_username).exists()

                        if not stu_exists_in_present:

                            student_obj = models.UserProfile.objects.get(username=stu_username)

                            teacher_model.Attendence.addStudent(request.user, student_obj, attendance_id)

                            message = "present"
                        else:
                            message = "allready present count"
                    else:
                        message = 'both not found'

                #delete present for student when unchecked
                elif status == 'take_absent':
                    if student_obj and attendance_obj:
                        stu_exists_in_present = attendance_obj.students.filter(username=stu_username).exists()

                        if stu_exists_in_present:

                            student_obj = models.UserProfile.objects.get(username=stu_username)

                            teacher_model.Attendence.removeStudent(request.user, student_obj, attendance_id)

                            message = "remove present"
                        else:
                            message = "student not found in present"
                    else:
                        message = 'both not found'
        else:
            message = 'not authenticated'

        x = {
            'message': message,
        }

        return JsonResponse(x)
