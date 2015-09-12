from placement.models import Results, Company, SecondRound, CompanyApplicationMap, PpoRejection
import datetime
import json

def can_apply(plac_person, company_applying) :
  """
  Check whether the PlacementPerson can apply to a particular company or not.
  Returns :
    True : if the person can apply
    'msg' : The message stating the reason why he cannot apply to the company.
  """
  if CompanyApplicationMap.objects.filter(plac_person=plac_person, company=company_applying).count()!=0 :
    return 'You have already applied to '+str(company_applying.name)
  if not company_applying.status == 'OPN' :
    return company_applying + ' is not open for applications.'
  if plac_person.student.branch not in company_applying.open_for_disciplines.all() :
    return company_applying.name + ' is not open for your branch.'
  if ppo_rejected(plac_person, company_applying):
    return "You have rejected PPO of higher package. You can not apply to this company"
  if plac_person.no_of_companies_placed == 2 :
    return 'You have been placed in two companies.'
  if plac_person.no_of_companies_placed == 0 :
    return True
  #if not SecondRound.objects.filter(branch = plac_person.student.branch,
  #                                  year = current_session_year() ).exists() :
    #return 'You have been placed and second Round is not open for your branch.'
  placed_company_category = plac_person.placed_company_category
  if placed_company_category == 'A' :
    return 'You have already been placed in "A" category company.'
  if placed_company_category == 'B' and company_applying.category in ('C', 'U') :
    return 'You have already been placed in "B" category company.'
  if placed_company_category == 'B' and company_applying.category in ('A', 'B') :
    if SecondRound.objects.filter(branch = plac_person.student.branch, year = current_session_year()).exists() :
      return True
    else :
      return 'You have already been placed in "B" category company and Second round is not open for your branch.'
  if placed_company_category in ('C','U') and company_applying.category in ('C', 'U') :
    return True
#  if placed_company_category == 'U' and company_applying.category in ('U') :
#   return 'You have already been placed in an university.'
  return True

def ppo_rejected(plac_person, company_applying):
  def INR_USD_request():
    import requests
    r = requests.get("http://api.fixer.io/latest?base=USD")
    if r.status_code != 200:
      return 65
    return json.loads(r.content)['rates']['INR']

  def parse_value(package_str):
    package_str = package_str.split()
    package = float(package_str[0])
    if package_str[1] == 'Thousands':
      package = package*1000
    elif package_str[1] == 'Lacs':
      package = package*100000
    return package, package_str[2]

  ppo_reject_inst = PpoRejection.objects.get_or_none(plac_person = plac_person)
  if not ppo_reject_inst:
    return False
  ppo_package = ppo_reject_inst.package
  if plac_person.student.branch.graduation == 'UG':
    apply_package = company_applying.package_ug
  elif plac_person.student.branch.graduation == 'PG':
    apply_package = company_applying.package_pg
  else:# plac_person.student.branch.graduation == 'PHD':
    apply_package = company_applying.package_phd

  if not apply_package:
    return False
  ppo_package = parse_value(ppo_package)
  apply_package = parse_value(apply_package)

  if apply_package[0] == 0.0:
    return False
  if ppo_package[1] == apply_package[1]:
    return ppo_package[0] > apply_package[0]
  else:
    if ppo_package[1] == 'USD':
      return ppo_package[0]*INR_USD_request() > apply_package[0]
    else:
      return ppo_package[0] > apply_package[0]*INR_USD_request()

def get_higher_category(cat1, cat2) :
  """
  Returns the category which is higher in the sense of applying to a company.
  e.g. If a student is placed in 'B', then he can apply to 'A' category company.
  This means that 'A' category is higher than 'B'.
  This is used in the case a student gets two job offers.
  """
  # Order at the time of writing is 'A' > 'B' > 'C' > 'U'
  if cat1 == 'A' or cat2 == 'A' :
    return 'A'
  if cat1 == 'B' or cat2 == 'B' :
    return 'B'
  if cat1 == 'C' or cat2 == 'C' :
    return 'C'
  if cat1 == 'U' or cat2 == 'U' :
    return 'U'

def current_session_year():
  """
  Returns the starting year for the current session. For the session of 2011-12, it will return 2011.
  It assumes that the session starts on the first day of July.
  Used by internship online too.
  """
  return (datetime.date.today()-datetime.timedelta(6*365/12-1)).year

