import os
import re

from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.conf import settings
from django.core import validators
from django.core.cache import cache
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.db.models.base import ModelBase
from django.db import models as django_models

from core import models
from api import model_constants as MC
from api.utils import int2roman
from facapp import constants as FC
from crop_image import CropImage

import redis
client = redis.Redis("localhost")
############################# Base Models #############################

class OwnerActiveManager(models.Manager):
  def get_queryset(self):
    return super(OwnerActiveManager, self).get_queryset().filter(active=True)

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

class UserPhoto(CropImage):
  unique_name = 'user_photo'
  field_name = 'photo'
  width = 150
  height = 150

  @classmethod
  def get_instance(cls, request, pk):
    if request.user.is_superuser:
      return User.objects.get(pk=pk)
    elif User.objects.get(pk=pk).in_group('Student Group'):
      if User.objects.get(pk=pk).group.admin.user == request.user:
        return User.objects.get(pk=pk)
    else:
      return request.user

  @classmethod
  def get_image_url(cls, image_field):
    if image_field:
      return image_field.url
    else:
      return settings.STATIC_URL + 'images/nucleus/default_dp.png'

  @classmethod
  def file_name(cls, image_field, fname):
    save_count = 0
    if image_field and os.path.exists(image_field.path):
      filename = save_count = image_field.name.split('/')[-1].split('.')[0]
      if len(filename.split('_')) > 1:
        try:
          save_count = int(filename.split('_')[-1]) + 1
        except Exception:
          save_count = 0
    fname = image_field.instance.username + '_' + str(save_count) + \
             '.' + fname.split('.')[-1]
    return fname


class User(AbstractUser, models.Model):
  """
  User = Channeli User
  """
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  photo = UserPhoto.ModelField(upload_to='nucleus/photo/', blank=True)
  gender = models.CharField(max_length=1, choices=MC.GENDER_CHOICES, blank=True)
  birth_date = models.DateField(blank=True, null=True,
                                verbose_name='Date of Birth')
  contact_no = models.CharField(max_length=12, blank=True,
                                verbose_name='Contact No')
  connections = models.ManyToManyField('self', through='Connection', symmetrical=False,
                                      related_name='related_to+', blank=True, null=True)
  objects = CustomUserManager()

  def __unicode__(self):
    return str(self.username) + ':' + self.name

  def in_group(self, name):
    return self.groups.filter(name=name).exists()

  def owner(self, account=None):
    if account is None:
      return Owner.objects.get_or_create(account=self, user=self)[0]
    else:
      return Owner.objects.get(account=account, user=self)

  @property
  def photo_url(self):
    if self.photo:
      return self.photo.url
    elif self.in_group('Student Group'):
      return settings.STATIC_URL + 'images/nucleus/default_group_dp.png'
    else:
      return settings.STATIC_URL + 'images/nucleus/default_dp.png'

  @property
  def short_name(self):
    return self.name.title()

  @property
  def info(self):
    if self.in_group('Student'):
      student = self.student
      string = MC.SIMPLIFIED_DEGREE[student.branch.degree]+' '+\
            (student.branch.name if len(student.branch.name)<20\
            else student.branch.code)
      if not student.passout_year:
        if student.semester > 0:
          string += ' ' + int2roman(student.year) + ' Year'
      else:
        string += ' (%s Batch)' % student.passout_year
      return string
    elif self.in_group('Faculty'):
      return dict(FC.DESIGNATION_CHOICES)[self.faculty.designation]+\
          ', ' + MC.SIMPLIFIED_DEPARTMENTS[self.faculty.department]
    elif self.in_group('Student Group'):
      return 'Student Group'
    else:
      return ''

  @property
  def html_name(self):
    if self.in_group('Student Group'):
      return mark_safe("<span class='user-span' data-username='"+self.username+\
          "' data-info='"+escape(self.info)+"' data-shortname='"+\
          escape(self.group.nickname.upper())+"' data-photo='"+\
          escape(self.photo_url)+"'>"+escape(self.short_name)+\
          "</span>")
    else:
      return mark_safe("<span class='user-span' data-username='"+self.username+\
          "' data-info='"+escape(self.info)+"' data-photo='"+\
          escape(self.photo_url)+"'>"+escape(self.short_name)+\
          "</span>")

  @property
  def role_group(self):
    if self.in_group('Student'):
      return 'Student'
    elif self.in_group('Faculty'):
      return 'Faculty'
    elif self.in_group('Student Group'):
      return 'Student Group'
    else:
      return 'Other'

  def serialize(self):
    return {
      'is_authenticated': True,
      'username': self.username,
      'name': self.name,
      'photo': self.photo_url,
      'role': self.role_group,
    }

  @property
  def delegates(self):
    return User.objects.filter(user_owners__account=self,
                                user_owners__active=True)

  @property
  def accounts(self):
    return User.objects.filter(account_owners__user=self,
                                account_owners__active=True)

  def add_connection(self, user, symmetric=True):
    connection, created = Connection.objects.get_or_create(
      from_user = self,
      to_user = user,
      status = 1
    )
    to_user__user_info = {
      'user_id': user.pk,
      'name': user.name,
      'username': user.username,
      'status': 0,
      'is_chat_on': 0,
      'photo': user.photo_url
    }
    client.hmset('user:'+str(user.pk), to_user__user_info)
    client.sadd('friends:'+str(self.pk), user.pk)
    if symmetric:
      user.add_connection(self, False)
    return connection

  def update_connection(self, user, status, symmetric=True):
    if status in (1,3):
      connection = Connection.objects.get(from_user=self, to_user=user)
      connection.status = status
      connection.save()
      if status is 1:
        client.sadd('friends:'+str(self.pk), user.pk)
      elif status is 3:
        client.srem('friends:'+str(self.pk), user.pk)
      if symmetric:
        user.update_connection(self, status, False)
      return connection
    else:
      return

  def remove_connection(self, user, symmetric=True):
    connection = Connection.objects.filter(from_user=self, to_user=user)
    connection.delete()
    client.srem('friends:'+str(self.pk), user.pk)
    if symmetric:
      user.remove_connection(self, False)
    return

  def get_friends(self):
    #return Connection.objects.filter(from_user=self, status=1)
    return self.connections.filter(
      to_people__status=1,
      to_people__from_user=self
    )

  def get_connections(self, status):
    return self.connections.filter(
      to_people__status=status,
      to_people__from_user=self
    )

class WebmailAccount(models.Model):
  webmail_id = models.CharField(max_length=20, primary_key=True)
  user = models.ForeignKey(User)


def Role(group_name):
  class UserOneToOne(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    __metaclass__ = models.base.ModelBase
    @property
    def role(self):
      return group_name

    @property
    def name(self):
      return self.user.name

    @staticmethod
    def post_save_receiver(sender, **kwargs):
      instance = kwargs['instance']
      if kwargs['created']:
        instance.user.groups.add(Group.objects.get_or_create(
                                               name=instance.role)[0])

    def __unicode__(self):
      return self.role + ':' + unicode(self.user)

    class Meta:
      abstract = True
  return UserOneToOne


########################## Student Models #############################

class Branch(models.Model):
  code = models.CharField(max_length=MC.CODE_LENGTH, primary_key=True)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  degree = models.CharField(max_length=MC.CODE_LENGTH,
                            choices=MC.DEGREE_CHOICES)
  department = models.CharField(max_length=MC.CODE_LENGTH,
                                choices=MC.DEPARTMENT_CHOICES)
  graduation = models.CharField(max_length=MC.CODE_LENGTH,
                                choices=MC.GRADUATION_CHOICES)
  no_of_semesters = models.IntegerField(null=True, blank=True)

  @property
  def duration(self):
    return self.no_of_semesters

  class Meta:
    verbose_name_plural = 'Branches'

  def __unicode__(self):
    return self.code + ':' + self.name + '(' + self.graduation + ')'

class AbstractStudentBase(django_models.Model):
  # semester field for backward compatibility, never change it's value
  # directly. Use semester_no instead.
  semester = models.CharField(max_length=MC.CODE_LENGTH,
                              choices=MC.SEMESTER_CHOICES)
  semester_no = models.IntegerField()
  branch = models.ForeignKey(Branch)
  admission_year = models.IntegerField(verbose_name='Admission Year')
  admission_semtype = models.CharField(max_length=1,
                          choices=MC.SEMESTER_TYPE_CHOICES,
                          verbose_name='Admission Semester')
  cgpa = models.CharField(max_length=6, blank=True)
  bhawan = models.CharField(max_length=MC.CODE_LENGTH,
            choices=MC.BHAWAN_CHOICES, null=True, blank=True, default=None)
  room_no = models.CharField(max_length=MC.CODE_LENGTH, blank=True,
                              verbose_name='Room No')
  passout_year = models.IntegerField(null=True, blank=True)

  class Meta:
    ordering = ['semester','branch']
    abstract = True

  def save(self, *args, **kwargs):
    # Change semester value automatically on save.
    if self.semester_no > 0 and (self.semester[:2] in ['UG','PG'] or
            self.semester[:3] == 'PHD'):
      year = (self.semester_no + 1)/2
      semtype_int = (self.semester_no + 1)%2
      self.semester = self.branch.graduation + str(year) + str(semtype_int)
    return super(AbstractStudentBase, self).save(*args, **kwargs)

  @property
  def year(self):
    return (self.semester_no+1)/2

class StudentBase(Role('Student'), AbstractStudentBase):
  class Meta:
    abstract = True

class Student(StudentBase):
  @staticmethod
  def post_save_receiver(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:
      StudentInfo.objects.get_or_create(student=instance)

class StudentUser(User, AbstractStudentBase):
  user = models.OneToOneField(User, primary_key=True, parent_link=True)
  class Meta:
    verbose_name = 'Student User (Dummy)'
    verbose_name_plural = 'Student Users (Dummy)'
    db_table = 'nucleus_student'
    managed = False

class AbstractStudentInfo(django_models.Model):
  fathers_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  verbose_name='Father\'s Name')
  fathers_occupation = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  verbose_name='Father\'s Occupation')
  fathers_office_address = models.CharField(max_length=MC.TEXT_LENGTH,
                  blank=True, verbose_name='Father\'s Office Address')
  fathers_office_phone_no = models.CharField(max_length=12, blank=True,
                  verbose_name='Father\'s Office Phone No')
  mothers_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  verbose_name='Mother\'s Name')
  permanent_address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  verbose_name='Permanent Address')
  home_contact_no = models.CharField(max_length=12, blank=True,
                  verbose_name='Home Contact No')
  state = models.CharField(max_length=3, choices=MC.STATE_CHOICES, blank=True)
  city = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  pincode = models.CharField(max_length=MC.CODE_LENGTH, blank=True)
  bank_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  verbose_name='Bank Name')
  bank_account_no = models.CharField(max_length=25, blank=True,
                  verbose_name='Bank Account No')
  passport_no = models.CharField(max_length=25, blank=True,
                  verbose_name='Passport No')
  nearest_station = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  choices=MC.RAILWAY_CHOICES, verbose_name='Nearest Station')
  local_guardian_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  verbose_name='Local Guardian\'s Name')
  local_guardian_address = models.CharField(max_length=MC.TEXT_LENGTH,
                  blank=True, verbose_name='Local Guardian\'s Address')
  local_guardian_contact_no = models.CharField(max_length=12, blank=True,
                  verbose_name='Local Guardian\'s Contact No')
  category = models.CharField(max_length=3, choices=MC.CATEGORY_CHOICES,
                  blank=True)
  nationality = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  marital_status = models.CharField(max_length=3, blank=True,
                  choices=MC.MARITAL_STATUS_CHOICES,
                  verbose_name='Marital Status')
  blood_group = models.CharField(max_length=3, choices=MC.BLOOD_GROUP_CHOICES,
                  blank=True, verbose_name='Blood Group')
  physically_disabled = models.BooleanField(default=False, blank=True,
                  verbose_name='Physically Disabled')
  fulltime = models.BooleanField(default=False, blank=True)
  resident = models.BooleanField(default=True, blank=True)
  license_no = models.CharField(max_length=MC.TEXT_LENGTH, blank=True,
                  verbose_name='License No')

  class Meta:
    abstract = True


class StudentInfo(models.Model, AbstractStudentInfo):
  student = models.OneToOneField(Student, primary_key=True)

  class Meta:
    verbose_name = 'Student Information'
    verbose_name_plural = 'Students Information'

  def __unicode__(self):
    return unicode(self.student.user)

class StudentUserInfo(StudentUser, AbstractStudentInfo):
  student = models.OneToOneField(StudentUser, primary_key=True, parent_link=True)

  class Meta:
    verbose_name = 'Student User Information (Dummy)'
    verbose_name_plural = 'Students User Information (Dummy)'
    db_table = 'nucleus_studentinfo'
    managed = False


class Course(models.Model):
  id = models.CharField(primary_key=True, max_length=60)
  code = models.CharField(max_length=50)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  credits = models.IntegerField()
  subject_area = models.CharField(max_length=MC.CODE_LENGTH)
  pre_requisites = models.ManyToManyField('Course', null=True, blank=True)
  semtype = models.CharField(max_length=1, choices=MC.SEMESTER_TYPE_CHOICES)
  year = models.IntegerField()
  seats = models.PositiveIntegerField(blank=True, null=True)

  def __unicode__(self):
    return self.code + ':' + self.name + '(' + str(self.year) +\
            ',' + self.get_semtype_display() + ')'

  def save(self, *args, **kwargs):
    self.id = self.code + ':' + str(self.year) + self.semtype
    super(Course, self).save(*args, **kwargs)


class RegisteredCourse(models.Model):
  student = models.ForeignKey(Student)
  course = models.ForeignKey(Course)
  semester_no = models.IntegerField()
  subject_area = models.CharField(max_length=MC.CODE_LENGTH, blank=True)
  credits = models.IntegerField(null=True, blank=True)
  cleared_status = models.CharField(max_length=MC.CODE_LENGTH)
  backlog_registeredcourse = models.ForeignKey('RegisteredCourse',
      related_name='next_registeredcourse', blank=True, null=True)
  grade = models.CharField(max_length=2, choices=MC.GRADE_CHOICES, default='-')

  def __unicode__(self):
    return unicode(self.student) + ':' + unicode(self.course)


class Batch(models.Model):
  name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  faculties = models.ManyToManyField('Faculty', blank=True, null=True)
  course = models.ForeignKey(Course)
  students = models.ManyToManyField(Student, blank=True, null=True)

  def __unicode__(self):
    return self.name + ':' + unicode(self.course)


########################### Other Roles  ##############################

class Faculty(Role('Faculty')):
  department = models.CharField(max_length=MC.CODE_LENGTH,
                                choices=MC.DEPARTMENT_CHOICES)
  resume = models.FileField(upload_to='facapp/resumes', null=True, blank=True)
  designation = models.CharField(max_length=MC.CODE_LENGTH,
                                  choices=FC.DESIGNATION_CHOICES)
  address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, null=True)
  employee_code = models.CharField(max_length=MC.CODE_LENGTH, blank=True)
  date_of_joining = models.CharField(max_length=MC.CODE_LENGTH, blank=True,
                                      null=True)
  home_page = models.URLField(blank=True, null=True)

  class Meta:
    verbose_name_plural = 'Faculties'


class Alumni(Role('Alumni')):
  branch = models.ForeignKey(Branch)
  admission_year = models.IntegerField()
  cgpa = models.CharField(max_length=6, blank=True)
  passout_year = models.IntegerField(null=True, blank=True)
  address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  pincode = models.CharField(max_length=MC.CODE_LENGTH, blank=True)


########################## Other useful Models ########################

class PHPSession(django_models.Model):
  session_key = models.CharField(max_length=40, primary_key=True)
  session_data = models.TextField()
  expire_date = models.DateTimeField(db_index=True)
  username = models.CharField(max_length=15)

  class Meta:
    db_table = 'nucleus_php_session'

  def __unicode__(self):
    return self.session_key


class FriendRequest(models.Model):
  from_user = models.ForeignKey(User, related_name='friendrequests_to')
  to_user = models.ForeignKey(User, related_name='friendrequests_from')
  is_declined = models.BooleanField(default=False)
  is_seen = models.BooleanField(default=False)

  class Meta:
    unique_together = ['from_user', 'to_user']

  def __unicode__(self):
    return 'From: ' + unicode(self.from_user) + ', To: ' +\
                      unicode(self.to_user)


class IntroAd(models.Model):
  name = models.CharField(max_length = MC.TEXT_LENGTH, unique=True)
  visited_users = models.ManyToManyField(User)

  def __unicode__(self):
    return 'IntroAd: ' + self.name


class UserLog(models.Model):
  user = models.ForeignKey(User)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  value = models.CharField(max_length=MC.TEXT_LENGTH)

  def __unicode__(self):
    return self.name + ':' + unicode(self.user)


class Log(models.Model):
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  value = models.CharField(max_length=MC.TEXT_LENGTH)

  def __unicode__(self):
    return self.name


class GlobalVarMeta(ModelBase):
  _cache_prefix = 'GlobalVar:'

  def __getitem__(cls, key):
    cache_key = cls._cache_prefix + key
    value = cache.get(cache_key)
    if value is None:
      obj = cls.objects.get_or_none(key=key)
      if not obj is None:
        value = obj.value
        cache.set(cache_key, value)
    if value is None:
      raise KeyError
    return value

  def __setitem__(cls, key, value):
    pair = cls.objects.get_or_create(key=key)[0]
    pair.value = value
    pair.save()
    cache_key = cls._cache_prefix + key
    cache.set(cache_key, value)

  def __delitem__(cls, key):
    pair = cls.objects.get_or_none(key=key)
    if pair:
      pair.delete()
    cache_key = cls._cache_prefix + key
    cache.set(cache_key, None)

  def has_key(cls, key):
    return cls.objects.filter(key=key).exists()

class GlobalVar(models.Model):
  key = models.CharField(max_length=MC.TEXT_LENGTH)
  value = models.CharField(max_length=MC.TEXT_LENGTH)
  __metaclass__ = GlobalVarMeta

  def __unicode__(self):
    return self.key + ':' + self.value

class Connection(models.Model):
  from_user = models.ForeignKey(User, related_name='from_people')
  to_user = models.ForeignKey(User, related_name='to_people')
  status = models.IntegerField(choices=MC.CONNECTION_STATUS)

  def __unicode__(self):
    return self.from_user.name+": "+self.to_user.name
