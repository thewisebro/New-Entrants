from django.shortcuts import render

# Create your views here.
'''def create_profile(request):
      try:
         upload_image  = Upload_Image.objects.get(user=request.user)
      except:
          pass
if request.method == 'POST':
      form = CreateProfileForm(request.POST, request.FILES)

else:
    form = CreateProfileForm(request.POST or None, instance=upload_image)
    return render_to_response('profile.html', locals(), context_instance=RequestContext(request))
'''
def tester(request):
      return HttpResponse("Hello, world. You're at lectut.")
