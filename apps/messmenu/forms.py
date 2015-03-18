from django import forms

rating_options = (
    ('5','Excellent'),
    ('4','Very good'),
    ('3','Good'),
    ('2','Average'),
    ('1','Poor'),
   )
class FeedbackForm(forms.Form):
  room_no = forms.CharField(max_length=10)
  rating = forms.ChoiceField(choices=rating_options)
