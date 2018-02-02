from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from notice.forms import NoticeForm
from notice.models import Notice

CAN_CREATE = ('teacher', 'office', 'headteaher')


# return list of all notice
def notice_list(request):
    noticeList = Notice.objects.all()
    variables = {
        'noticeList': noticeList
    }
    return render(request, 'notice/notices.html', variables)


# only listed user type can add notice
@login_required
def add_notice(request):
    if str(request.user.member_type) in CAN_CREATE:
        if request.method == 'POST':
            notice_form = NoticeForm(request.POST or None)
            if notice_form.is_valid():
                new_notice = notice_form.save(commit=False)
                new_notice.notice_from = request.user.member_type
                new_notice.author = request.user
                new_notice.school = request.user.school
                new_notice.save()
                return redirect('notice:all_notice')
        else:
            notice_form = NoticeForm()
        return render(request, 'notice/add_notice.html', {'notice_form': notice_form})
    else:
        return HttpResponse("You don't have permission")


# only listed user type can edit notice
@login_required
def edit_notice(request, id):
    if str(request.user.member_type) in CAN_CREATE:
        notice = get_object_or_404(Notice, pk=id)
        if request.method == 'POST':
            notice_form = NoticeForm(request.POST, instance=notice)
            if notice_form.is_valid():
                notice_form.save()
                return redirect('notice:all_notice')
        else:
            notice_form = NoticeForm(instance=notice)
        return render(request, 'notice/add_notice.html', {'notice_form': notice_form})
    else:
        return HttpResponse("You don't have permission")


@login_required
def delete_notice(request, id):
    if str(request.user.member_type) in CAN_CREATE:
        notice = get_object_or_404(Notice, pk=id)
        notice.delete()
        return redirect('notice:all_notice')
    else:
        return HttpResponse("You don't have permission")


