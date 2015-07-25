import re

from django.db import models
from nucleus.models import User
from django import forms

from api import model_constants as MC
from nucleus.models import Branch, Student


def ContactValidator(value):
  if not str(value).isdigit():
    raise ValidationError("Contact number should contain only numerical digits.")


def isdecimal(s):
  return re.match('^[0-9][0-9]*[.]?[0-9]*$',s) != None


class StudentApplicationInfo(models.Model):
  user = models.OneToOneField(User, primary_key=True, verbose_name='Enrollment No', null=False, blank=False)
  name_in_english = models.CharField(max_length=MC.TEXT_LENGTH)
  name_in_hindi = models.CharField(max_length=MC.TEXT_LENGTH)
  branch = models.ForeignKey(Branch)
  fathers_name = models.CharField(max_length=MC.TEXT_LENGTH)
  mothers_name = models.CharField(max_length=MC.TEXT_LENGTH)
  state_of_domicile = models.CharField(max_length=3, choices=MC.STATE_CHOICES + (('FOR', 'Foreign'),), blank=True)
  nationality = models.CharField(max_length=3, choices=MC.NATIONALITY_CHOICES)
  religion = models.CharField(max_length=MC.TEXT_LENGTH)
  minority = models.CharField(max_length=3, choices=MC.MINORITY_CHOICES)           # No for no minority, other specifies the minority.
  birth_date = models.DateField()
  marital_status = models.CharField(max_length=3, choices=MC.MARITAL_STATUS_CHOICES, blank=True)
  category = models.CharField(max_length=3, choices=MC.CATEGORY_CHOICES, blank=True, null=True)
  gender = models.CharField(max_length=1, choices=MC.GENDER_CHOICES)
  physically_disabled = models.CharField(max_length=3, choices=MC.HANDICAPPED_CHOICES)    # NO for not handicapped
  email_id = models.EmailField()
  personal_contact_no = models.CharField(max_length=12, validators=[ContactValidator])
  personal_contact_no_alternative = models.CharField(max_length=12, blank=True ,validators=[ContactValidator])
  bhawan = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.BHAWAN_CHOICES)
  room_no = models.CharField(max_length=MC.CODE_LENGTH)
  local_guardian_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  local_guardian_address = models.TextField(blank=True)
  local_guardian_email_id = models.EmailField(blank=True)
  local_guardian_contact_no_home    = models.CharField(max_length=12, blank=True)
  local_guardian_contact_no_work    = models.CharField(max_length=12, blank=True)
  local_guardian_contact_no_mobile  = models.CharField(max_length=12, blank=True)
  parent_or_guardian_address = models.TextField()
  parent_or_guardian_email_id = models.EmailField(blank=True)
  parent_or_guardian_contact_no_home   = models.CharField(max_length=12)
  parent_or_guardian_contact_no_work   = models.CharField(max_length=12)
  parent_or_guardian_contact_no_mobile = models.CharField(max_length=12)
  parent_or_guardian_state = models.CharField(max_length=3, choices=MC.STATE_CHOICES)
  parent_or_guardian_country = models.CharField(max_length=3, choices=MC.COUNTRY_CHOICES)
  permanent_address = models.TextField(blank=False)
  permanent_address_email_id = models.EmailField(blank=True)
  state = models.CharField(max_length=3, choices=MC.STATE_CHOICES)
  city = models.CharField(max_length=MC.TEXT_LENGTH)
  country = models.CharField(max_length=3, choices=MC.COUNTRY_CHOICES)
  pincode = models.CharField(max_length=MC.CODE_LENGTH)
  home_contact_no = models.CharField(max_length=12, validators=[ContactValidator])
  jee_rank = models.CharField(max_length=6, blank=True)
  jee_category_rank = models.CharField(max_length=6, blank=True)

# For PHD Students

  fellowship_category = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  phd_status = models.CharField(max_length=1, blank=True, choices=MC.PHD_STATUS_CHOICES)
  title_of_thesis = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  editable_fields = ['marital_status', 'local_guardian_name','local_guardian_address','local_guardian_contact_no_home','local_guardian_contact_no_work','local_guardian_contact_no_mobile','local_guardian_email_id', 'permanent_address_email_id','bhawan','room_no','personal_contact_no','personal_contact_no_alternative']
  not_required_fields = ['state_of_domicile', 'marital_status', 'personal_contact_no_alternative', 'local_guardian_name','local_guardian_address','local_guardian_contact_no_home','local_guardian_contact_no_work','local_guardian_contact_no_mobile','local_guardian_email_id', 'parent_or_guardian_email_id', 'permanent_address_email_id', 'title_of_thesis']

  def __unicode__(self):
    return self.user.username + "::" + self.name_in_english


class AcademicQualification(models.Model):
  student = models.ForeignKey(StudentApplicationInfo)
  exam_passed = models.CharField(max_length=MC.TEXT_LENGTH)
  institute_name = models.CharField(max_length=MC.TEXT_LENGTH)
  year_of_passing = models.IntegerField()
  division = models.CharField(max_length=3)
  max_marks = models.DecimalField(max_digits=7, decimal_places=3)
  marks_obtained = models.DecimalField(max_digits=7, decimal_places=3)
  percentage = models.DecimalField(max_digits=7, decimal_places=4)

  def __unicode__(self):
    return self.student.user.username + "::" + self.exam_passed


class GateJamCatScore(models.Model):
  student = models.ForeignKey(StudentApplicationInfo)
  exam_type = models.CharField(max_length=4, choices=MC.GATE_JAM_CAT_CHOICES)
  reigon_no = models.CharField(max_length=MC.TEXT_LENGTH)
  score = models.CharField(max_length=12)       # Not Sure
  specialization = models.CharField(max_length=MC.TEXT_LENGTH)
  validity_upto = models.CharField(max_length='20')

  def __unicode__(self):
    return self.student.user.username + "::" + self.exam_type



class StudentApplicationForm(forms.ModelForm):

  def __init__(self, person, *args, **kwargs):
    if StudentApplicationInfo.objects.filter(user=person.user).exists():
      kwargs['instance'] = StudentApplicationInfo.objects.filter(user=person.user)[0]
    super(StudentApplicationForm, self).__init__(*args, **kwargs)
    self.user = person.user
    if StudentApplicationInfo.objects.filter(user=person.user).exists():
      for field in self.fields.keys():
        if field not in StudentApplicationInfo.editable_fields:
          self.fields[field].widget.attrs['readonly'] = True
    else:
      self.fields['name_in_english'].initial = person.name
      self.fields['branch'].initial = person.branch
      for field in ['fathers_name', 'mothers_name', 'nationality', 'marital_status', 'category', 'local_guardian_name',
                    'local_guardian_address', 'permanent_address', 'state', 'city', 'pincode', 'home_contact_no']:
        self.fields[field].initial = person.studentinfo.__getattribute__(field)
      self.fields['name_in_english'].widget.attrs['readonly']=True


      self.fields['jee_rank'].required = True
      self.fields['jee_category_rank'].required = True         # For UG students


    if person.semester.find('PHD') < 0 :
      del self.fields['fellowship_category']
      del self.fields['phd_status']
      del self.fields['title_of_thesis']
    else:
      self.fields['fellowship_category'].required = True
      self.fields['phd_status'].required = True
      self.fields['title_of_thesis'].required = False
      self.fields['jee_rank'].required = False
      self.fields['jee_category_rank'].required = False

    if person.semester.find('PG') < 0 :
      self.fields['category'].required = True
    else:
      self.fields['jee_rank'].required = False
      self.fields['jee_category_rank'].required = False


  def clean(self):
    person = Student.objects.get(user=self.user)
    cleaned_data = super(StudentApplicationForm, self).clean()
    print cleaned_data
    if StudentApplicationInfo.objects.filter(user=person.user).exists():
      s = StudentApplicationInfo.objects.filter(user=person.user)[0]
      for field in self.fields.keys():
        if field not in StudentApplicationInfo.editable_fields:
          cleaned_data[field] = s.__getattribute__(field)
          
    
    if cleaned_data['name_in_english'] != person.name:
      raise forms.ValidationError('Name should be correct')

    if not StudentApplicationInfo.objects.filter(user=person.user).exists():
      cleaned_data['acad'] = []
      for i in range(1,7):
        ans1 = True
        ans2 = True
        tdata = []
        for x in ['exam', 'board', 'year', 'division', 'max', 'marks', 'percentage']:
          if self.data[x + str(i)] == '':
            ans1=False
          else:
            ans2 = False
            tdata.append(self.data[x + str(i)])

        if ans1:
          cleaned_data['acad'].append(tdata)
          print tdata

        tstr = ''
        if i==1:
          tstr = 'st'
        elif i==2:
          tstr = 'nd'
        elif i==3:
          tstr = 'rd'
        else:
          tstr = 'th'


        if not ans1 and not ans2:
          raise forms.ValidationError('Fill every detail in the '+str(i)+tstr+' Academic Qualification entry.')
        
        if ans2:
          continue

        if not self.data['year'+str(i)].isdigit():
          raise forms.ValidationError('Year should be a number in the '+str(i)+tstr+' Academic Qualification entry.')

        if not isdecimal(self.data['max'+str(i)]) or not isdecimal(self.data['marks'+str(i)]) or not isdecimal(self.data['percentage'+str(i)]):
          raise forms.ValidationError('Marks/Percentage should be a decimal in the '+str(i)+tstr+' Academic Qualification entry.')

      if len(cleaned_data['acad']) == 0:
        raise forms.ValidationError('Academic Qualification should not be empty.')





      cleaned_data['exam'] = []
      if self.data['exam_type']:
        if self.data['reg']=='' or self.data['score']=='' or self.data['spec']=='' or self.data['date']=='':
          print '6'
          raise forms.ValidationError(self.data['exam_type']+' data should be filled correctly.')
        
        cleaned_data['exam'].append(self.data['exam_type'])
        for x in ['reg','score','spec','date']:
          print '7'
          cleaned_data['exam'].append(self.data[x])

    print 'yo'
    return cleaned_data


  def save(self):
    exist = False
    if StudentApplicationInfo.objects.filter(user=self.user).exists():
      exist = True

    print 'here'
    map(lambda x: x.delete(), StudentApplicationInfo.objects.filter(user=self.user))
    obj = super(StudentApplicationForm,self).save(commit=False)
    obj.user = self.user
    obj.save()
    print 'saved'
    
    if not exist:
      for acad_data in self.cleaned_data['acad']:
        AcademicQualification.objects.create(student=obj,
           exam_passed = acad_data[0],
           institute_name = acad_data[1],
           year_of_passing = acad_data[2],
           division = acad_data[3],
           max_marks = acad_data[4],
           marks_obtained = acad_data[5],
           percentage = acad_data[6] )




      if len(self.cleaned_data['exam']):
        GateJamCatScore.objects.create(student=obj,
            exam_type = self.cleaned_data['exam'][0],
            reigon_no = self.cleaned_data['exam'][1],
            score = self.cleaned_data['exam'][2],
            specialization = self.cleaned_data['exam'][3],
            validity_upto = self.cleaned_data['exam'][4] )


  class Meta:
    model = StudentApplicationInfo
    exclude = ['user']
