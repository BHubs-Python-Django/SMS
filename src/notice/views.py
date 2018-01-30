from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View

from notice.forms import NoticeForm
from notice.models import Notice


CAN_CREATE = ('teacher', 'office', 'headteaher')


def notice_list(request):
    noticeList = Notice.objects.all()
    variables = {
        'noticeList': noticeList
    }
    return render(request, 'notice/notices.html', variables)


@login_required
def add_notice(request):
    # print(request.user.member_type in CAN_CREATE)
    if request.user.member_type in CAN_CREATE:
        if request.method == 'POST':
            notice_form = NoticeForm(request.POST or None)
            if notice_form.is_valid():
                new_notice = notice_form.save(commit=False)
                new_notice.notice_from = request.user
                new_notice.save()
                return render(request, 'notice/notices.html')
        else:
            notice_form = NoticeForm()
        return render(request, 'notice/add_notice.html', {'notice_form': notice_form})
    else:
        return HttpResponse("You don't have permission")


@login_required
def edit_notice(request, id):
    # print(request.user.member_type in CAN_CREATE)
    if request.user.member_type in CAN_CREATE:
        notice = Notice.objects.get(pk=id)
        if request.method == 'POST':
            notice_form = NoticeForm(request.POST, instance=notice)
            if notice_form.is_valid():
                notice_form.save()
                return render(request, 'notice/notices.html')
        else:
            notice_form = NoticeForm()
        return render(request, 'notice/add_notice.html', {'notice_form': notice_form})
    else:
        return HttpResponse("You don't have permission")







