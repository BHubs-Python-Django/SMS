from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View

from administration.views import AdminPermission
from office.views import check_user
from teacher_dashboard.forms import ExamForm, ResultForm
from teacher_dashboard.models import Result


def teacher_dashboard(request):
    return render(request, 'teacher_dashboard/teacher_dashboard.html')


def take_exam(request):
    exam_form = ExamForm(request.POST)
    if exam_form.is_valid():
        exam_form.save()
    else:
        exam_form = ExamForm()

    context = {
        'title': 'Take Exam',
        'form': exam_form,
    }
    return render(request, 'teacher_dashboard/take_exam.html', context)


''''@login_required
def publish_result(request):
    result_form = ResultForm(request.POST)
    if result_form.is_valid():
        result_form.save()
    else:
        result_form = ResultForm()

    context = {
        'title': 'Publish Result',
        'form': result_form,
    }
    return render(request, 'teacher_dashboard/take_exam.html', context)'''


class PublishResult(AdminPermission, View):
    template_name = 'teacher_dashboard/take_exam.html'

    def get(self, request):
        result_form = ResultForm(request.POST, request=request)
        variables = {
            'form': result_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        result_form = ResultForm(request.POST)
        if result_form.is_valid():
            result_form.save()

        variables = {
            'form': result_form,
        }

        return render(request, self.template_name, variables)


def results(request):
    results = Result.objects.all()
    return render(request, 'teacher_dashboard/results.html', {'results': results})

