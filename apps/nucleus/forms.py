from core import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=True)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct username and"+\
                    " password. Note that both fields are case-sensitive.")

        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Your Web browser doesn't appear to"+\
                    " have cookies enabled. Cookies are required for logging in.")

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
