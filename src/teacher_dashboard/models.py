from django.db import models
from account.models import Student, Class, Section, UserProfile, School


class Subject(models.Model):
    subject_name = models.CharField(max_length=222)

    def __str__(self):
        return self.subject_name


class Exam(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.Class) + '--' + str(self.subject)


class Result(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    result = models.CharField(max_length=222, null=True, blank=True)
    result_GPA = models.FloatField(null=True, blank=True)

    '''def __str__(self):
        return self.student.student.roll'''




