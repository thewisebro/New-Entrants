import os.path

from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from core import models
from api import model_constants as MC
from placement import constants as PC
from nucleus.models import Student, Branch

# Make sure that this model has default values for each field except Student
class PlacementPerson(models.Model):
  student = models.OneToOneField(Student)
  # This field stores the category of the company in which the user is placed.
  # In case the user is placed in more than one company, it will store higher category.
  # e.g. if he is placed in 'A' and 'C' then it will store 'A'
  placed_company_category = models.CharField(max_length=3,null=True,blank=True,choices=PC.COMPANY_CATEGORY_CHOICES)
  no_of_companies_placed = models.IntegerField(default=0)
  status = models.CharField(max_length=3, choices=PC.PLACEMENT_STATUS_CHOICES, default='CLS')
  photo = models.AutoDeleteImageField(upload_to='placement/photos/',null=True,blank=True,help_text="<span style='font-size:0.9em;'>Recommended size: <b>35mm width x 45mm height</b></span>")
  is_debarred = models.BooleanField(default=False)
  def __unicode__(self):
    return str(self.status) + str(self.student) + str(self.photo)
  def clean(self):
    if self.photo :
      if self.photo.size > 500*1024 :
        raise ValidationError('Photo size can not be > 500 Kb')

# Placement related information models start.
class InternshipInformation(models.Model):
  brief_description = models.TextField(blank=True) # Can be blank
  industry = models.CharField(max_length=MC.TEXT_LENGTH) # Neither null nor blank
  title = models.CharField(max_length=200) # Neither null nor blank
  period = models.CharField(max_length=MC.TEXT_LENGTH)
  priority = models.IntegerField(choices=MC.PRIORITY_CHOICES, default=1)
  visible = models.BooleanField(default=True)
  student = models.ForeignKey(Student)
  def __unicode__(self):
    return str(self.title) + str(self.student)

class ProjectInformation(models.Model):
  brief_description = models.TextField(blank=True) # Can be blank
  industry = models.CharField(max_length=MC.TEXT_LENGTH) # Neither null nor blank
  title = models.CharField(max_length=MC.TEXT_LENGTH) # Neither null nor blank
  period = models.CharField(max_length=MC.TEXT_LENGTH)
  priority = models.IntegerField(choices=MC.PRIORITY_CHOICES, default=1)
  visible = models.BooleanField(default=True)
  student = models.ForeignKey(Student)
  def __unicode__(self):
    return str(self.title) + str(self.student)

class ExtraCurriculars(models.Model):
  # All fields req
  name_of_activity = models.CharField(max_length=MC.TEXT_LENGTH)
  year = models.CharField(max_length = MC.TEXT_LENGTH, blank=True)
  achievement = models.TextField()
  priority = models.IntegerField(choices=MC.PRIORITY_CHOICES, default=1)
  visible = models.BooleanField(default=True)
  student = models.ForeignKey(Student)
  def __unicode__(self):
    return str(self.name_of_activity) + str(self.student)

class JobExperiences(models.Model):
  # All fields req
  organisation = models.CharField(max_length=MC.TEXT_LENGTH)
  post = models.CharField(max_length=MC.TEXT_LENGTH)
  date_of_joining = models.DateField()
  date_of_leaving = models.DateField()
  brief_description = models.TextField()
  priority = models.IntegerField(choices=MC.PRIORITY_CHOICES, default=1)
  visible = models.BooleanField(default=True)
  student = models.ForeignKey(Student)
  def __unicode__(self):
    return str(self.organisation) + str(self.student)

class LanguagesKnown(models.Model):
  # All field req
  language = models.CharField(max_length=3, choices=PC.LANGUAGE_CHOICES)
  proficiency = models.CharField(max_length=3, choices=PC.LANGUAGE_PROFICIENCY_CHOICES)
  student = models.ForeignKey(Student)
  def __unicode__(self):
    return str(self.language) + ':' + str(self.student)

class ResearchPublications(models.Model):
  # All field req
  author = models.CharField(max_length=MC.TEXT_LENGTH)
  title  = models.CharField(max_length=200)
  publisher = models.CharField(max_length=MC.TEXT_LENGTH)
  year = models.IntegerField()
  priority = models.IntegerField(choices=MC.PRIORITY_CHOICES, default=1)
  visible = models.BooleanField(default=True)
  student = models.ForeignKey(Student)
  def __unicode__(self):
    return str(self.author) + ',' + str(self.title) + ':' + str(self.student)

class EducationalDetails(models.Model):
  # All field req
  student = models.ForeignKey(Student)
  year = models.IntegerField()
  sgpa = models.FloatField(default=0.0, verbose_name='SGPA')
  cgpa = models.FloatField(default=0.0, verbose_name='CGPA')
  course = models.CharField(max_length=4, choices = MC.SEMESTER_CHOICES)
  institution = models.CharField(max_length=MC.TEXT_LENGTH)
  # XXX : Keep discipline_provided just after discipline, this is the requirement of jquery
  # static/js/placement/educational_details.js
  discipline = models.CharField(max_length=MC.CODE_LENGTH)
  discipline_provided = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  def __unicode__(self):
    return str(self.course) + str(self.discipline) + str(self.student)

class PlacementInformation(models.Model):
  # All fields can be null (or blank if charfields) unless otherwise
  registration_no = models.CharField(max_length=50, blank=True) # Can be blank for people not elligible for placements
  area_of_interest = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  computer_languages = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  software_packages = models.TextField(blank=True)
  achievements = models.TextField(blank=True)
  course_taken = models.TextField(blank=True, verbose_name='Additional Courses Taken')
  reference_1 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True) # Can be blank for people not elligible for placements
  designation_1 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True) # Can be blank for people not elligible for placements
  institute_1 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True) # Can be blank for people not elligible for placements
  email_1 = models.EmailField(blank=True) # Can be blank for people not elligible for placements
  phone_1 = models.CharField(max_length=25, blank=True) # Can be blank for non-PHD only
  reference_2 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True) # Can be blank for people not elligible for placements
  designation_2 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True) # Can be blank for people not elligible for placements
  institute_2 = models.CharField(max_length=MC.TEXT_LENGTH, blank=True) # Can be blank for people not elligible for placements
  email_2 = models.EmailField(blank=True) # Can be blank for people not elligible for placements
  phone_2 = models.CharField(max_length=25, blank=True) # Can be blank for non-PHD only
  student = models.OneToOneField(Student)
  def __unicode__(self):
    return str(self.registration_no) + str(self.student)
# Placement related information models start.

class CPTMember(models.Model) :
  """
  This model stores details about the members of CPT for each placement session.
  This information is used to display contact information in a company.
  """
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  contact_no = models.CharField(max_length=15)
  year = models.IntegerField()
  email = models.EmailField()
  currently_a_member = models.BooleanField(default=True)
  def __unicode__(self) :
    return str(self.name) + ', ' + str(self.contact_no)

# Company related models start.
class Company(models.Model):
  """
    Contains details of company. No need to delete, 'year' field keeps track of which year the company came.
  """
  # All fields can be null (or blank if charfields) unless otherwise
  name = models.CharField(max_length=MC.TEXT_LENGTH) # Cannot be blank
  open_for_disciplines = models.ManyToManyField(Branch) # Must not be null or blank, it must contain the discipline codes of at least one discipline.
  year = models.IntegerField(null=False) # Must not be null. Contains the year in which placement session starts, e.g. for 2011-12 session, this will have a value of '2011'
  status = models.CharField(max_length=3, choices=PC.COMPANY_STATUS_CHOICES) # Must not be null.
  place_of_posting = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  category = models.CharField(max_length=3, choices=PC.COMPANY_CATEGORY_CHOICES) # Cannot be blank
  latest_date_of_joining = models.DateField(null=True, blank=True)
  package_ug = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'CTC(UG)')
  package_pg = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'CTC(PG)')
  package_phd = models.CharField(max_length=20, null=True, blank=True, verbose_name = 'CTC(PhD)')
  ctc_remark = models.CharField(max_length=MC.TEXT_LENGTH, null=True, blank=True, verbose_name = 'CTC Remark')
  cgpa_requirement = models.FloatField(choices=PC.CGPA_CHOICES, verbose_name = 'CGPA Requirement', null=True, blank=True)
  company_description = models.TextField(blank=True)
  contact_person = models.ForeignKey(CPTMember, null=True, blank=True)
  pre_placement_talk = models.DateField(null=True, blank=True)
  shortlist_from_resumes = models.BooleanField(default=False)
  group_discussion = models.BooleanField(default=False)
  online_test = models.BooleanField(default=False)
  written_test = models.BooleanField(default=False)
  paper_based_test = models.BooleanField(default=False)
  interview_1 = models.BooleanField(verbose_name = 'Interview(In Person)', default=False)
  interview_2 = models.BooleanField(verbose_name = 'Interview(Video Conferencing)', default=False)
  interview_3 = models.BooleanField(verbose_name = 'Interview(Skype)', default=False)
  last_date_of_applying = models.DateTimeField(null=True, blank=True)
  name_of_post = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  description_of_post = models.TextField(blank=True)
  other_requirements = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  total_vacancies_for_iitr = models.IntegerField(null=True, blank=True, verbose_name = 'Total vacancies for IITR')
  website = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  brochure = models.AutoDeleteFileField(upload_to='placement/brochures/', null=True, blank=True)
  # Sector cannot be blank. Also the sector 'VER' is reserved for the full resume for verification.
  # It decides what kind of resume will be submitted to the company.
  sector = models.CharField(max_length=3, choices=PC.COMPANY_RESUME_CHOICES)
  category_required = models.BooleanField(default=False)
  def __unicode__(self):
    return str(self.name)

class CompanyApplicationMap(models.Model):
  """
    This model stores what is the status of applications, sent by students to companies.
  """
  # All fields req
  # Only this model contains a ForeignKey to PlacementPerson
  # this is to make the coloring in applications_to_company possible
  plac_person = models.ForeignKey(PlacementPerson)
  company = models.ForeignKey(Company)
  status = models.CharField(max_length=3, choices=PC.COMPANY_APPLICATION_STATUS) # Status of the application, can be selected, not selected, etc.
  shortlisted = models.BooleanField(default = False)
  time_of_application = models.DateTimeField(auto_now=True)
  class Meta :
    unique_together = ('plac_person','company')
  def __unicode__(self):
    return str(self.company) + str(self.plac_person)

class SecondRound(models.Model):
  """
  This model stores whether second round is open for a branch or not.
  If a branch is present in this table, second round is open for that branch.
  """
  # All fields req
  branch = models.ForeignKey(Branch)
  year = models.IntegerField()
  def __unicode__(self):
    return str(self.branch) + str(self.year)

class Results(models.Model):
  """
  This model contains the information regarding where a student was placed and in which year.
  Current placement session information is also here.
  The year field of Company specifies the year of that selection/result.
  """
  student = models.ForeignKey(Student)
  company = models.ForeignKey(Company)
  def __unicode__(self):
    return str(self.student) + str(self.company)

# Company related models end.

# Miscellaneous models start.
# Keep models here independent of any other model anywhere else.
# This is because, this data shall be preserved irrespective of which placement session is running.
# As you will see, there is no ForeignKey to any model (other than between themselves).
# Even personal information is stored in each table separately.
# Can get details of a company using 'company_name'and 'year' in Company model.
# Can get Student data using 'enrollment_no'.
# This was done so that these model's data is not affected, even when Student/Company model's data is deleted.
class ForumPost(models.Model):
  """
    This model maintains an entry of a new post, in any the forums.
  """
  # All fields req
  enrollment_no = models.CharField(max_length=MC.CODE_LENGTH)
  person_name = models.CharField(max_length=MC.TEXT_LENGTH)
  discipline_name = models.CharField(max_length=MC.TEXT_LENGTH)
  department_name = models.CharField(max_length=MC.TEXT_LENGTH)
  title = models.TextField()
  content = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
  forum_type = models.CharField(max_length=3, choices=PC.FORUM_CHOICES)
  def __unicode__(self):
    return str(self.forum_type) + str(self.content) + str(self.date)

class ForumReply(models.Model):
  """
    This model stores all the replies that come to a specific post in the forum.
  """
  # All fields req
  enrollment_no = models.CharField(max_length=MC.CODE_LENGTH)
  person_name = models.CharField(max_length=MC.TEXT_LENGTH)
  post = models.ForeignKey(ForumPost)
  content = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return str(self.post) + str(self.content) + str(self.date)

class Feedback(models.Model):
  """
    This contains all the information regarding the feedback given by a student."
  """
  # All fields req
  student = models.ForeignKey(Student)
  company = models.ForeignKey(Company)
  feedback = models.TextField()
  date = models.DateField(auto_now_add=True)
  def __unicode__(self):
    return str(self.company) + str(self.student) + str(self.date)

class Notices(models.Model):
  """
    CPT uploads notices and forms from time to time. This model keeps a record of that.
  """
  # All field req
  notice = models.AutoDeleteFileField(upload_to='placement/notices/',help_text="<span style='margin-left:70px; font-size:0.8em'>Allowed extensions : 'txt', 'doc', 'pdf', 'xml', 'xls', 'xlsx'</span>")
  date_of_upload = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return str(self.notice.url) + str(self.date_of_upload)
  def filename(self):
    # convert path like placement/notices/abc__def.jpg
    # into a user friendly name like 'abc def'
    filename = os.path.basename(self.notice.name)
    filename = filename.replace('__',' ')
    filename = '.'.join(filename.split('.')[:-1])
    return filename
# Miscellaneous models start.
class CompanySlot(models.Model):
    """
      Time slots for different companies
    """
    company = models.ManyToManyField(Company)
    visibility = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null= True, blank = True)

    def __unicode__(self):
      return str(self.visibility) + str(self.start_date) + str(self.end_date)

class CompanyPlacementPriority(models.Model):
    """
      Company priority fields
    """
    student = models.ForeignKey(Student)
    slots = models.ForeignKey(CompanySlot)
    priority = models.IntegerField(null=True, blank=True)
    company = models.ForeignKey(Company)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
      return str(self.company) + str(self.priority) + str(self.slots)

class WorkshopRegistration(models.Model):
    """
      Workshop Registration Model: Used in 2015-2016 session: Workshop was optional in this year.
      This is different from Workshop Priority. Workshop priority was used in 2014-15. It was compulsory in this year.
    """
    placement_person = models.ForeignKey(PlacementPerson)
    is_registered = models.BooleanField(default=False, verbose_name = "Select to register")

    def _unicode__(self):
      return str(self.placement_person.student.user.name)+" "+str(self.registered)

class WorkshopPriority(models.Model):

  student = models.ForeignKey(Student)
  day1_priority = models.IntegerField(default=0)
  day2_priority = models.IntegerField(default=0)
  day3_priority = models.IntegerField(default=0)
  day4_priority = models.IntegerField(default=0)
  day5_priority = models.IntegerField(default=0)
  interview_application = models.BooleanField(default=False)

  def __unicode__(self):
     return str(self.student.user.name)+str(self.day1_priority)+str(self.day2_priority)+str(self.day3_priority)+str(self.day4_priority)+str(self.day5_priority)

############NEW CONTACT MANAGER MODELS

class CompanyContactInfo(models.Model):
    """
        Company info which links to a primary contact person, i.e, the HR or manager
        whom one should contact as a primary designated identity of that company.
    """
    name = models.CharField(max_length=250, unique=True, help_text="Should be unique")
    cluster = models.IntegerField(choices=PC.CLUSTER_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=40, choices=PC.STATUS_CHOICES, null=True, blank=True)

    def __unicode__(self):
        return str(self.name)+str(self.status)
class ContactPerson(models.Model):
    """
        Details of person inside the company whom campus contact would be
        contacting.
    """
    name = models.CharField(max_length=250)
    designation = models.CharField(max_length=100, null=True , blank=True)
    phone_no = models.CharField(max_length=250, null=True , blank=True)
    email = models.CharField(max_length=250 , null=True  , blank=True)
    company_contact = models.ForeignKey(CompanyContactInfo, null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.name)+' '+str(self.designation)+' '+str(self.is_primary)


class CampusContact(models.Model):
    """
        Students in the campus who would be contacting different companies contact
        F.K. to student field to get info about that student and extending info about
        the contact person like when to contact, last contact.
    """
    student = models.ForeignKey(Student, null=True, blank=True)
    last_contact = models.CharField(max_length=100, null=True, blank=True)
    when_to_contact = models.DateField(null=True, blank=True)
    contact_person =  models.OneToOneField(ContactPerson)

    def __unicode__(self):
      try:
        return str(self.student.user.name)+' '+str(self.contact_person)
      except:
        return str(self.student)+' '+str(self.contact_person)

class CompanyContactComments(models.Model):
    """
        Comments to keep updated about contacts status
    """
    comment = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    campus_contact = models.ForeignKey(CampusContact)

    def __unicode__(self):
      return str(self.campus_contact)+' '+str(self.comment)

###########COMMON CONTACT MANAGER MODELS


#############################OLD CONTACT MANAGER MODELS


class CompanyContact(models.Model):
    """
      Contains the contact of companies
    """
    company_name = models.CharField(max_length=250)
    cluster = models.IntegerField(choices=PC.CLUSTER_CHOICES, null=True, blank=True)
    contactperson = models.ForeignKey(ContactPerson, null=True, blank=True)
    status = models.CharField(max_length=40, choices=PC.STATUS_CHOICES, null=True, blank=True)
    last_contact = models.CharField(max_length=100, null=True, blank=True)
    person_in_contact = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    when_to_contact = models.DateField(null=True, blank=True)

class PlacementMgr(models.Model):
    """
      Placement manager fields.
    """
    coordi=models.ForeignKey(Student)
    company_name=models.ForeignKey(CompanyContact)

class CompanyCoordi(models.Model):
    """
      Contains information about company coordinators
    """
    student = models.ForeignKey(Student)

    def __unicode__(self):
      return self.student.user.name
