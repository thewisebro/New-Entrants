from django.contrib.auth.models import AbstractUser, UserManager, Group

from core import models

from api import model_constants as MC
from facapp import constants as FC


class OwnerActiveManager(models.Manager):
  def get_query_set(self):
    return super(OwnerActiveManager, self).get_query_set().filter(active=True)

class Owner(models.Model):
  account = models.ForeignKey('User', related_name='account_owners')
  user = models.ForeignKey('User', related_name='user_owners')
  active = models.BooleanField(default=True)
  objects = OwnerActiveManager()
  all_objects = models.Manager()

  class Meta:
    unique_together = ['account', 'user']

  def __unicode__(self):
    return 'account: ' + str(self.account.username) + ' -> ' +\
           'user: ' + str(self.user.username)

  @classmethod
  def add(cls, account, user):
    owner, created = cls.all_objects.get_or_create(account=account, user=user)
    if not created:
      owner.active = True
      owner.save()

  @classmethod
  def remove(cls, account, user):
    owner = cls.all_objects.get_or_none(account=account, user=user)
    if owner:
      owner.active = False
      owner.save()


class CustomUserManager(UserManager, models.Manager):
  pass

class User(AbstractUser):
  """
  User = Channeli User
  """
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  photo = models.ImageField(upload_to='nucleus/photo/', blank=True)
  gender = models.CharField(max_length=1, choices=MC.GENDER_CHOICES, blank=True)
  birth_date = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
  contact_no = models.CharField(max_length=12, blank=True, verbose_name='Contact No')
  connections = models.ManyToManyField('self', blank=True, null=True)
  objects = CustomUserManager()

  def __unicode__(self):
    return str(self.username) + ':' + self.name

  def save(self, *args, **kwargs):
    result = super(User, self).save(*args, **kwargs)
    if hasattr(self, 'role'):
      self.groups.add(Group.objects.get(name=getattr(self, 'role')))
    return result

  def in_group(self, name):
    return self.groups.filter(name=name).exists()

  def owner(self, account=None):
    if account is None:
      return Owner.objects.get_or_create(account=self, user=self)[0]
    else:
      return Owner.objects.get(account=account, user=self)

  @property
  def delegates(self):
    return User.objects.filter(user_owners__account=self, user_owners__active=True)

  @property
  def accounts(self):
    return User.objects.filter(account_owners__user=self, account_owners__active=True)


class WebmailAccount(models.Model):
  webmail_id = models.CharField(max_length=15, primary_key=True)
  user = models.ForeignKey(User)


class Branch(models.Model):
  code = models.CharField(max_length=MC.CODE_LENGTH, primary_key=True)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  degree = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.DEGREE_CHOICES)
  department = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.DEPARTMENT_CHOICES)
  graduation = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.GRADUATION_CHOICES)
  duration = models.IntegerField(null=True, blank=True) # no of semesters

  class Meta:
    verbose_name_plural = 'Branches'

  def __unicode__(self):
    return self.code + ':' + self.name + '(' + self.graduation + ')'


class Student(User):
  role = 'Student'
  semester = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.SEMESTER_CHOICES)
  branch = models.ForeignKey(Branch)
  admission_year = models.CharField(max_length=4)
  cgpa = models.CharField(max_length=6, blank=True)
  bhawan = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.BHAWAN_CHOICES, null=True, blank=True, default=None)
  room_no = models.CharField(max_length=MC.CODE_LENGTH, blank=True)
  courses = models.ManyToManyField('Course', through='RegisteredCourse', blank=True, null=True)

  class Meta:
    ordering = ['semester','branch']


class StudentInfo(models.Model):
  student = models.OneToOneField(Student, primary_key=True)
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


class Faculty(User):
  role = 'Faculty'
  department = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.DEPARTMENT_CHOICES)
  resume = models.FileField(upload_to='facapp/resumes', null=True, blank=True)
  designation = models.CharField(max_length=MC.CODE_LENGTH, choices=FC.DESIGNATION_CHOICES)
  address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, null=True)
  employee_code = models.CharField(max_length=MC.CODE_LENGTH, blank=True)
  date_of_joining = models.CharField(max_length=MC.CODE_LENGTH, blank=True, null=True)
  home_page = models.URLField(blank=True, null=True)

  class Meta:
    verbose_name_plural = 'Faculties'


class Alumni(User):
  role = 'Alumni'
  branch = models.ForeignKey(Branch)
  admission_year = models.CharField(max_length=4)
  cgpa = models.CharField(max_length=6, blank=True)
  passout_year = models.CharField(max_length=4, blank=True)
  address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  pincode = models.CharField(max_length=MC.CODE_LENGTH, blank=True)


class Course(models.Model):
  code = models.CharField(max_length=MC.CODE_LENGTH, primary_key=True)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  pre_requisites = models.ManyToManyField('Course', null=True, blank=True)

  def __unicode__(self):
    return self.course_code + ':' + self.course_name


class RegisteredCourse(models.Model):
  student = models.ForeignKey(Student)
  course = models.ForeignKey(Course)
  credits = models.IntegerField()
  registered_date = models.DateField(blank=True, null=True)
  semester = models.CharField(max_length=MC.TEXT_LENGTH, choices=MC.SEMESTER_CHOICES)
  subject_area = models.CharField(max_length=MC.CODE_LENGTH)
  cleared_status = models.CharField(max_length=MC.CODE_LENGTH, default='NXT') # TODO set default based on choices
  grade = models.CharField(max_length=2, choices=MC.GRADE_CHOICES, default='-')

  def __unicode__(self):
    return unicode(self.student) + ':' + unicode(self.course)


class Class(models.Model):
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  faculties = models.ManyToManyField(Faculty, blank=True, null=True)
  semester_type = models.CharField(max_length=1, choices=MC.SEMESTER_TYPE_CHOICES)
  year = models.CharField(max_length=4)
  course = models.ForeignKey(Course)
  students = models.ManyToManyField(Student, blank=True, null=True)

  def __unicode__(self):
    return self.name + ':' + unicode(self.course)
