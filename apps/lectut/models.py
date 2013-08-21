from core import models

# Create your models here.


class FileUpload(models.Model):
   file_id = models.BigIntegerField(primary_key=True)
   file_location = models.CharField(max_length=450)
   topic = models.CharField(max_length=450)
   timestamp = models.DateTimeField()
   year = models.CharField(max_length=45, blank=True)
   file_type_list = (
       ('EP', 'Exampaper'),
       ('Le', 'Lecture'),
       ('So', 'Solution'),
       )
   file_type = modelsCharField(max_lenght=1, choices=file_type_list)
   faculty = models.ForeignKey(Faculty)
   course = models.ForeignKey(Course)


