from core import models
from api import model_constants as MC
from internship import constants as IC
from placement import constants as PC
from nucleus.models import Student, Branch
import os.path

class InternshipPerson(models.Model):
  """
     Details of Student
  """
  #all fields required
  student = models.OneToOneField(Student)
  status = models.CharField(max_length=3, choices=IC.INTERNSHIP_STATUS_CHOICES)
  is_placed = models.BooleanField(default=False)
  def __unicode__(self):
    return str(self.student) + str(self.status) + str(self.is_placed)

#Too many fields, most of them are not not used in the previous Placement online.
class Company(models.Model):
  """
    Contains details of companies. No deletion required.
  """
  #All fields without blank/null required
  name_of_company = models.CharField(max_length=MC.TEXT_LENGTH)
  status = models.CharField(max_length=3, choices=PC.COMPANY_STATUS_CHOICES)
  year = models.IntegerField(null=False) # Must not be null. Contains the year in which placement session starts, e.g. for 2011-12 session, this will have a value of '2011'
  address = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  open_for_disciplines = models.ManyToManyField(Branch, related_name="internship_company_related")  # Must not be null or blank, it must contain the discipline codes of at least one discipline.
  latest_date_of_joining = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  stipend = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  stipend_remark = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  cgpa_requirements = models.CharField(max_length=MC.TEXT_LENGTH, verbose_name = 'CGPA Requirements', blank=True)
  description = models.TextField(blank=True)
  designation_of_contact_person = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  email = models.EmailField(blank=True, null=True)
  fax = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  last_date_of_applying = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  name_of_contact_person = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  nature_of_duties = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  name_of_post = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  no_of_employees = models.IntegerField(null=True, blank=True)
  other_requirements = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  telephone = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  pre_internship_talk = models.BooleanField(default=False)
  shortlist_from_resumes = models.BooleanField(default=False)
  group_discussion = models.BooleanField(default=False)
  online_test = models.BooleanField(default=False)
  written_test = models.BooleanField(default=False)
  paper_based_test = models.BooleanField(default=False)
  interview_1 = models.BooleanField(verbose_name = 'Interview(In Person)', default=False)
  interview_2 = models.BooleanField(verbose_name = 'Interview(Video Conferencing)', default=False)
  interview_3 = models.BooleanField(verbose_name = 'Interview(Skype)', default=False)
  probable_date_of_arrival = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  total_vacancies = models.IntegerField(null=True, blank=True)
  training_period = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  turnover = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  website = models.CharField(max_length=MC.TEXT_LENGTH, blank=True)
  brochure = models.AutoDeleteFileField(upload_to='internship/brochures/', null=True, blank=True) 
  sector = models.CharField(max_length=2, choices=IC.COMPANY_SECTORS)
  def __unicode__(self):
    return str(self.name_of_company)

class CompanyApplicationMap(models.Model):
  """
    Mapping companies and students
  """
  #all fields required
  #### Student is mapped to InternshipPerson. This may be confusing.
  student = models.ForeignKey(InternshipPerson)
  company = models.ForeignKey(Company)
  #name of the choices list to be changed
  status = models.CharField(max_length=3, choices=IC.COMPANY_APPLICATION_STATUS)
  def __unicode__(self):
    return str(self.student) + str(self.company)


# Miscellaneous models start.
# Keep models here independent of any other model anywhere else. 
# This is because, this data shall be preserved irrespective of which placement/internship session is running.
# As you will see, there is no ForeignKey to any model (other than between themselves).
# Even personal information is stored in each table separately.
# Can get details of a company using 'company_name'and 'year' in Company model.
# Can get Person data using 'enrollment_no'.
# This was done so that these model's data is not affected, even when Person/Company model's data is deleted.

class ForumPost(models.Model):
  """
    This model maintains an entry of a new post, in any the forums.
  """
  #All fields req
  enrollment_no = models.CharField(max_length=MC.CODE_LENGTH)
  person_name = models.CharField(max_length=MC.TEXT_LENGTH)
  discipline_name = models.CharField(max_length=MC.TEXT_LENGTH)
  department_name = models.CharField(max_length=MC.TEXT_LENGTH)
  title = models.TextField()
  content = models.TextField()
  date = models.DateTimeField(auto_now_add=True)
  forum_type = models.CharField(max_length=3, choices=IC.FORUM_CHOICES)
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
    This contains all the information regarding the feedback given by a student.
  """
  # All fields req
  enrollment_no = models.CharField(max_length=MC.CODE_LENGTH)
  person_name = models.CharField(max_length=MC.TEXT_LENGTH)
  discipline_name = models.CharField(max_length=MC.TEXT_LENGTH)
  department_name = models.CharField(max_length=MC.TEXT_LENGTH)
  company_name = models.CharField(max_length=MC.TEXT_LENGTH)
  feedback = models.TextField()
  date = models.DateField()
  year = models.IntegerField(null = False) 
  def __unicode__(self):
    return str(self.company_name) + str(self.person_name) + str(self.feedback)

class Results(models.Model):
  """
    This model contains the information regarding where a student was placed and in which year.
    Current placement session information is also here.
  """
  # All fields req
  enrollment_no = models.CharField(max_length=MC.CODE_LENGTH, primary_key=True)
  person_name = models.CharField(max_length=MC.TEXT_LENGTH)
  company_name = models.CharField(max_length=MC.TEXT_LENGTH)
  discipline_name = models.CharField(max_length=MC.TEXT_LENGTH)
  department_name = models.CharField(max_length=MC.TEXT_LENGTH)
  year = models.IntegerField()
  company_id = models.IntegerField()
  def __unicode__(self):
    return str(self.person_name) + str(self.company_name)

class ResultsNew(models.Model):
  """
  This model contains the information regarding where a student was placed and in which year.
  Current placement session information is also here.
  The year field of Company specifies the year of that selection/result.
  """
  student = models.ForeignKey(Student)
  company = models.ForeignKey(Company)
  def __unicode__(self):
    return str(self.student) + str(self.company)

class Notices(models.Model):
  """
    CPT uploads notices and forms from time to time. This model keeps a record of that.
  """
  # All field req
  notice = models.AutoDeleteFileField(upload_to='internship/notices/',help_text="<span style='margin-left:70px; font-size:0.8em'>Allowed extensions : 'txt', 'doc', 'pdf', 'xml', 'xls', 'xlsx'</span>")
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

class CompanyPriority(models.Model):
  student = models.ForeignKey(Student)
  company = models.ForeignKey(Company)
  priority = models.IntegerField(default=0)
  def __unicode__(self):
    return str(self.student)+str(self.company)+str(self.priority)

