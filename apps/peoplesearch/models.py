from core import models

# Create your models here.
class services_table(models.Model):
# Insurance_companies = models.CharField(max_length=30)
# Employment_bureau = models.CharField(max_length=30)
# Courier_services = models.CharField(max_length=30)
# Chemists_diagnostic_centres = models.CharField(max_length=30)
# Hotels_restaurants = models.CharField(max_length=30)
# Banks = models.CharField(max_length=30)
# Doctors = models.CharField(max_length=30)
# Travel_agents = models.CharField(max_length=30)
# Gas_service = models.CharField(max_length=30)
# Staff_clubs = models.CharField(max_length=30)
# Miscellaneous = models.CharField(max_length=30)
  name = models.CharField(max_length=40)
  office_no = models.CharField(max_length=40)
  service = models.CharField(max_length=40)
