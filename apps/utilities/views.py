from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from nucleus.models import StudentUserInfo, StudentInfo
from utilities.forms import ProfileForm

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def edit_profile(request):
  StudentInfo.objects.get_or_create(student=request.user.student)
  student_user_info = StudentUserInfo.objects.get(pk=request.user.pk)
  profileform = ProfileForm(instance=student_user_info)
  if request.method == 'POST':
    profileform = ProfileForm(request.POST, instance=student_user_info)
    if profileform.is_valid():
      profileform.save()
      messages.success(request, "Changes have been saved.")
  return render(request, 'utilities/edit_profile.html' ,{
    'form': profileform,
    'student_user_info': student_user_info,
  })
