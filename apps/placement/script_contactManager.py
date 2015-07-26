from nucleus.models import *
from placement.models import *
import ipdb

old_company_lst = CompanyContact.objects.all()
length_of_lst = len(old_company_lst)
i=1
x=False
empty_name = 0
for old_company in old_company_lst:
 if x:
   ipdb.set_trace()
 try:
  print str(i)+" out of "+str(length_of_lst)
  new_add = not CompanyContactInfo.objects.filter(name=old_company.company_name).exists()
  if new_add:
    new_company = CompanyContactInfo()
    if old_company.company_name == "":
      new_company.name = "NOT ADDED "+str(empty_name+1)
      empty_name += 1
    else:
      new_company.name = old_company.company_name
    new_company.cluster = old_company.cluster
    new_company.status = old_company.status
    new_company.save()
  else:
    new_company = CompanyContactInfo.objects.get(name=old_company.company_name)

  contact_person = old_company.contactperson
  if not new_add:
    contact_person_lst = ContactPerson.objects.filter(company_contact = new_company)
    if contact_person in list(contact_person_lst):
      pass
    else:
      contact_person = old_company.contactperson
      contact_person.company_contact = new_company
      campus_contact = CampusContact()
      primary_contact_new_company = ContactPerson.objects.filter(company_contact = new_company, is_primary = True)

      if primary_contact_new_company.exists():
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

  else:
    contact_person = old_company.contactperson
    contact_person.company_contact = new_company
    campus_contact = CampusContact()
    primary_contact_new_company = ContactPerson.objects.filter(company_contact = new_company, is_primary = True)

    if primary_contact_new_company.exists():
      contact_person.is_primary = False
      campus_contact.student = primary_contact_new_company[0].campuscontact.student
    else:
      contact_person.is_primary = True
      try:
        company_coordinator = CompanyCoordi.objects.get(student__user__name=old_company.person_in_contact)
        student = company_coordinator.student
        campus_contact.student = student
      except CompanyCoordi.DoesNotExist:
        pass
    contact_person.save()
    campus_contact.last_contact = old_company.last_contact
    campus_contact.when_to_contact = old_company.when_to_contact
    campus_contact.contact_person = contact_person
    campus_contact.save()

  if old_company.comments!="":
    if new_add:
      company_comment = CompanyContactComments()
      company_comment.comment = old_company.comments
      company_comment.campus_contact = campus_contact
      company_comment.save()
    else:
      if CompanyContactComments.objects.filter(comment=old_company.comments, campus_contact__contact_person = contact_person).exists():
        pass
      else:
        company_comment = CompanyContactComments()
        company_comment.comment = old_company.comments
        company_comment.campus_contact = campus_contact
        company_comment.save()

  i=i+1
  x = False
 except Exception as e:
  x = True
  f = open("errors.txt", 'a')
  f.write(": ".join((unicode(str(old_company.id),errors='ignore'),unicode(str(e),errors='ignore'),"\n")))
  f.close()
 except UnicodeEncodeError as e:
  x = True
  f = open("errors.txt", 'a')
  f.write(": ".join((unicode(str(old_company.id),errors='ignore'),unicode(str(e),errors='ignore'),"\n")))
  f.close()
