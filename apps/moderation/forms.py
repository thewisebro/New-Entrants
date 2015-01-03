from core import forms

REPORT_CHOICES = (
  ('offensive', "It's offensive or abusive"),
  ('insincere', "It's insincere and unproductive."),
  ('spam', "It's spam"),
  ('plagiarism', "It's plagiaristic"),
  ('default', 'It shouldn\'t be on Channel i'),
)

class ReportForm(forms.Form):
  reason = forms.ChoiceField(choices=REPORT_CHOICES,
      widget=forms.RadioSelect(),
      label="I am reporting this because")
