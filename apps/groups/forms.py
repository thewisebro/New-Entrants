from django import forms
from core.forms import Form, ModelForm
from groups import models
#from api.custom_checkboxes import CustomCheckboxSelectMultiple

class GroupForm(ModelForm) :
  class Meta :
    model   = models.Group
    exclude = ('admin', 'members', 'group_admin','user','is_active')

  def __init__(self, *args, **kwargs):
    super(GroupForm, self).__init__(*args, **kwargs)
    self.fields['description'].widget.attrs.update({'class' : 'big-field'})


class GroupInfoForm(ModelForm) :
  class Meta :
    model   = models.GroupInfo
    exclude = ('subscribers','group','members','posts','photo')

  def __init__(self, *args, **kwargs):
    super(GroupInfoForm, self).__init__(*args, **kwargs)
    self.fields['mission'].widget.attrs.update({'class' : 'big-field'})

class PostAdd(forms.Form) :
  postname = forms.CharField(label="Post")

class MemberAddMultiple(forms.Form) :
  username_list = forms.CharField(widget=forms.Textarea,label="Enrollment no. list")

def MemberAddFormGen(groupinfo):
  class MemberAddForm(ModelForm):
    username = forms.CharField(label="Name/Enrollment No.")
    class Meta:
      model = models.Membership
      exclude = ('person','groupinfo')
    def __init__(self, *args, **kwargs):
      super(MemberAddForm, self).__init__(*args, **kwargs)
      self.fields['post'].queryset = groupinfo.posts
      self.fields['post'].empty_label = None
  return MemberAddForm

def MemberDeleteForm(choices):
  class MemberDelete(forms.Form):
    members = forms.ModelMultipleChoiceField(queryset=choices, widget=forms.CheckboxSelectMultiple)
  return MemberDelete

def PostDeleteForm(choices):
  class PostDelete(forms.Form):
    posts = forms.ModelMultipleChoiceField(queryset=choices, widget=forms.CheckboxSelectMultiple)
  return PostDelete

def PostChangeFormGen(groupinfo):
  class PostChangeForm(ModelForm):
    class Meta:
      model = models.Membership
      exclude = ('groupinfo')
    def __init__(self, *args, **kwargs):
      super(PostChangeForm, self).__init__(*args, **kwargs)
      self.fields['person'].queryset = groupinfo.members
      self.fields['post'].queryset = groupinfo.posts
      self.fields['post'].empty_label = None
      self.fields['person'].empty_label = None
  return PostChangeForm

def AdminChangeFormGen(groupinfo):
  class AdminChangeForm(ModelForm):
    class Meta:
      model = models.Membership
      exclude = ('post','groupinfo')
    def __init__(self, *args, **kwargs):
      super(AdminChangeForm, self).__init__(*args, **kwargs)
      self.fields['person'].queryset = groupinfo.members
  return AdminChangeForm





