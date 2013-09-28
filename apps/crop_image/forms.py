from django import forms

class PhotoForm(forms.Form):
  photo = forms.ImageField()
  def clean_photo(self):
    photo = self.cleaned_data.get('photo', False)
    if photo:
      return photo
    else:
      raise ValidationError("Couldn't read uploaded image")
