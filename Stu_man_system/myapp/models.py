from django.db import models


# Create your models here.
class User(models.Model):
	usertype=models.CharField(max_length=100,choices=(
		('student','student'),
		('teacher','teacher'),
		('admin','admin'),

		))
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_picture=models.ImageField(upload_to='profile_picture/',default="")

	def __str__(self):
		return self.fname+"-"+self.usertype

class Book(models.Model):
	name=models.CharField(max_length=100)
	id = models.AutoField(primary_key=True)
	isbn=models.PositiveIntegerField()
	publisher=models.CharField(max_length=100)
	author=models.CharField(max_length=100)

	def __str__(self):
		return self.author

class Club(models.Model):
	club_name=models.CharField(max_length=100)
	
	def __str__(self):
		return self.club_name