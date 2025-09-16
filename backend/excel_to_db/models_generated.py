from django.db import models

class ExcelData(models.Model):
    # auto-generated model from Excel
    user_id = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    registration_source = models.CharField(max_length=255, null=True, blank=True)
    registered_on = models.CharField(max_length=255, null=True, blank=True)
    last_login_date = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    current_company = models.CharField(max_length=255, null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    institue = models.CharField(max_length=255, null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    reume_upload_month_file_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"

