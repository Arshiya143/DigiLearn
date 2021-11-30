from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Student,Teacher,Course,Chapter,Lesson
from django.contrib.auth import authenticate, login,logout
import os,re

# Create your views here.
def home(request):
    return render(request, "home.html")

def signin(request):
    context = {'usererror':'None','passerror':'None','error':'None'}
    return render(request, "auth/login.html",context)

def signup(request):
    context = {'usererror':'None','emailerror':'None','passerror':'None','profileerror':'None'}
    return render(request, "auth/signup.html",context)

def signout(request):
    logout(request)
    return redirect("home")

def search(request):
    if request.method == 'GET':
        s = request.GET['search']
    return redirect("stcourse")
    

def course(request):
    if request.user.is_authenticated:
        s = request.GET.get('search','None')
        if s == "None":
            cr = Course.objects.filter(teacher_id=request.user.id)
            return render(request, "teacher/course.html",{'user':request.user, 'course':cr})
        else:
            cr = Course.objects.filter(title__contains=s,teacher_id=request.user.id)
            return render(request, "teacher/course.html",{'user':request.user, 'course':cr})

def stcourse(request):
    if request.user.is_authenticated:
            course = []
            se = []
            st = Student.objects.get(user_id=request.user.id)
            s = request.GET.get('search','None')
            if s == "None":    
                cr = Course.objects.all().order_by('id')
                for c in cr:
                    cs = c.student.through.objects.filter(course_id=c.id,student_id=st.id)
                    for s in cs:
                        co = Course.objects.filter(id=s.course_id)
                        course.append(co)
                for c in course:
                    for ce in c:
                        se.append(ce.id)
                nonenroll = Course.objects.exclude(id__in=se)
                if nonenroll is None:
                    nonenroll = "None"
                return render(request, "student/course.html",{'user':request.user,'course':course,'nonenroll':nonenroll})
            else:
                cr = Course.objects.all().filter(title__contains=s)
                for c in cr:
                    cs = c.student.through.objects.filter(course_id=c.id,student_id=st.id)
                    if cs:
                        en = 1
                    else:
                        en = 0
                return render(request, "student/course.html",{'user':request.user,'cr':cr,'enroll':en})

def register(request):
    if request.method == "POST" :
        username = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        profile = request.POST['profile']
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if username is "":
            usererror = "Username Required"
        elif username.isalpha():
            usererror = "None"
        else:
            usererror = "Please enter characters A-Z only"
        if email is "":
            emailerror = "Email Required"
        elif (re.fullmatch(regex, email)):
            emailerror = "None"
        else:
            emailerror = "Please enter valid email address"
        passerror = ""
        if password is "":
            passerror = "Password Required"
        else:
            while True:
                if (len(password)<8):
                    passerror = passerror + " Minimum 8 characters."
                    break
                elif not re.search("[a-z]", password):
                    passerror = passerror +" The alphabets must be between [a-z]."
                    break
                elif not re.search("[A-Z]", password):
                    passerror = passerror +" At least one alphabet should be of Upper Case [A-Z]."
                    break
                elif not re.search("[0-9]", password):
                    passerror = passerror +" At least 1 number or digit between [0-9]."
                    break
                elif not re.search("[_@$]", password):
                    passerror = passerror +" At least 1 character from [ _ or @ or $ ]."
                    break
                elif re.search("\s", password):
                    passerror = passerror +" Space in password not allowed."
                    break
                else:
                    passerror = "None"
                    break
        if profile == "" :
            profileerror = "Profile Required"
        elif profile == "Student" or profile == "Teacher":
            profileerror = "None"
        else:
            profileerror = 'Please enter "Student" or "Teacher"'
        if usererror == "None" and emailerror == "None" and passerror == "None" and passerror == "None":
            user = User.objects.create_user(username=username, password=password ,email=email)
            login(request, user)
            userid = request.user.id
            if profile == 'Student':
                pro = Student.objects.create(profile=profile, user_id=userid)
                pro.save()
            elif profile == 'Teacher':
                pro = Teacher.objects.create(profile=profile, user_id=userid)
                pro.save()
            return redirect("login")
        else:
            context = {'username':username,'email':email,'password':password,'profile':profile,
                        'usererror':usererror,'emailerror':emailerror,'passerror':passerror,'profileerror':profileerror}
            return render(request, "auth/signup.html",context)

def sign(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        if username is "":
            usererror = "Username Required"
        elif username.isalpha():
            usererror = "None"
        else:
            usererror = "Please enter characters A-Z only"
        passerror = ""
        if password is "":
            passerror = "Password Required"
        else:
            while True:
                if (len(password)<8):
                    passerror = passerror + " Minimum 8 characters."
                    break
                elif not re.search("[a-z]", password):
                    passerror = passerror +" The alphabets must be between [a-z]."
                    break
                elif not re.search("[A-Z]", password):
                    passerror = passerror +" At least one alphabet should be of Upper Case [A-Z]."
                    break
                elif not re.search("[0-9]", password):
                    passerror = passerror +" At least 1 number or digit between [0-9]."
                    break
                elif not re.search("[_@$]", password):
                    passerror = passerror +" At least 1 character from [ _ or @ or $ ]."
                    break
                elif re.search("\s", password):
                    passerror = passerror +" Space in password not allowed."
                    break
                else:
                    passerror = "None"
                    break
        error = "None"
        if usererror == "None" and passerror == "None":
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                error = "Invalid Credentials...Please try again"
                context = {'username':username,'password':password,
                        'usererror':usererror,'passerror':passerror,'error':error}
                return render(request, "auth/login.html",context)
        else:
            context = {'username':username,'password':password,
                        'usererror':usererror,'passerror':passerror,'error':error}
            return render(request, "auth/login.html",context)
        userid = request.user.id
        st = Student.objects.filter(user_id=userid).select_related()
        th = Teacher.objects.filter(user_id=userid).select_related()
        #st = Student.objects.get(user_id=userid)
        #th = Teacher.objects.get(user_id=userid)  
        if st:
            course = []
            se = []
            st = Student.objects.get(user_id=userid)
            cr = Course.objects.all().order_by('id')
            for c in cr:
                cs = c.student.through.objects.filter(course_id=c.id,student_id=st.id)
                for s in cs:
                   co = Course.objects.filter(id=s.course_id)
                   course.append(co)
            for c in course:
                for ce in c:
                    se.append(ce.id)
            nonenroll = Course.objects.exclude(id__in=se)
            if nonenroll is None:
                nonenroll = "None"
            return render(request, "student/course.html",{'user':user,'course':course,'nonenroll':nonenroll})
            
        elif th:
            cr = Course.objects.filter(teacher_id=userid)
            return render(request, "teacher/course.html",{'user':user, 'course':cr})

def addcourse(request):
    return render(request, "teacher/addcourse.html",{'nameerror':'None','descerror':'None'})

def savecourse(request):
    if request.user.is_authenticated:
        name = request.POST['name']
        desc = request.POST['desc']
        if name is "":
            nameerror = "Title Required"
        elif name.isdigit():
            nameerror = "Title should not only contains digits"
        else:
            nameerror = "None"
        if desc is "":
            descerror = "Description Required"
        elif desc.isdigit():
            descerror = "Description should not only contains digits"
        elif len(desc)<120:
            descerror = "Description should contain 120 characters. "
        else:
            descerror = "None"
        if nameerror == "None" and descerror == "None":
            uid = request.user.id
            cr = Course.objects.create(title=name, desc=desc, teacher_id=uid)
            cr.save()
            crs = Course.objects.all().order_by('id')
            return render(request, "teacher/course.html",{'user':request.user, 'course':crs})
        else:
            return render(request, "teacher/addcourse.html",{'name':name,'desc':desc,'nameerror':nameerror,'descerror':descerror})

def editcourse(request,cr_id):
    cr = Course.objects.filter(id=cr_id)
    return render(request, "teacher/editcourse.html",{'course':cr,'nameerror':'None','descerror':'None'})

def updatecourse(request,cr_id):
    if request.user.is_authenticated:
        name = request.POST['name']
        desc = request.POST['desc']
        if name is "":
            nameerror = "Title Required"
        elif name.isdigit():
            nameerror = "Title should not only contains digits"
        else:
            nameerror = "None"
        if desc is "":
            descerror = "Description Required"
        elif desc.isdigit():
            descerror = "Description should not only contains digits"
        elif len(desc)<120:
            descerror = "Description should contain 120 characters. "
        else:
            descerror = "None"
        if nameerror == "None" and descerror == "None":
            cr = Course.objects.all().order_by('id')
            c = Course.objects.filter(id=cr_id).update(title=name,desc=desc)
            return render(request, "teacher/course.html",{'user':request.user, 'course':cr})
        else:
            cr = Course.objects.filter(id=cr_id)
            return render(request, "teacher/editcourse.html",{'course':cr,'name':name,'desc':desc,'nameerror':nameerror,'descerror':descerror})

def deletecourse(request,cr_id):
    if request.user.is_authenticated:
        cr = Course.objects.all()
        c = Course.objects.filter(id=cr_id).delete()
        return render(request, "teacher/course.html",{'user':request.user, 'course':cr})

def chapter(request,cr_id):
    if request.user.is_authenticated:
        cr = Course.objects.filter(id=cr_id)
        ch = Chapter.objects.filter(course_id=cr_id).order_by('id')
        return render(request, "teacher/chapter.html",{'user':request.user, 'course':cr, 'chapter':ch})

def addchapter(request,cr_id):
    if request.user.is_authenticated:
        cr = Course.objects.filter(id=cr_id)
        return render(request, "teacher/addchapter.html",{'user':request.user, 'course':cr,'nameerror':'None'})

def savechapter(request,cr_id):
    if request.user.is_authenticated:
        name = request.POST['name']
        if name is "":
            nameerror = "Title Required"
        elif name.isdigit():
            nameerror = "Title should not only contains digits"
        else:
            nameerror = "None"
        if nameerror == "None":
            c = Chapter.objects.create(title=name , course_id=cr_id)
            c.save()
            ch = Chapter.objects.all().order_by('id')
            cr = Course.objects.filter(id=cr_id)
            return render(request, "teacher/chapter.html",{'user':request.user, 'chapter':ch, 'course':cr})
        else:
            cr = Course.objects.filter(id=cr_id)
            return render(request, "teacher/addchapter.html",{'course':cr,'name':name,'nameerror':nameerror})

def editchapter(request,ch_id):
    ch = Chapter.objects.filter(id=ch_id)
    return render(request, "teacher/editchapter.html",{'chapter':ch,'nameerror':'None'})

def updatechapter(request,ch_id,cr_id):
    if request.user.is_authenticated:
        name = request.POST['name']
        if name is "":
            nameerror = "Title Required"
        elif name.isdigit():
            nameerror = "Title should not only contains digits"
        else:
            nameerror = "None"
        print(name)
        if nameerror == "None":
            c = Chapter.objects.get(id=ch_id)
            c.title=name
            c.course_id=cr_id
            c.save()
            ch = Chapter.objects.all().order_by('id')
            cr = Course.objects.filter(id=cr_id)
            return render(request, "teacher/chapter.html",{'user':request.user, 'chapter':ch, 'course':cr})
        else:
            ch = Chapter.objects.filter(id=ch_id)
            return render(request, "teacher/editchapter.html",{'chapter':ch,'name':name,'nameerror':nameerror})

def deletechapter(request,ch_id,cr_id):
    if request.user.is_authenticated:
        ch = Chapter.objects.all().order_by("id")
        cr = Course.objects.filter(id=cr_id)
        c = Chapter.objects.filter(id=ch_id)
        c.delete()
        return render(request, "teacher/chapter.html",{'user':request.user, 'chapter':ch, 'course':cr})

def lesson(request,ch_id):
    if request.user.is_authenticated:
        ch = Chapter.objects.filter(id=ch_id)
        ls = Lesson.objects.filter(chapter_id=ch_id).order_by('id')
        for c in ch:
            cr_id = c.course_id
        return render(request, "teacher/lesson.html",{'user':request.user, 'chapter':ch_id, 'lesson':ls, 'course':cr_id})

def addlesson(request,ch_id):
    if request.user.is_authenticated:
        ch = Chapter.objects.filter(id=ch_id)
        for c in ch:
            cr_id = c.course_id
        return render(request, "teacher/addlesson.html",{'user':request.user, 'chapter':ch,'nameerror':'None','videoerror':'None', 'course':cr_id})

def savelesson(request,ch_id):
    if request.user.is_authenticated:
        name = request.POST['name']
        if len(request.FILES) != 0:
            video = request.FILES['video']
            ext = os.path.splitext(video.name)[1]
            valid_extension = ['.mp4','.pdf','.txt','.pptx','.docx','.zip','.rar','.xlsx']
            if ext.lower() in valid_extension:
                videoerror = "None"
            else:
                videoerror = "Please select [.mp4, .pdf, .txt, .pptx, .docx, .zip, .rar, .xlsx] format file"
        else:
            videoerror = "Please select a file"
        if name is "":
            nameerror = "Title Required"
        elif name.isdigit():
            nameerror = "Title should not only contains digits"
        else:
            nameerror = "None"
        if nameerror == "None" and videoerror == "None":
            l = Lesson.objects.create(name=name, video=video, chapter_id=ch_id)
            l.save()
            ls = Lesson.objects.filter(chapter_id=ch_id).order_by('id')
            ch = Chapter.objects.filter(id=ch_id)
            for c in ch:
                cr_id = c.course_id
            return render(request, "teacher/lesson.html",{'user':request.user, 'lesson':ls, 'chapter':ch, 'course':cr_id})
        else:
            ch = Chapter.objects.filter(id=ch_id)
            for c in ch:
                cr_id = c.course_id
            return render(request, "teacher/addlesson.html",{'chapter':ch,'name':name,'nameerror':nameerror,'videoerror':videoerror,'course':cr_id})

def editlesson(request,l_id):
    l = Lesson.objects.filter(id=l_id)
    for le in l:
        ch = Chapter.objects.filter(id=le.chapter_id)
        for c in ch:
            cr_id = c.course_id
    return render(request, "teacher/editlesson.html",{'lesson':l,'nameerror':'None','videoerror':'None','course':cr_id})

def updatelesson(request,l_id,ch_id):
    if request.user.is_authenticated:
        name = request.POST['name']
        if len(request.FILES) != 0:
            video = request.FILES['video']
            ext = os.path.splitext(video.name)[1]
            valid_extension = ['.mp4','.pdf','.txt','.pptx','.docx','.zip','.rar','.xlsx']
            if ext.lower() in valid_extension:
                videoerror = "None"
            else:
                videoerror = "Please select [.mp4, .pdf, .txt, .pptx, .docx, .zip, .rar, .xlsx] format file"
        else:
            videoerror = "Please select a file"
        if name is "":
            nameerror = "Title Required"
        elif name.isdigit():
            nameerror = "Title should not only contains digits"
        else:
            nameerror = "None"
        if nameerror == "None" and videoerror == "None":
            l = Lesson.objects.get(id=l_id)
            ln = Lesson.objects.filter(id=l_id)
            for le in ln:
                le.video.close()
                le.video.delete()
            l.name=name
            l.video=video
            l.chapter_id=ch_id
            l.save()
            ls = Lesson.objects.filter(chapter_id=ch_id).order_by('id')
            ch = Chapter.objects.filter(id=ch_id)
            for c in ch:
                    cr_id = c.course_id
            return render(request, "teacher/lesson.html",{'user':request.user, 'lesson':ls, 'chapter':ch,'course':cr_id})
        else:
            l = Lesson.objects.filter(id=l_id)
            for le in l:
                ch = Chapter.objects.filter(id=le.chapter_id)
                for c in ch:
                    cr_id = c.course_id
            return render(request, "teacher/editlesson.html",{'lesson':l,'name':name,'nameerror':nameerror,'videoerror':videoerror,'course':cr_id})
            
def deletelesson(request,l_id,ch_id):
    if request.user.is_authenticated:
        ls = Lesson.objects.all().order_by("id")
        ch = Chapter.objects.filter(id=ch_id)
        l = Lesson.objects.filter(id=l_id)
        for le in l:
            le.video.closed
            le.video.close()
            le.video.delete()
        l.delete()
        return render(request, "teacher/lesson.html",{'user':request.user, 'lesson':ls, 'chapter':ch})

def listlesson(request,cr_id):
    if request.user.is_authenticated:
        cr = Course.objects.filter(id=cr_id)
        s = Student.objects.get(user_id=request.user.id)
        ch = Chapter.objects.filter(course_id=cr_id)
        for c in cr:
            if c.student.through.objects.filter(student_id=request.user.id):
                pass
            else:
                cs = c.student.add(s)
        l={}
        for cp in ch:
            ls = Lesson.objects.filter(chapter_id=cp.id)
            l[cp.title] = ls
        #for ch in l:
         #   print(ch)
          #  for key, value in l.items():
           #     if key == ch:
            #        print(value)
        return render(request, "student/lessonlist.html",{'user':request.user,'course':cr,'chapter':l})

def playlesson(request,l_id,ch_id):
    if request.user.is_authenticated:
        ch = Chapter.objects.filter(id=ch_id)
        for c in ch:
            cr_id = c.course_id
        ls = Lesson.objects.filter(id=l_id)
        return render(request, "student/playlesson.html",{'user':request.user,'lesson':ls,'course':cr_id})