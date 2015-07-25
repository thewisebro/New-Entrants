from nucleus.models import *
from placement.models import *

contact_person_lst = ContactPerson.objects.all()
new_company_names = []
for contact_person in contact_person_lst:

  old_compay = old_contact_person.companycontact
  if old_company.company_name not in new_company_names:
    new_company = CompanyContactInfo()
    new_company.name = old_company.company_name
    new_company.cluster = old_company.cluster
    new_company.status = old_company.status
    new_company.save()
    new_company_names.append(new_company.name)
  else:
    new_company = CompanyContactInfo(name=old_company_name)

  contact_person.company_contact = new_company
  campus_contact = CampusContact()
  primary_contact_new_company = ContactPerson.objects.filter(company_contact = new_company, is_primary = True)

  if primary_contact_new_contact.exists():
    contact_person.is_primary = False
    campus_contact.student = primary_contact_new_company[0].campuscontact.student
  else:
    contact_person.is_primary = True
    student = Student.objects.get(user__name=old_company.person_in_contact)
    campus_contact.student = student

  contact_person.save()

  campus_contact.last_contact = old_company.last_contact
  campus_contact.when_to_contact = old_company.when_to_contact
  campus_contact.contact_person = contact_person
  campus_contact.save()

  company_comment = CompanyContactComments()
  company_comment.comment = old_company.comments
  company_comment.campus_contact = campus_contact
  company_comment.save()
