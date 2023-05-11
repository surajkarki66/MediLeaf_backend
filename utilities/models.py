from django.db import models
from django.utils import timezone

class TimeStamp(models.Model):
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      abstract = True



class EditableTimeStamp(models.Model):
   created_at = models.DateTimeField()
   updated_at = models.DateTimeField()
   class Meta:
      abstract = True

   def save(self, *args, **kwargs):
      if not self.id:
         self.created_at = timezone.now()
      self.updated_at = timezone.now()
      return super().save(*args, **kwargs)