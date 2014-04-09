from django.db import models
from nucleus.models import Student, Branch, Faculty
from api import model_constants as MC
from regol import constants as RC

class CourseDetails(models.Model):
  course_code = models.CharField(max_length=MC.CODE_LENGTH, primary_key=True)
  course_name = models.CharField(max_length=MC.TEXT_LENGTH)
  credits = models.IntegerField()
  pre_requisite = models.ForeignKey('self', null=True, blank=True)#Self ForeignKey
  group_code = models.CharField(max_length=MC.TEXT_LENGTH, default='-1') # List of group codes for a course.
  seats = models.IntegerField(null=True, blank=True)
  def __unicode__(self):
    return self.course_code + ':' + self.course_name

class CourseStructureMap(models.Model):
  course_code = models.CharField(max_length=MC.CODE_LENGTH) # Must be course_code in CourseDetails or user defined group code in CourseDetails for IE/DE.
  semester = models.CharField(max_length=MC.TEXT_LENGTH, choices=MC.SEMESTER_CHOICES)
  branch = models.ForeignKey(Branch)
  subject_area = models.CharField(max_length=MC.CODE_LENGTH, choices = RC.SUBJECT_AREA_CHOICES)
  group_status = models.BooleanField(default=False) # It checks for IE/DE.
  def __unicode__(self):
    return self.course_code + ':' + self.branch.code

class InstituteElectivesNotEligibleMap(models.Model):
  branch = models.ForeignKey(Branch)
  course_details = models.ForeignKey(CourseDetails)
  def __unicode__(self):
    return str(self.course_details)

class RegolStudent(models.Model):
  student = models.OneToOneField(Student)
  reg_type = models.CharField(max_length=MC.TEXT_LENGTH, choices=RC.REGISTRATION_TYPE_CHOICES,default='RFN')
  semreg_finalized = models.BooleanField(default = False)
  def __unicode__(self):
    return str(self.student)

class AssignedFaculty(models.Model):
  branch = models.ForeignKey(Branch)
  year = models.IntegerField()
  faculty = models.ForeignKey(Faculty)


class PhdInfo(models.Model):
  student = models.OneToOneField(Student)
  internal_guide_1 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  internal_guide_2 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  initial_regn_date = models.DateField(blank=True, null=True)
  external_guide = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  thesis_topic = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  thesis_abstract = models.TextField(blank=True)
  time_type = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, choices=MC.PHD_INFO_TIME_TYPE_CHOICES)
  scheme = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, choices=MC.PHD_INFO_SCHEME_CHOICES)
  mhrd_asst_comp_date = models.DateField(blank=True, null=True)
  def __unicode__(self):
    return self.student

class InstituteElectives(models.Model):
  student = models.ForeignKey(Student)
  semester = models.CharField(max_length=MC.TEXT_LENGTH, choices=MC.SEMESTER_CHOICES)
  choice_list = models.CharField(max_length=MC.TEXT_LENGTH)
  tentative_elective = models.CharField(max_length=MC.TEXT_LENGTH)
  group_code = models.CharField(max_length=MC.CODE_LENGTH)
  def __unicode__(self):
    return str(self.student) + ':' + self.choice_list

class RegisteredCourses(models.Model):
  student = models.ForeignKey(Student)
  course_details = models.ForeignKey(CourseDetails)
  credits = models.IntegerField()
  registered_date = models.DateField()
  semester = models.CharField(max_length=MC.TEXT_LENGTH, choices=MC.SEMESTER_CHOICES)
  subject_area = models.CharField(max_length=MC.CODE_LENGTH)
  cleared_status = models.CharField(max_length=MC.CODE_LENGTH, choices=RC.REGISTERED_COURSES_CLEARED_STATUS, default='NXT') # TODO set default based on choices
  grade = models.CharField(max_length=2, choices=MC.GRADE_CHOICES, default='-')
  group_code = models.CharField(max_length = MC.CODE_LENGTH, default='-1')


class JeeEntrants(models.Model):
  enrollment_no = models.CharField(max_length=MC.CODE_LENGTH, unique=True, primary_key=True)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  branch = models.ForeignKey(Branch)
  admission_year = models.CharField(max_length=4)
  gender = models.CharField(max_length=1, choices=MC.GENDER_CHOICES)
  fathers_name = models.CharField(max_length=MC.TEXT_LENGTH,verbose_name = "Father's Name")
  birth_date = models.DateField(verbose_name = 'Date of Birth')
  rank = models.PositiveIntegerField()
  nationality = models.CharField(max_length = MC.TEXT_LENGTH)
  category = models.CharField(max_length=3, choices=MC.CATEGORY_CHOICES)
  registration_no = models.CharField(max_length = MC.TEXT_LENGTH, null = True, blank = True)
  category_rank = models.PositiveIntegerField(null=True, blank = True)
  received_fee = models.BooleanField(default = False)
  registered = models.BooleanField(default = False)
  class Meta:
    ordering = ['branch','enrollment_no']
    verbose_name = 'JEE Entrants'
    verbose_name_plural = 'JEE Entrants'
  def __unicode__(self):
    return self.enrollment_no + ':' + self.name

