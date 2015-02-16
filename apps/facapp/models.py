from core import models
from nucleus.models import Faculty
from api import model_constants as MC
from facapp import constants as FC
from django.contrib.auth.models import User


'''
Stores the priority of section created by faculty
'''
class SectionPriority(models.Model):
  title = models.CharField(max_length=MC.TEXT_LENGTH)
  faculty = models.ForeignKey(Faculty)
  priority = models.IntegerField(default=0)
  lastModified = models.DateTimeField(auto_now=True)
  def __unicode__(self):
        return self.title + " of " + str(self.faculty.user.username)


'''
Some predefined sections
Stores detail instances of that section
'''
class Honors(models.Model):
  faculty = models.ForeignKey(Faculty)
  year = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  award = models.CharField(max_length=MC.TEXT_LENGTH)
  institute = models.CharField(max_length=MC.TEXT_LENGTH)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class ParticipationSeminar(models.Model):
  faculty = models.ForeignKey(Faculty)
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  place = models.CharField(max_length=MC.TEXT_LENGTH)
  sponsored_by = models.CharField(max_length=MC.TEXT_LENGTH)
  date = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class Membership(models.Model):
  faculty = models.ForeignKey(Faculty)
  organisation = models.CharField(max_length=MC.TEXT_LENGTH)
  position = models.CharField(max_length=MC.TEXT_LENGTH) 
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class AdministrativeBackground(models.Model):
  faculty = models.ForeignKey(Faculty)
  from_year = models.CharField(max_length=MC.CODE_LENGTH)
  to_year = models.CharField(max_length=MC.CODE_LENGTH)
  designation = models.CharField(max_length=MC.TEXT_LENGTH)
  organisation = models.CharField(max_length=MC.TEXT_LENGTH)
  at_level = models.CharField(max_length=MC.CODE_LENGTH, choices=FC.LEVEL_CHOICES)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class ProfessionalBackground(models.Model):
  faculty = models.ForeignKey(Faculty)
  from_year = models.CharField(max_length=MC.CODE_LENGTH)
  to_year = models.CharField(max_length=MC.CODE_LENGTH)
  designation = models.CharField(max_length=MC.TEXT_LENGTH)
  organisation = models.CharField(max_length=MC.TEXT_LENGTH)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class Miscellaneous(models.Model):
  faculty = models.ForeignKey(Faculty)
  particulars_of_course = models.TextField(blank=True, null=True)
  innovation_in_teaching = models.TextField(blank=True, null=True)
  instructional_tasks = models.TextField(blank=True, null=True)
  process_development = models.TextField(blank=True, null=True)
  extension_tasks = models.TextField(blank=True, null=True)
  other_work = models.TextField(blank=True, null=True)
  self_appraisal = models.TextField(blank=True, null=True) 
  comments = models.TextField(blank=True, null=True)
  separate_summary = models.TextField(blank=True, null=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class EducationalDetails(models.Model):
  faculty = models.ForeignKey(Faculty)
  subject = models.CharField(max_length=MC.TEXT_LENGTH)
  year = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  university = models.CharField(max_length=MC.TEXT_LENGTH)
  degree = models.CharField(max_length=MC.TEXT_LENGTH)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class Collaboration(models.Model):
  faculty = models.ForeignKey(Faculty) 
  topic = models.TextField()
  organisation = models.CharField(max_length=MC.TEXT_LENGTH)
  level = models.CharField(max_length=MC.CODE_LENGTH, choices=FC.DEGREE_LEVEL_CHOICES)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

  
  '''  CKEditor Models  '''
class BooksAuthored(models.Model):
  faculty = models.ForeignKey(Faculty, primary_key=True)
  books = models.TextField()
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)

class RefereedJournalPapers(models.Model):
  faculty = models.ForeignKey(Faculty, primary_key=True)
  papers = models.TextField()
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  '''  CKEditor Models over  '''

class Invitations(models.Model):
  faculty = models.ForeignKey(Faculty) 
  topic = models.TextField()
  organisation = models.CharField(max_length=MC.TEXT_LENGTH)
  category = models.CharField(max_length=MC.CODE_LENGTH, choices=FC.INVITATION_CHOICES)
  year = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class MultiplePost(models.Model):
  post = models.TextField()
  faculty = models.ForeignKey(Faculty)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class TeachingEngagement(models.Model):
  faculty = models.ForeignKey(Faculty)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  class_name = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, null=True)
  semester = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.SEMESTER_TYPE_CHOICES, default='S')
  course_code = models.CharField(max_length=MC.CODE_LENGTH)
  title = models.CharField(max_length=MC.TEXT_LENGTH)
  no_of_students = models.IntegerField()
  lecture_hours = models.IntegerField()
  practical_hours = models.IntegerField()
  tutorial_hours = models.IntegerField()
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class SponsoredResearchProjects(models.Model):
  faculty = models.ForeignKey(Faculty)
  financial_outlay = models.CharField(max_length=MC.TEXT_LENGTH)
  funding_agency = models.CharField(max_length=MC.TEXT_LENGTH)
  period = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, null=True)
  other_investigating_officer = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, null=True)
  status_of_project = models.CharField(max_length=MC.CODE_LENGTH, choices=FC.PROJECT_STATUS_CHOICES, default='O')
  type_of_project = models.CharField(max_length=MC.CODE_LENGTH, choices=FC.PROJECT_TYPE_CHOICES, default='S')
  year = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.HISTORY_YEAR_CHOICES)
  topic = models.CharField(max_length=MC.TEXT_LENGTH)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class ProjectAndThesisSupervision(models.Model):
  faculty = models.ForeignKey(Faculty)
  title_of_project = models.CharField(max_length=MC.TEXT_LENGTH)
  names_of_students = models.TextField()
  name_of_other_supervisor = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, null=True)
  description = models.TextField()
  course = models.CharField(max_length=MC.TEXT_LENGTH)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class PhdSupervised(models.Model):
  faculty = models.ForeignKey(Faculty)
  topic = models.CharField(max_length=MC.TEXT_LENGTH)
  name_of_other_supervisor = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, null=True)
  registration_year = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  status_of_phd = models.CharField(max_length=MC.CODE_LENGTH, choices=FC.PHD_STATUS_CHOICES)
  phd_type = models.CharField(max_length=MC.CODE_LENGTH, choices=MC.PHD_INFO_TIME_TYPE_CHOICES)
  scholar_name = models.CharField(max_length=MC.TEXT_LENGTH)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class ResearchScholarGroup(models.Model):
  faculty = models.ForeignKey(Faculty)
  scholar_name = models.CharField(max_length=MC.TEXT_LENGTH)
  interest = models.CharField(max_length=MC.TEXT_LENGTH)
  home_page = models.URLField(blank=True, null=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class Interests(models.Model):
  faculty = models.ForeignKey(Faculty)
  general_topic = models.CharField(max_length=MC.TEXT_LENGTH)
  research_work_topic = models.CharField(max_length=MC.TEXT_LENGTH)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class Visits(models.Model):
  faculty = models.ForeignKey(Faculty)
  purpose_of_visit = models.TextField()
  institute_visited = models.CharField(max_length=MC.TEXT_LENGTH)
  date = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class ParticipationInShorttermCourses(models.Model):
  faculty = models.ForeignKey(Faculty)
  course_name = models.CharField(max_length=MC.TEXT_LENGTH)
  sponsored_by = models.CharField(max_length=MC.TEXT_LENGTH)
  date = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class OrganisedConference(models.Model):
  # Course or Conference both
  faculty = models.ForeignKey(Faculty)
  conference_name = models.CharField(max_length=MC.TEXT_LENGTH)
  sponsored_by = models.CharField(max_length=MC.TEXT_LENGTH)
  date = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

class SpecialLecturesDelivered(models.Model):
  faculty = models.ForeignKey(Faculty)
  title = models.CharField(max_length=MC.TEXT_LENGTH)
  place = models.CharField(max_length=MC.TEXT_LENGTH)
  description = models.TextField(blank=True, null=True)
  date = models.CharField(max_length=MC.CODE_LENGTH, null=True, blank=True)
  content = models.TextField(default='')
  lastModified = models.DateTimeField(auto_now=True)
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)
  visibility = models.BooleanField(default=True)
  def __unicode__(self):
    return definition(self)

# class FacSpace(models.Model):
#   user = models.ForeignKey(User, primary_key=True)
#   space = models.IntegerField() # space alloted in GB, if row is not found,
#                                 # then default space will be 5GB
#   def __unicode__(self):
#     return str(self.user.username) + ', ' + str(self.space) + 'GB'


'''
For totally customizable section
Stores detail instances of that section
'''
class OtherSection(models.Model):
  title = models.CharField(max_length=MC.TEXT_LENGTH)
  faculty = models.ForeignKey(Faculty)
  content = models.TextField()
  priority = models.IntegerField(max_length=MC.CODE_LENGTH, choices=MC.PRIORITY_CHOICES)

def definition(self):
  if self.priority == 1:
    return "1st " + self.__class__.__name__ + " of " + str(self.faculty.user.username)
  elif self.priority == 2:
     return "2nd " + self.__class__.__name__ + " of " + str(self.faculty.user.username)
  elif self.priority == 3:
    return "3rd " + self.__class__.__name__ + " of " + str(self.faculty.user.username)
  else:
    return str(self.priority) + "th " + self.__class__.__name__ + " of " + str(self.faculty.user.username)