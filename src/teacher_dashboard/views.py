from django.shortcuts import render


def teacher_dashboard(request):
    return render(request, 'teacher_dashboard/teacher_dashboard.html')
