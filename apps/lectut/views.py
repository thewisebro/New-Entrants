from django.shortcuts import render

# Create your views here.
def create_profile(request):
      try:
          profile = Profile.objects.get(user=request.user)
      except:
          pass
if request.method == 'POST':
      form = CreateProfileForm(request.POST, request.FILES)

      if form.is_valid():
          new = form.save(commit=False)
          new.user = profile.user
          new.save()

      else:
      form = CreateProfileForm(request.POST or None, instance=profile)


  return render_to_response('profile.html', locals(), context_instance=RequestContext(request))

