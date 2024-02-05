from django.shortcuts import render,redirect
from django.http import HttpResponse
import jinja2
from userlogin.models import *
from django.views import View
from .models import *
from django.contrib import messages
# Create your views here.
from userlogin.models import customer
#class for handling the user session

def getuserid(request):
    if request.session.has_key('email'):
        email = request.session['email']
    user=customer.objects.filter(email=email).first()
    return user
class usersession:

    #class method for checking the user session i
    #if user session is not expired returns user object
    #else returns the None
    def getuser(self,request):

        if request.session.has_key('email') :
            email=request.session['email']
            print('------email---------',email)
            if email is not None:
                myuser=customer.objects.filter(email=email).first()
                print(myuser)
                if myuser is not None:
                    return myuser
        return None

    #home method for redirecting the user to resume.html page
def home(request):
    return render(request,'resume/resume.html')


#class for handling user personal details
class personal_details(View,usersession):

    #class method for getting the user details from the database and redirecting it to the user
    def get(self,request):
        user=usersession().getuser(request)
        print(user)
        if user is not None:
            user=customer.objects.get(username=user)
            #print(user)
            try:
                p_details=customer_p_details.objects.get(email=user.email)
            except:
                return render(request,'resume/personal_details.html',{'user':user})

        return render(request,'resume/personal_details.html',{'user':user,'city':p_details.city,'gender':p_details.gender})

    #http post method for getting the details from the user
    # and saving it in the database
    def post(self,request):
        user = usersession().getuser(request)
        print(user)

        #if usersession is not expired
        #getting the details from the user and saving it
        if user is not None:
            username=getuserid(request)
            user = customer.objects.get(username=user)
            fullname=user.first_name +" "+user.last_name
            email=user.email
            dob=user.dob
            mobile=user.mobile
            city=request.POST.get('city')
            print(request.POST)
            gender=request.POST.get('gender')

            #saving the details into the database
            try:
                existed_user=customer_p_details.objects.get(username=username)
                if existed_user:
                    existed_user.city = city
                    existed_user.gender = gender
                    messages.success(request, 'successfully updated')
                    existed_user.save()

            #if any error during the saving the previous details
            except:
                username = getuserid(request)
                p_details=customer_p_details.objects.create(username=username,full_name=fullname,email=email,dob=dob,mobile=mobile,city=city,gender=gender)
                messages.success(request,'successfully updated')
            return redirect('/build')

#class for handling the education details of an user
class education_details(View,usersession):

    #http get method
    #checking the user session if not expired
    #getting all saved education details from database and showing to the user
    def get(self,request):
        user=usersession().getuser(request)
        print(user)

        #if user session is not expired
        #fetching the details of the user and rendering it to the user
        if user is not None:
            user=customer.objects.get(username=user)
            #print(user)
            try:
               # print(user.email)
                e_details=customer_e_details.objects.filter(email=user.email)
                #print(e_details)
            except:
                #print('exception')
                return render(request,'resume/education.html')


        return render(request,'resume/education.html',{'user':user,'education':e_details})

    # http post method
    # checking the user session if not expired
    # getting all  education details from user and saving it in the database
    def post(self,request):
        #print(request.POST)
        user = usersession().getuser(request)
       # print(user)
        if user is not None:
            username = getuserid(request)
            user = customer.objects.get(username=user)
            length=len(request.POST)
            email=user.email
            print(request.POST)


            #saving the new details and in the details
            #by accessing the sequentially in the database
            for i in range(1,(length//5)+1):

                course=request.POST.get('course'+str(i))
                college=request.POST.get('college'+str(i))
                passing_year=request.POST.get('passing' + str(i))
                percentage=request.POST.get('percentage' + str(i))
                city=request.POST.get('city' + str(i))
               # print(course)
               ## print(existing_details)

                try:
                    existing_details=customer_e_details.objects.filter(course=course)
                    print(existing_details)
                    if len(existing_details) !=0:
                        print("if",len(existing_details))
                        existing_details.update(course=course,year_of_passing=passing_year,percentage=percentage,college=college,college_city=city)
                    else:
                        user=usersession().getuser(request).username
                        username=customer_p_details.objects.get(username=user)
                        ed_details = customer_e_details.objects.create(username=username,email=email, course=course,
                                                                       year_of_passing=passing_year,
                                                                       percentage=percentage, college=college,
                                                                       college_city=city)
                        ed_details.save()

                   #  print(existing_details)
                   #  existing_details.college=college
                   # # print(college)
                   #  existing_details.year_of_passing=passing_year
                   #  existing_details.percentage=percentage
                   #
                   #  existing_details.college=college
                   #  existing_details.college_city=city
                   #  existing_details.save()

                except:
                    print("new")
                    ed_details=customer_e_details.objects.create(email=email,course=course,year_of_passing=passing_year,percentage=percentage,college=college,college_city=city)
                    ed_details.save()
            messages.success(request,'successfully updated')
            return redirect('/build')

            #print(course,college,passing_year,percentage,city)
        else:
            return redirect('signin')

#class for handling the internships details of an user
class internship_details(View,usersession):

    # http get method
    # checking the user session if not expired
    # getting all saved internship details from database and showing to the user
    def get(self,request):
        user = usersession().getuser(request)
        print(user)

        # if user session is not expired
        # fetching the details of the user and rendering it to the user
        if user is not None:
            user = customer.objects.get(username=user)
            # print(user)
            try:
                # print(user.email)
                intern_details = customer_intern_details.objects.filter(email=user.email)
                # print(e_details)
                for i in intern_details:
                    i.durationfrom = i.durationfrom.strftime("%Y-%m-%d")
                    i.durationto = i.durationto.strftime("%Y-%m-%d")
            except:
                # print('exception')
                return render(request, 'resume/intern.html')
            return render(request, 'resume/intern.html', {'user': user, 'intern': intern_details})

    # http post method
    # checking the user session if not expired
    # getting all  internship details from user and saving it in the database
    def post(self,request):
        print(request.POST)
        user = usersession().getuser(request)
        # print(user)
        username = getuserid(request)
        if user is not None:
            user = customer.objects.get(username=user)
            length = len(request.POST)
            email = user.email

            # saving the new details and in the details
            # by accessing the sequentially in the database
            for i in range(1, (length // 5) + 1):
                company = request.POST.get('company' + str(i))
                project_name = request.POST.get('project_name' + str(i))
                from_duration = request.POST.get('from_duration' + str(i))
                to_duration = request.POST.get('to_duration' + str(i))
                description = request.POST.get('description' + str(i))
                url=request.POST.get('url'+str(i))
                # print(course,college,passing_year,percentage,city)
                try:
                    existing_details = customer_intern_details.objects.filter( company=company)
                    if len(existing_details)!=0:
                        existing_details.update(email=email, company=company,
                                                                   durationfrom=from_duration, durationto=to_duration,
                                                                   projectname=project_name, description=description,url=url)
                    else:
                        user = usersession().getuser(request).username
                        username = customer_p_details.objects.get(username=user)
                        ed_details = customer_intern_details.objects.create(username=username, email=email,
                                                                            company=company,
                                                                            durationfrom=from_duration,
                                                                            durationto=to_duration,
                                                                            projectname=project_name,
                                                                            description=description, url=url)
                        ed_details.save()
                    # existing_details.company = company
                    # existing_details.durationfrom = from_duration
                    # existing_details.durationto = to_duration
                    # existing_details.projectname = project_name
                    # existing_details.description = description
                    # existing_details.url=url
                    # existing_details.save()

                except:
                    ed_details = customer_intern_details.objects.create(username=username,email=email, company=company,
                                                                   durationfrom=from_duration, durationto=to_duration,
                                                                   projectname=project_name, description=description,url=url)
                    ed_details.save()
            messages.success(request, 'successfully updated')
            return redirect('/build')

            # print(course,college,passing_year,percentage,city)
        else:
            return redirect('signin')

#class for handling the project details of an user
class project_details(View,usersession):

    # http get method
    # checking the user session if not expired
    # getting all saved project details from database and showing to the user
    def get(self,request):
        user = usersession().getuser(request)
        print(user)

        # if user session is not expired
        # fetching the details of the user and rendering it to the user
        if user is not None:
            user = customer.objects.get(username=user)
            # print(user)
            try:
                # print(user.email)
                intern_details = customer_project_details.objects.filter(email=user.email)
                for i in intern_details:
                    i.durationfrom = i.durationfrom.strftime("%Y-%m-%d")
                    i.durationto = i.durationto.strftime("%Y-%m-%d")
                print(intern_details)
            except:
                # print('exception')
                return render(request, 'resume/project_details.html')
            return render(request, 'resume/project_details.html', {'user': user, 'projects': intern_details})

    # http post method
    # checking the user session if not expired
    # getting all  project details from user and saving it in the database
    def post(self,request):
        print(request.POST)
        user = usersession().getuser(request)
        username = getuserid(request)
        # print(user)
        if user is not None:
            user = customer.objects.get(username=user)
            length = len(request.POST)
            email = user.email

            # saving the new details and in the details
            # by accessing the sequentially in the database
            for i in range(1, (length // 5) + 1):
                company = request.POST.get('company' + str(i))
                project_name = request.POST.get('project_name' + str(i))
                from_duration = request.POST.get('from_duration' + str(i))
                to_duration = request.POST.get('to_duration' + str(i))
                description = request.POST.get('description' + str(i))
                url = request.POST.get('url' + str(i))
                # print(course,college,passing_year,percentage,city)
                try:
                    existing_details = customer_project_details.objects.filter(email=email, company=company)

                    if len(existing_details) != 0:
                        existing_details.update(email=email, company=company,
                                                                   durationfrom=from_duration, durationto=to_duration,
                                                                   projectname=project_name, description=description,url=url)
                    else:
                        user = usersession().getuser(request).username
                        username = customer_p_details.objects.get(username=user)
                        ed_details = customer_project_details.objects.create(username=username, email=email,
                                                                            company=company,
                                                                            durationfrom=from_duration,
                                                                            durationto=to_duration,
                                                                            projectname=project_name,
                                                                            description=description, url=url)
                        ed_details.save()

                except:
                    ed_details = customer_project_details.objects.create(username=username,email=email, company=company,
                                                                   durationfrom=from_duration, durationto=to_duration,
                                                                   projectname=project_name, description=description,url=url)
                    ed_details.save()
            messages.success(request, 'successfully updated')
            return redirect('/build')

            # print(course,college,passing_year,percentage,city)
        else:
            return redirect('signin')

#class for handling the skills details of an user
class skills(View,usersession):

    # http get method
    # checking the user session if not expired
    # getting all saved skills details from database and showing to the user
    def get(self,request):
        user = usersession().getuser(request)
        #print(user)

        # if user session is not expired
        # fetching the details of the user and rendering it to the user
        if user is not None:
            user = customer.objects.get(username=user)
            # print(user)
            try:
                # print(user.email)
                intern_details = customer_skills.objects.filter(email=user.email)

            except:
                # print('exception')
                return render(request, 'resume/skills.html')
            return render(request, 'resume/skills.html', {'user': user, 'skills': intern_details})

    # http post method
    # checking the user session if not expired
    # getting all  skills details from user and saving it in the database
    def post(self,request):
        print(request.POST)
        #return redirect('/build')
        user = usersession().getuser(request)
        username = getuserid(request)
        print(user)
        if user is not None:
            user = customer.objects.get(username=user)
            length=len(request.POST)
            #print(length)

            # saving the new details and in the details
            # by accessing the sequentially in the database
            i=0
            while i<length:
                exist=customer_skills.objects.filter(email=user.email)
                print(len(exist))
                while i<len(exist):
                    skill=request.POST.get('skills'+str(i+1))
                    exist[i].skills=skill
                    exist[i].save()
                    i+=1
                    print('object created')

                if i<length:
                    skill = request.POST.get('skills' + str(i + 1))
                    print('skill',skill)

                    user = usersession().getuser(request)
                    username = customer_p_details.objects.get(username=user.username)

                    new_skill=customer_skills.objects.create(username=username,email=user.email,skills=skill)
                    new_skill.save()
                    i+=1
                    print('object created')
            return redirect('build')
        else:
            messages.warning(request,'something went wrong please signin again ')
            return redirect('signin')


#class for handling the language details of an user
class languages(View,usersession):

    # http get method
    # checking the user session if not expired
    # getting all saved language details from database and showing to the user
    def get(self,request):
        user = usersession().getuser(request)
        #print(user)

        # if user session is not expired
        # fetching the details of the user and rendering it to the user
        if user is not None:
            user = customer.objects.get(username=user)
            # print(user)
            try:
                # print(user.email)
                intern_details = customer_languages.objects.filter(email=user.email)

            except:
                # print('exception')
                return render(request, 'resume/languages_known.html')
            return render(request, 'resume/languages_known.html', {'user': user, 'lang': intern_details})

    # http post method
    # checking the user session if not expired
    # getting all  language details from user and saving it in the database
    def post(self,request):
        print(request.POST)
        #return redirect('/build')
        user = usersession().getuser(request)
        print(user)
        username = getuserid(request)
        if user is not None:
            user = customer.objects.get(username=user)
            length=len(request.POST)
            print(length)

            # saving the new details and in the details
            # by accessing the sequentially in the database
            i = 0
            while i < length:
                exist = customer_languages.objects.filter(email=user.email)
                print(len(exist))
                while i < len(exist):
                    lang = request.POST.get('lang' + str(i + 1))
                    print(exist[i])
                    exist[i].language = lang
                    exist[i].save()
                    i += 1
                    print('object created')

                if i < length:
                    skill = request.POST.get('lang' + str(i + 1))
                    user = usersession().getuser(request)
                    username = customer_p_details.objects.get(username=user.username)
                    new_skill = customer_languages.objects.create(username=username,email=user.email, language=skill)
                    new_skill.save()
                    i += 1
                    print('object created')
            return redirect('build')

            messages.success(request,'saved successfully')
            return redirect('build')
        else:
            messages.warning(request,'something went wrong please signin again ')
            return redirect('signin')


#class for handling the achievements details of an user
class achievements_details(View,usersession):

    # http get method
    # checking the user session if not expired
    # getting all saved achievements details from database and showing to the user
    def get(self,request):
        user = usersession().getuser(request)
        # print(user)

        # if user session is not expired
        # fetching the details of the user and rendering it to the user
        if user is not None:
            user = customer.objects.get(username=user)
            # print(user)
            try:
                # print(user.email)
                intern_details = customer_achievements.objects.filter(email=user.email)

            except:
                # print('exception')
                return render(request, 'resume/achivements.html')
            return render(request, 'resume/achivements.html', {'user': user, 'achievements': intern_details})

    # http post method
    # checking the user session if not expired
    # getting all  achivements details from user and saving it in the database
    def post(self,request):
        print(request.POST)
        #return redirect('/build')
        user = usersession().getuser(request)
        print(user)
        username = getuserid(request)
        if user is not None:
            user = customer.objects.get(username=user)
            length=len(request.POST)
            #print(length)

            # saving the new details and in the details
            # by accessing the sequentially in the database
            i = 0
            while i < length:
                exist = customer_achievements.objects.filter(email=user.email)
                print(len(exist))
                while i < len(exist):
                    lang = request.POST.get('achivements' + str(i + 1))
                    print(exist[i])
                    exist[i].achivements = lang
                    exist[i].save()
                    i += 1
                    print('object created')

                if i < length:
                    skill = request.POST.get('achivements' + str(i + 1))
                    user = usersession().getuser(request)
                    username = customer_p_details.objects.get(username=user.username)
                    new_skill = customer_achievements.objects.create(username=username,email=user.email, achivements=skill)
                    new_skill.save()
                    i += 1
                    print('object created')


            messages.success(request,'saved successfully')
            return redirect('build')
        else:
            messages.warning(request,'something went wrong please signin again ')
            return redirect('signin')

def showtemplates(request):
    return render(request,'resume/resume.html',{'show':1})




#method for showing the user details in resume template 1
def resume1(request):
    user = usersession().getuser(request)
    print(user)
    if user is not None:
        user = customer.objects.get(username=user)
        email = user.email

        #retrieving the personal details from the database
        try:
            personal_details = customer_p_details.objects.get(email=email)
        except:
            messages.warning(request, 'fill the personal details to continue !')
            return redirect('build')

        # retrieving the education details from the database
        try:
            education_details = customer_e_details.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the education details to continue !')
            return redirect('build')

        # retrieving the internship details from the database
        try:
            intern_details = customer_intern_details.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the internship details to continue !')
            return redirect('build')

        # retrieving the project details from the database
        try:
            project_details = customer_project_details.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the project details to continue !')
            return redirect('build')

        # retrieving the skills details from the database
        try:
            skills_details = customer_skills.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the skills details to continue !')
            return redirect('build')

        # retrieving the language details from the database
        try:
            languages_details = customer_languages.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the language details to continue !')
            return redirect('build')

        # retrieving the achivements details from the database
        try:
            achievements_details = customer_achievements.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the achievements details to continue !')
            return redirect('build')

        #redirecting the user with all user details to the resume template

        return render(request, 'resume/resume1.html',
                          {'personal': personal_details, 'education': education_details, 'internships': intern_details,
                           'projects': project_details, 'skills': skills_details, 'languages': languages_details,
                           'achivements': achievements_details})


#method for resume template 2
def resume2(request):
    user = usersession().getuser(request)
    print(user)

    #checking the user session
    if user is not None:
        user = customer.objects.get(username=user)
        email = user.email

        # retrieving the personal details from the database
        try:
            personal_details = customer_p_details.objects.get(email=email)
        except:
            messages.warning(request, 'fill the personal details to continue !')
            return redirect('build')

        # retrieving the education details from the database
        try:
            education_details = customer_e_details.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the education details to continue !')
            return redirect('build')

        # retrieving the internship details from the database
        try:
            intern_details = customer_intern_details.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the internship details to continue !')
            return redirect('build')

        # retrieving the project details from the database
        try:
            project_details = customer_project_details.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the project details to continue !')
            return redirect('build')

        # retrieving the skills details from the database
        try:
            skills_details = customer_skills.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the skills details to continue !')
            return redirect('build')

        # retrieving the language details from the database
        try:
            languages_details = customer_languages.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the language details to continue !')
            return redirect('build')

        # retrieving the achievements details from the database
        try:
            achievements_details = customer_achievements.objects.filter(email=email)
        except:
            messages.warning(request, 'fill the achievements details to continue !')
            return redirect('build')

        #returning all fetching details to the resume template 2
    return render(request, 'resume/srt-resume.html',
                  {'personal': personal_details, 'education': education_details, 'internships': intern_details,
                   'projects': project_details, 'skills': skills_details, 'languages': languages_details,
                   'achivements': achievements_details})


def dele(request):
    all=customer_p_details.objects.all()
    for i in all:
        i.delete()
    return HttpResponse("hi")




