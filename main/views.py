from django.shortcuts import render,redirect,HttpResponse,reverse
from django.contrib import messages
from . models import *
import json
from django.core.mail import send_mail
import os
import math, random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#===========Important Functions ==========


def next_post(post):
    try:
        for x in range(len(Post.objects.all())+1):
            next1=post.get_next_by_created_on()
            if next1.status=="Approved":
                return next1
            else:
                post=next1
        else:
            return None            
    except Exception as identifier:
        print(identifier)
        return None 
def previous_post(post):
    try:
        for x in range(len(Post.objects.all())+1):
            pre=post.get_previous_by_created_on()
            if pre.status=="Approved":
                return pre
            else:
                post=pre
        else:
            return None            
    except Exception as identifier: 
        print(identifier)
        return None 
def generateOTP():
    string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * length)]
    return OTP

#============================== End Important functions ===========

# Create your views here.
def index(request,p=1): 
    print("======================",request.user)
    categories=Category.objects.all()
    Tags=Tag.objects.all()
    posts=Post.objects.order_by('created_on').filter(status="Approved").reverse()
    #==================Pagination=======
    paginator = Paginator(posts,8)
    try:
        posts = paginator.page(p)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    latest_post=Post.objects.order_by('created_on').filter(status="Approved").reverse()[:4]
    popular_posts=Post.objects.order_by('-views').filter(status="Approved")[:4]
    top_stories=Post.objects.filter(id__in=[1,2,3]).filter(status="Approved")
    try:
        if request.session["RazzMyBlog_visits"]:
            request.session["RazzMyBlog_visits"]=int(request.session["RazzMyBlog_visits"])+1
        else:
             request.session["RazzMyBlog_visits"]=1
    except Exception as identifier:
        request.session["RazzMyBlog_visits"]=1
    return render (request,"main/index.html", {'category':categories,'tags':Tags,'top_stories':top_stories,
                           'latest':latest_post,'popular_posts':popular_posts,'posts':posts})

def categoryPost(request,c=1,p=1,**slug):
    categories=Category.objects.all()
    Tags=Tag.objects.all()
    cat1 = Category.objects.get(id=c)
    posts = cat1.posts.filter(status="Approved")

    #==================Pagination=======
    paginator = Paginator(posts,8)
    try:
        posts = paginator.page(p)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    latest_post=Post.objects.order_by('created_on').filter(status="Approved").reverse()[:4]
    popular_posts=Post.objects.order_by('-views').filter(status="Approved")[:4]
    top_stories=Post.objects.filter(id__in=[1,2,3]).filter(status="Approved")
    return render (request,"main/index.html", {'category':categories,'tags':Tags,'top_stories':top_stories,
                           'latest':latest_post,'popular_posts':popular_posts,'posts':posts})

def tagedPost(request,t=1,p=1,**slug):
    categories=Category.objects.all()
    Tags=Tag.objects.all()
    tag1 = Tag.objects.get(id=t)
    posts = tag1.posts.filter(status="Approved")

    #==================Pagination=======
    paginator = Paginator(posts,8)
    try:
        posts = paginator.page(p)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    latest_post=Post.objects.order_by('created_on').filter(status="Approved").reverse()[:4]
    popular_posts=Post.objects.order_by('-views').filter(status="Approved")[:4]
    top_stories=Post.objects.filter(id__in=[1,2,3]).filter(status="Approved")
    return render (request,"main/index.html", {'category':categories,'tags':Tags,'top_stories':top_stories,
                           'latest':latest_post,'popular_posts':popular_posts,'posts':posts})

def postDetails(request,id,**slug):
    current=Post.objects.get(id=id)
    current.views=current.views+1
    current.save()
    tagged=current.tags.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_post=Post.objects.order_by('created_on').filter(status="Approved").reverse()[:4]
    popular_posts=Post.objects.order_by('-views').filter(status="Approved")[:4]

    return render (request,"main/blogDetails.html",{'previous':previous_post(current),'current':current,'next':next_post(current),"tagged":tagged,"category":categories,'latest':latest_post,'popular_posts':popular_posts,"tags":tags})

def About(request):
    if request.method=="GET":
        return render(request,"main/about.html")
    if request.method == "POST":
        try:
            name=request.POST.get("name")
            email=request.POST.get("email")
            subject=request.POST.get("subject")
            message=request.POST.get("message")
            p=Prins(name=name,email=email,title=subject,content=message)
            p.save()
            messages.success(request,"Your Message Send Successfully!!")
        except Exception as identifier:
            print(identifier)
            messages.warning(request,"Sorry !! There is some Error While Sending Your Message!!")
        return redirect(request.path + "#cn")

def contact(request):
    if request.method=="GET":
        return render (request,"main/contact.html")
    if request.method=="POST":
        try:
            name=request.POST.get("name")
            email=request.POST.get("email")
            subject=request.POST.get("subject")
            message=request.POST.get("message")
            p=Query(name=name,email=email,title=subject,content=message)
            p.save()
            messages.success(request,"Your Message Send Successfully!!")
        except Exception as identifier:
            print(identifier)
            messages.warning(request,"Sorry !! There is some Error While Sending Your Message!!")
        return redirect(request.path +"#show")

def login(request):
    if request.method =="GET":
        if 'RazzMyBlog_user_name' in request.session:
            print(request.session['RazzMyBlog_user_id'],request.session['RazzMyBlog_user_name'])            
            user=User.objects.get(id=request.session['RazzMyBlog_user_id'])
            if user.role=="User":
                return redirect(reverse("Blog:Profile"))
                #return render(request,"main/profile.html",{'user':user})
            else:
                request.session['RazzMyBlog_user_photo'] =user.photo.url
                return  redirect(reverse("Author:index"))
        return render(request,"main/Login.html")
    if request.method =="POST":
        user_id=request.POST.get('user_name')
        your_pass=request.POST.get('your_pass')
        try:
            remember_me=request.POST.get('remember_me')
        except:
            remember_me=False
        try:
            user=User.objects.filter(user_id=user_id).first()
            if user.otp=="Verified":
                if your_pass==user.password:
                    request.session['RazzMyBlog_user_name']=user.name
                    request.session['RazzMyBlog_user_id']=user.id
                    response=HttpResponse()
                    if not request.COOKIES.get('RazzMyBlog_user_name') and remember_me:
                        response.set_cookie('RazzMyBlog_user_name', user.name, max_age=60*60)
                        response.set_cookie('RazzMyBlog_id', user.id, max_age=60*60)
                        response.set_cookie('RazzMyBlog_user_password', user.password, max_age=60*60)
                        response.set_cookie('RazzMyBlog_user_id', user.user_id, max_age=60*60)
                        print("============================Cookie created!!==================")
                    if user.role!="User":
                        request.session['RazzMyBlog_user_photo'] =user.photo.url
                        return redirect(reverse("Author:index"))
                    else:
                        return redirect(reverse("Blog:index"))
                else:
                    messages.warning(request,"Invalid Password !!")
                    return render(request,"main/Login.html")
            else:
                messages.info(request,"Account Not Verified!! Please Verify your account !! check you email for OTP.")
                return render(request,"main/otp.html",{"id":user.id,"otp":user.otp})
        except Exception as e:
            print(e)
            messages.warning(request,"Invalid User ID and Password !!")
            return render(request,"main/Login.html")

def register(request):
    if request.method =="GET":
        return render(request,"main/signup.html")
    if request.method =="POST":
        name = request.POST.get('name')
        userId = request.POST.get('userId')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        passwrd=request.POST.get('pass')
        otp=generateOTP()
        photo = request.FILES['photo']

        try:
            user1=User(name=name,user_id=userId,email=email,mobile=mobile,password=passwrd,role='User',photo=photo,otp=otp)
            user1.save()
            #===========Mail
            send_mail(
            'RazzMyBlog Confirm OTP',
            "Good Day !!\n\nWelcome To MyBlog.\nYour OTP is: {} \nPlease Confirm OTP to Use Your account. ".format(otp),
            'prinssingh7448@gmail.com',
            [email],
            fail_silently=False,
               )
            print("Mail Send Success!!")
            #==========
            messages.success(request,"Account Created SuccessFully!!\n Please Check your email For OTP!!")
            return render(request,"main/otp.html",{'id':user1.id,"otp":otp})
        except Exception as e:
            print("Error :",e)
            messages.warning(request,"Please Enter Unique Values!.. The Data You Have Entered Already Exist..!!")     
    return redirect(request.path)
        
def logout(request):
    if 'RazzMyBlog_user_id' in request.session:        
        request.session.pop('RazzMyBlog_user_id')
        if "RazzMyBlog_user_name" in request.session:
            request.session.pop('RazzMyBlog_user_name')
        if "RazzMyBlog_user_photo" in request.session:
            request.session.pop('RazzMyBlog_user_photo')
        messages.info(request,"Logout Successfull!!")
    return redirect(reverse("Blog:index"))

def confirmOTP(request):
    otp=request.POST.get('otp')
    id=request.POST.get('id')
    user=User.objects.filter(id=id).first()
    if otp==user.otp:
        user.otp="Verified"
        user.save()
        messages.success(request,"Account Verified..Please login !!")
        return render(request,"main/Login.html")
    else:
        messages.warning(request,"OTP Dose't Matched !!....Please Enter correct OTP!!")
        return render(request,"main/otp.html",{"id":user.id,"otp":user.otp}) 

def resendOTP(request,email):
    try:
        user=User.objects.filter(email=email).first()
        otp=generateOTP()
        # ===========Mail
        send_mail(
        'RazzMyBlog Confirm OTP',
        "Good Day !!\n\nWelcome To MyBlog.\nYour OTP is: {} \nPlease Confirm OTP to Use Your account. ".format(otp),
        'prinssingh7448@gmail.com',
        [email],
        fail_silently=False,
            )
        print("Mail Send Success!!")
        # ==========
        user.otp=otp
        user.save()
        return HttpResponse("success")
    except:
        return HttpResponse("Email Not Found !!")
   
def forgetPassword(request):    
    email=request.POST.get("email")
    otp=request.POST.get('psw')
    user=User.objects.filter(email=email).first()
    if user.otp==otp:
        user.otp="Verified"
        user.save()
        messages.success(request,"OTP Matched !! Please Reset your password here..")
        return  render(request,"main/resetPassword.html",{'id':user.id})
    else:
        messages.warning(request,"SORRY !! OTP Dosn't  Matched ")
        return redirect(reverse("Blog:Login"))

def resetPassword(request):
    id=request.POST.get('id')
    print("====================",id)
    psw=request.POST.get('psw')
    re_psw=request.POST.get('re_psw')
    if psw == re_psw:
        user=User.objects.get(id=id)
        user.password=psw
        user.save()
        messages.success(request,"Password Reset Success!!...Please login With new Password!!")
        return redirect(reverse("Blog:Login"))
    else:
        messages.warning(request,"Password And Repeat Password Diden't matched!! Try Again!!")
        return redirect(request.path)

def Profile(request):
    if request.method=="GET":
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        return render(request,"main/profile.html",{'user':user})
    if request.method == "POST":
        try :
            id = request.POST.get("id")
            user=User.objects.get(id=id)
            user.name = request.POST.get("name")
            user.user_id = request.POST.get("user_name")
            user.email = request.POST.get("email")
            user.password = request.POST.get("password")
            user.mobile = request.POST.get("mobile")
            user.gender = request.POST.get("gender")
            user.country = request.POST.get("country")
            user.state = request.POST.get("state")
            if 'photo' in request.FILES:
                # Removing Old Pic
                old_pic= request.POST.get("old_pic")
                if json.dumps(str(user.photo))!=old_pic and old_pic!="img/users/default.png" and "prins" not in old_pic:
                    os.remove( str(os.getcwd()) + str("/media/"+old_pic))
                request.FILES['photo'].filename=id
                user.photo=request.FILES['photo']
               

            user.save()
            request.session["RazzMyblog_user_name"]=user.name            
            messages.success(request,"Profile Updated Successfully!!")
        except Exception as e:
            print(e)
            messages.warning(request,'Sorry!! There is Some Error While Updating your Profile!!')
        return redirect(reverse("Blog:Login"))

def commentOnPost(request):
    sub=request.POST.get("subject")
    user_id=request.POST.get("user_id")
    post_id=request.POST.get("post_id")
    pre_request=request.POST.get("pre_request")
    message=request.POST.get("message")
    user=User.objects.get(id=user_id)
    post=Post.objects.get(id=post_id)
    print("==================================================================",request.POST.get("commentid"))
    try:
        if request.POST.get("commentid"):
            comment=Comment.objects.get(id= request.POST.get("commentid"))
            subCom=SubComment(title=sub,content=message,author=user,post=post,parent=comment)
            subCom.save()
        else:
            Com=Comment(title=sub,content=message,author=user,post=post)
            Com.save()
        messages.success(request,"Your Comment Posted SuccessFully!! Thanks For Your Opinion!!")
    except expression as identifier:
        print(identifier)
        messages.warning(request,"Sorry There is Some error while posting your Comment!!")
    return redirect(pre_request)
    
def PostLike(request,uid,pid):
    user=User.objects.get(id=uid)
    post=Post.objects.get(id=pid)
    post.likes.add(user)
    return HttpResponse(post.getLikes())

def PostDisLike(request,uid,pid):
    user=User.objects.get(id=uid)
    post=Post.objects.get(id=pid)
    post.likes.remove(user)
    return HttpResponse(post.getLikes())

def subscribe(request):
    try:
        email=request.GET.get("email")
        sub=Subscribers(email=email)
        sub.save()
        return HttpResponse("success")
    except Exception as e:
        return HttpResponse("error")

def search(request,p=1):
    categories=Category.objects.all()
    Tags=Tag.objects.all()
    data=request.POST.get("data")
    posts=Post.objects.filter(title__icontains=data).filter(status="Approved")
    #==================Pagination=======
    paginator = Paginator(posts,8)
    try:
        posts = paginator.page(p)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    latest_post=Post.objects.order_by('created_on').filter(status="Approved").reverse()[:4]
    popular_posts=Post.objects.order_by('-views').filter(status="Approved")[:4]
    top_stories=Post.objects.filter(id__in=[1,2,3]).filter(status="Approved")
    return render (request,"main/index.html", {'category':categories,'tags':Tags,'top_stories':top_stories,
                           'latest':latest_post,'popular_posts':popular_posts,'posts':posts})