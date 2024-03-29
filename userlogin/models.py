from django.db import models




class customer(models.Model):
    username=models.CharField(primary_key=True,max_length=25)
    first_name=models.CharField(max_length=25)
    last_name=models.CharField(max_length=25)
    dob=models.DateField()
    mobile=models.IntegerField()
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=25)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.username



