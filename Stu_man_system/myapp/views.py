from django.shortcuts import render,redirect
from . models import User,Book,Club
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import HttpResponse


# Create your views here.
def index(request):
	return render(request,'index.html')

def register(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg='Email Already Registered'
			return render(request,'login.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					usertype=request.POST['usertype'],
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					profile_picture=request.FILES['profile_picture']
					)
				msg='User Registered Successfully'
				return render(request,'login.html',{'msg':msg})
			else:
				msg='Password and Confirm password does not match'
				return render(request,'register.html',{'msg':msg})
	else:
		return render(request,'register.html')

def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:

				request.session['fname']=user.fname
				request.session['email']=user.email
				request.session['profile_picture']=user.profile_picture.url
				student_count = User.objects.filter(usertype='student')
				request.session['stu_count'] = len(student_count)
				teacher_count=User.objects.filter(usertype='teacher')
				request.session['tea_count'] = len(teacher_count)
				msg='Login Successful'
				return render(request,'index.html',{'msg':msg,'stu_count': request.session['stu_count']})
			else:
				msg='Incorrect password'
				return render(request,'login.html',{'msg':msg})

		except Exception as e:
			msg='User not registered'
			return render(request,'register.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['fname']
		del request.session['email']
		del request.session['profile_picture']
		msg='User Logged out Successfully'
		return render(request,'login.html',{'msg':msg})

	except:
		msg='User Logged out Successfully'
		return render(request,'login.html',{'msg':msg})

def change_password(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.session['email'])
			if user.password==request.POST['password']:
				if request.POST['new_password']==request.POST['cnew_password']:
					if user.password!=request.POST['new_password']:
						user.password=request.POST['new_password']
						user.save()
						msg='Password Changed Successfully'
						return render(request,'login.html',{'msg':msg})
					else:
						msg='New Password can not be from old passwords'
						return render(request,'change-password.html',{'msg':msg})
				else:
					msg='New Password and confirm New Password does not match'
					return render(request,'change-password.html',{'msg':msg})
			else:
				msg='Incorrect Old Password'
				return render(request,'change-password.html',{'msg':msg})

		except:
			msg='User Not Found'
			return render(request,'register.html',{'msg':msg})

	else:
		return render(request,'change-password.html')

def forgot_password(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject='OTP for forgot password'
			message='Hello'+user.fname+'Your OTP for forgot password is'+str(otp)
			from_email=settings.EMAIL_HOST_USER
			recipient_list=[user.email,]
			request.session['email']=user.email
			request.session['otp']=otp
			send_mail(subject, message, from_email,recipient_list)
			return render(request,'otp.html')
		except Exception as e:
			print(e)
			msg='USer Not Found'
			return render(request,'register.html',{'msg':msg})	
	else:
		return render(request,'forgot-password.html')


def verify_otp(request):
	if request.method=='POST':
		otp1=str(request.session['otp'])
		otp2=str(request.POST['otp'])
		if otp1==otp2:
			del request.session['otp']
			return render(request,'new-password.html')
		else:
			msg='Invalid OTP'
			return render(request,'otp.html')
	else:
		return render(request,'otp.html')


def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(email=request.session['email'])
		user.password=request.POST['new_password']
		user.save()
		del request.session['email']
		msg='Password Updated Successfully'
		return render(request,'login.html',{'msg':msg})

	else:
		msg='New Password and confirm new password does not match'
		return render(request,'new-password.html',{'msg':msg})
	return render(request,'new-password.html')

def profile(request):

	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
		user.save()
		request.session['profile_picture']=user.profile_picture.url
		msg='Profile updated Successfully'
		return render(request,'profile.html',{'user':user,'msg':msg})
	else:			
		return render(request,'profile.html',{'user':user})

def add_student(request):
	if request.method=='POST':
		action=request.POST.get('action')
		if action=='add':
			email=request.POST['email']
			try:
				user=User.objects.get(email=email)
				msg='User already registered'
				return render(request,'student.html',{'msg':msg})

			except Exception as e:
				print(e)
			
				user=User.objects.create(
						usertype=request.POST['usertype'],
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
						profile_picture=request.FILES['profile_picture']
						)

				msg='Student Inserted Successfully'
				student_count = User.objects.filter(usertype='student')
				request.session['stu_count'] = len(student_count)
				subject='Congratulation! Registration Successful'
				message='Hello'+user.fname+'Your login id is'+user.email+'and your password is'+user.password
				from_email=settings.EMAIL_HOST_USER
				recipient_list=[user.email,]
				send_mail(subject, message, from_email,recipient_list)
				return render(request,'student.html',{'msg':msg,'stu_count': request.session['stu_count']})

		elif action=='select':
			email=request.POST.get('email')
			try:

				user=User.objects.get(email=email)
				
				msg='USer Found'
				return render(request,'student.html',{'user':user,'msg':msg})
			except:
				msg = 'User Not Found'
				return render(request, 'student.html', {'msg': msg})
		
		elif action=='update':
			email=request.POST.get('email')
			try:

				user=User.objects.get(email=email)
		
				user.fname=request.POST['fname']
				user.lname=request.POST['lname']
				user.mobile=request.POST['mobile']
				user.address=request.POST['address']
				try:
					user.profile_picture=request.FILES['profile_picture']
				except:
					pass
				user.save()
				
				msg='Profile updated Successfully'
				return render(request,'student.html',{'user':user,'msg':msg})
			except:
				msg = 'User Not Found'
				return render(request, 'student.html', {'msg': msg})

		elif action=='delete':
			email=request.POST.get('email')
			try:
				user=User.objects.get(email=email)
				user.delete()
				msg='USer deleted successfully'
				student_count = User.objects.filter(usertype='student')
				request.session['stu_count'] = len(student_count)
				return render(request,'student.html',{'msg':msg,'stu_count': request.session['stu_count']})
			except:
				msg='User Not Found'
				return render(request,'student.html',{'msg':msg})

		else:
			msg='Invalid action'
			return render(request,'student.html',{'msg':msg})
	else:
		return render(request,'student.html')

def add_teacher(request):
	if request.method=='POST':
		act=request.POST.get('act')
		if act=='add':
			email=request.POST['email']
			try:
				user=User.objects.get(email=email)
				msg='User already registered'
				return render(request,'teacher.html',{'msg':msg})

			except Exception as e:
				print(e)
			
				user=User.objects.create(
						usertype=request.POST['usertype'],
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
						profile_picture=request.FILES['profile_picture']
						)

				msg='Teacher Inserted Successfully'
				teacher_count=User.objects.filter(usertype='teacher')
				request.session['tea_count'] = len(teacher_count)
				subject='Congratulation! Registration Successful'
				message='Hello'+user.fname+'Your login id is'+user.email+'and your password is'+user.password
				from_email=settings.EMAIL_HOST_USER
				recipient_list=[user.email,]
				send_mail(subject, message, from_email,recipient_list)
				return render(request,'teacher.html',{'msg':msg,'user':user,'tea_count':request.session['tea_count']})

		elif act=='select':
			email=request.POST.get('email')
			try:

				user=User.objects.get(email=email)
				
				msg='USer Found'
				return render(request,'teacher.html',{'user':user,'msg':msg})
			except:
				msg = 'User Not Found'
				return render(request, 'teacher.html', {'msg': msg})
		
		elif act=='update':
			email=request.POST.get('email')
			try:

				user=User.objects.get(email=email)
		
				user.fname=request.POST['fname']
				user.lname=request.POST['lname']
				user.mobile=request.POST['mobile']
				user.address=request.POST['address']
				try:
					user.profile_picture=request.FILES['profile_picture']
				except:
					pass
				user.save()
				
				msg='Updated Successfully'
				return render(request,'teacher.html',{'user':user,'msg':msg})
			except:
				msg = 'User Not Found'
				return render(request, 'teacher.html', {'msg': msg})

		elif act=='delete':
			email=request.POST.get('email')
			try:
				user=User.objects.get(email=email)
				user.delete()
				msg='USer deleted successfully'
				teacher_count=User.objects.filter(usertype='teacher')
				request.session['tea_count'] = len(teacher_count)
				return render(request,'teacher.html',{'msg':msg,'tea_count':request.session['tea_count']})
			except:
				msg='User Not Found'
				return render(request,'teacher.html',{'msg':msg})

		else:
			msg='Invalid action'
			return render(request,'teacher.html',{'msg':msg})
	else:
		return render(request,'teacher.html')



def add_book(request):
	if request.method=='POST':
		ac=request.POST.get('ac')
		if ac=='add':
			isbn=request.POST['isbn']
			try:
				book=Book.objects.get(isbn=isbn)
				msg='Book already registered'
				return render(request,'book.html',{'msg':msg})

			except Exception as e:
				print(e)
			
				book=Book.objects.create(
						name=request.POST['bname'],
						isbn=isbn,
						publisher=request.POST['publisher'],
						author=request.POST['author'],
						)

				msg='Book Inserted Successfully'
				book_count = Book.objects.count()
				request.session['b_count'] = book_count
				return render(request,'book.html',{'msg':msg,'book':book,'b_count':request.session['b_count']})

		elif ac=='select':
			isbn=request.POST.get('isbn')
			try:

				book=Book.objects.get(isbn=isbn)
				
				msg='Book Found'
				return render(request,'book.html',{'book':book,'msg':msg})
			except:
				msg = 'Book Not Found'
				return render(request, 'book.html', {'msg': msg})
		
		elif ac=='update':
			isbn=request.POST.get('isbn')
			try:

				book=Book.objects.get(isbn=isbn)
		
				book.name=request.POST['bname']
				book.isbn=request.POST['isbn']
				book.publisher=request.POST['publisher']
				book.author=request.POST['author']
				book.save()
				
				msg='Book Updated Successfully'
				return render(request,'book.html',{'book':book,'msg':msg})
			except:
				msg = 'Book Not Found'
				return render(request, 'book.html', {'msg': msg})

		elif ac=='delete':
			isbn=request.POST.get('isbn')
			try:
				book=Book.objects.get(isbn=isbn)
				book.delete()
				msg='Book deleted successfully'
				book_count=Book.objects.filter(book=book)
				request.session['b_count'] = len(book_count)
				return render(request,'book.html',{'msg':msg,'b_count':request.session['b_count']})
			except:
				msg='Book Not Found'
				return render(request,'book.html',{'msg':msg})

		else:
			msg='Invalid action'
			return render(request,'book.html',{'msg':msg})
	else:
		return render(request,'book.html')


def add_club(request):
	if request.method=='POST':
		ax=request.POST.get('ax')
		if ax=='add':
			club_name=request.POST['cname']
			
			try:
				club=Club.objects.get(club_name=club_name)
				msg='Club already registered'
				return render(request,'club.html',{'msg':msg})

			except Exception as e:
				print(e)
				
				club=Club.objects.create(
						club_name=club_name,
						
						)

				msg='Club Inserted Successfully'
				club_count = Club.objects.count()
				request.session['c_count'] =club_count
				return render(request,'club.html',{'msg':msg,'club':club,'c_count':request.session['c_count']})

		elif ax=='select':
			club_name=request.POST['cname']
			try:

				club=Club.objects.get(club_name=club_name)
				
				msg='Club Found'
				return render(request,'club.html',{'club':club,'msg':msg})
			except:
				msg = 'Club Not Found'
				return render(request, 'club.html', {'msg': msg})

		elif ax=='delete':
			club_name=request.POST['cname']
			try:
				club=Club.objects.get(club_name=club_name)
				club.delete()
				msg='Club deleted successfully'
				club_count=Club.objects.filter(club=club)
				request.session['c_count'] = len(club_count)
				return render(request,'club.html',{'msg':msg,'c_count':request.session['c_count']})
			except:
				msg='Club Not Found'
				return render(request,'club.html',{'msg':msg})

		else:
			msg='Invalid action'
			return render(request,'club.html',{'msg':msg})
	else:
		return render(request,'club.html')

