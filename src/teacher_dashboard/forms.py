from django import forms
from account.models import Class, Section, School, Student
from teacher_dashboard.models import Exam, Result


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = ('Class', 'subject', 'section')


class ResultForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(ResultForm, self).__init__(*args,**kwargs)
        self.fields['classes'].queryset = Class.objects.filter(school=self.request.user.school)
        self.fields['section'].queryset = Section.objects.filter(school=self.request.user.school)
        self.fields['student'].queryset = Student.objects.filter(userprofile__school=self.request.user.school)
        self.fields['exam'].queryset = Exam.objects.filter(Class__school=self.request.user.school)

    classes = forms.ModelChoiceField(queryset=Class.objects.all())
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    student = forms.ModelChoiceField(queryset=Student.objects.all())

    class Meta:
        model = Result
        fields = ('exam', 'section', 'student')
