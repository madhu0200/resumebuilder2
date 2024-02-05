from django.db import models

from django.contrib.auth.models import User
# Create your models_pkl here.
class customer_p_details(models.Model):
    username=models.CharField(primary_key=True,max_length=25)
    full_name=models.CharField(max_length=50)
    #last_name=models_pkl.CharField(max_length=25)
    dob=models.DateField()
    mobile=models.IntegerField()
    email=models.EmailField(unique=True)
    ##is_active=models_pkl.BooleanField(default=False)
    city=models.CharField(max_length=25)
    gender=models.CharField(max_length=6)

    def __str__(self):
        return self.username

class customer_e_details(models.Model):
    username = models.ForeignKey(customer_p_details, on_delete=models.CASCADE, default=" ")
    email=models.EmailField()
    course=models.CharField(max_length=50)
    year_of_passing=models.IntegerField()
    percentage=models.IntegerField()
    college=models.CharField(max_length=60)
    college_city=models.CharField(max_length=30)

    def __str__(self):
        return self.email

class customer_intern_details(models.Model):
    username = models.ForeignKey(customer_p_details, on_delete=models.CASCADE, default=" ")
    email=models.EmailField()
    company=models.CharField(max_length=50)
    durationfrom=models.DateField()
    durationto=models.DateField()
    projectname=models.CharField(max_length=60)
    description=models.CharField(max_length=500)
    url=models.CharField(max_length=120,default=None)

    def __str__(self):
        return self.email

class customer_project_details(models.Model):
    username = models.ForeignKey(customer_p_details, on_delete=models.CASCADE, default=" ")
    email=models.EmailField()
    company=models.CharField(max_length=50)
    durationfrom=models.DateField()
    durationto=models.DateField()
    projectname=models.CharField(max_length=60)
    description=models.CharField(max_length=500)
    url=models.CharField(max_length=120,default=None)

    def __str__(self):
        return self.email


class customer_skills(models.Model):
    username = models.ForeignKey(customer_p_details, on_delete=models.CASCADE, default=" ")
    email=models.EmailField()
    skills=models.CharField(max_length=60)

    def __str__(self):
        return self.email

class customer_languages(models.Model):
    username = models.ForeignKey(customer_p_details, on_delete=models.CASCADE, default=" ")

    email=models.EmailField()
    language=models.CharField(max_length=60)

    def __str__(self):
        return self.email

class customer_achievements(models.Model):
    username = models.ForeignKey(customer_p_details, on_delete=models.CASCADE, default=" ")

    email=models.EmailField()
    achivements=models.CharField(max_length=60)

    def __str__(self):
        return self.email


