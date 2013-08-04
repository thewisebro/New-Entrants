from django.contrib.auth.models import User, Group

from core import models
import api.model_constants as MC


class CUser(User):
  """
  CUser = Channeli User
  """
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  photo = models.ImageField(upload_to='nucleus/photo/', blank=True)
  gender = models.CharField(max_length=1, choices=MC.GENDER_CHOICES, blank=True)
  birth_date = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
  contact_no = models.CharField(max_length=12, blank=True, verbose_name='Contact No')

  class Meta:
    verbose_name = 'Channeli User'
    verbose_name_plural = 'Channeli Users'

  def __unicode__(self):
    return str(self.username) + ':' + self.name

  def save(self, *args, **kwargs):
    result = super(CUser, self).save(*args, **kwargs)
    if hasattr(self, 'role'):
      self.groups.add(Group.objects.get(name=getattr(self, 'role')))
    return result


class WebmailAccount(models.Model):
  webmail_id = models.CharField(max_length=15, primary_key=True)
  cuser = models.ForeignKey(CUser)


class Branch(models.Model):
  code = models.CharField(max_length=MC.CODE_LENGTH, primary_key=True)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  degree = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.DEGREE_CHOICES)
  department = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.DEPARTMENT_CHOICES)
  graduation = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.GRADUATION_CHOICES)
  duration = models.IntegerField() # no of semesters

  class Meta:
    verbose_name_plural = 'Branches'

  def __unicode__(self):
    return self.code + ':' + self.name + '(' + self.graduation + ')'


class Student(CUser):
  role = 'Student'
  semester = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.SEMESTER_CHOICES)
  branch = models.ForeignKey(Branch)
  admission_year = models.CharField(max_length=4)
  cgpa = models.CharField(max_length=6, blank=True)
  bhawan = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.BHAWAN_CHOICES, null=True, blank=True, default=None)
  room_no = models.CharField(max_length=MC.CODE_LENGTH, blank=True)

  class Meta:
    ordering = ['semester','branch']


class StudentInfo(Student):
  fathers_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  fathers_occupation = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  fathers_office_address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  fathers_office_phone_no = models.CharField(max_length=12, blank=True)
  mothers_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  permanent_address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  home_contact_no = models.CharField(max_length=12, blank=True)
  state = models.CharField(max_length=3, choices=MC.STATE_CHOICES, blank=True)
  city = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  pincode = models.CharField(max_length=MC.CODE_LENGTH, blank=True)
  bank_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  bank_account_no = models.CharField(max_length=25, blank=True)
  passport_no = models.CharField(max_length=25, blank=True)
  nearest_station = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, choices=MC.RAILWAY_CHOICES)
  local_guardian_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  local_guardian_address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  local_guardian_contact_no = models.CharField(max_length=12, blank=True)
  category = models.CharField(max_length=3, choices=MC.CATEGORY_CHOICES, blank=True)
  nationality = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  marital_status = models.CharField(max_length=3, choices=MC.MARITAL_STATUS_CHOICES, blank=True)
  blood_group = models.CharField(max_length=3, choices=MC.BLOOD_GROUP_CHOICES, blank=True)
  physically_disabled = models.BooleanField(default=False, blank=True)
  fulltime = models.BooleanField(default=False, blank=True)
  resident = models.BooleanField(default=True, blank=True)
  license_no = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)

  class Meta:
    verbose_name = 'Student Information'
    verbose_name_plural = 'Students Information'

class Alumni(CUser):
  role = 'Alumni'
  branch = models.ForeignKey(Branch)
  admission_year = models.CharField(max_length=4)
  cgpa = models.CharField(max_length=6, blank=True)
  passout_year = models.CharField(max_length=4, blank=True)
  address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  pincode = models.CharField(max_length=MC.CODE_LENGTH, blank=True)

