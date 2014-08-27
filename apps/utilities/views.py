from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from nucleus.models import StudentUserInfo, StudentInfo
from utilities.forms import ProfileFormPrimary, ProfileFormGuardian,\
                            ProfileFormExtra

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists())
def edit_profile(request):
  StudentInfo.objects.get_or_create(student=request.user.student)
  student_user_info = StudentUserInfo.objects.get(pk=request.user.pk)
  profileform1 = ProfileFormPrimary(instance=student_user_info)
  profileform2 = ProfileFormGuardian(instance=student_user_info)
  profileform3 = ProfileFormExtra(instance=student_user_info)
  if request.method == 'POST':
    profileform1 = ProfileFormPrimary(request.POST, instance=student_user_info)
    profileform2 = ProfileFormGuardian(request.POST, instance=student_user_info)
    profileform3 = ProfileFormExtra(request.POST, instance=student_user_info)
    if profileform1.is_valid() and profileform2.is_valid() and\
        profileform3.is_valid():
      profileform1.save()
      profileform2.save()
      profileform3.save()
      messages.success(request, "Changes have been saved.")
    else:
      messages.error(request, "Changes couldn't be saved.")
  return render(request, 'utilities/edit_profile.html' ,{
    'form1': profileform1,
    'form2': profileform2,
    'form3': profileform3,
    'student_user_info': student_user_info,
  })
