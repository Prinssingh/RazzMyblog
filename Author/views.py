from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib import messages
from django.template.defaultfilters import slugify
from main.models import *
import json
import os
# Create your views here.
from datetime import datetime
def index(request):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')

    subs=Subscribers.objects.all()
    visit= request.session["RazzMyBlog_visits"]
    users=User.objects.all()
    data={"subscribers":subs,"Users":users,"visit":visit}
    posts=Post.objects.filter(author=user)
    comments=Comment.objects.filter(post__in=posts)
    subcomments=SubComment.objects.filter(post__in=posts)
    return  render(request,'Author/Author.html',{'admin_data':data,'comments':comments,'subcomments':subcomments})

def Profile(request):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
            return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    if request.method == 'GET':
        id= request.session["RazzMyBlog_user_id"]
        user=User.objects.filter(id=id).first()
        return render (request,'Author/Profile.html',{'user':user})
    if request.method=="POST":
        id = request.POST.get("id")
        user=User.objects.get(id=id)
        user.name=request.POST.get("name")
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
                user.photo=request.FILES['photo']
        
        user.save()
        request.session['RazzMyBlog_user_photo'] =user.photo.url
        request.session['RazzMyBlog_user_name'] =user.name      
        messages.success(request, 'Profile Updated Successfully!!')
        return redirect(reverse("Author:Profile"))

def newBlog(request):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    if request.method == 'GET':
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return  render (request,'Author/newBlog.html',{'category':categories,'tags':tags})
        
    if request.method== 'POST':
        try:
            title = request.POST.get('blog_title')
            categories = request.POST.getlist('categories')
            tags = request.POST.getlist('tags')
            content = request.POST.get('content')
            photo = request.FILES['blog_image']
            id = request.session["RazzMyBlog_user_id"]
            AUTHOR=User.objects.get(id=id)
            post1 = Post(image=photo, title=title, slug=slugify(title),content=content,author=AUTHOR,created_on=datetime.now(),updated_on=datetime.now())
            post1.save()
            
            for cat in categories:
                cate=Category.objects.filter(id=cat).first()
                cate.posts.add(post1)
            
            for tag in tags:
                tag1=Tag.objects.filter(id=tag).first()
                tag1.posts.add(post1)
            messages.success(request, 'Post Added Successfully!!')
            return redirect(reverse("Author:NewBlog"))
        except expression as identifier:
            print(identifier)
            return redirect(reverse("Author:NewBlog"))

def Personal_Blogs(request):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    if request.method == 'GET':
        posts=Post.objects.filter(author=user).order_by('-created_on')[:10]
        comments=Comment.objects.filter(post__in=posts)
        subcomments=SubComment.objects.filter(post__in=posts)
        return render (request,'Author/Table.html',{'posts':posts,'comments':comments,'subcomments':subcomments})

def editBlog(request,id):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    if request.method == 'GET':
        post=Post.objects.get(id=id)
        if post.author!=user:
             return  render(request,'Author/404.html')
        categories = Category.objects.all()
        tags = Tag.objects.all()
        pcid=post.categories.all()
        post_cat_id=[x.id for x in pcid ]
        ptid=post.tags.all()
        post_tag_id=[x.id for x in ptid ]
        return render (request,'Author/Editblog.html',{'post':post,'category':categories,'tags':tags,"pcid":post_cat_id,'ptid':post_tag_id})
    if request.method=="POST":
        post=Post.objects.get(id=id)
        post.title = request.POST.get('blog_title')
        post.slug=slugify(request.POST.get('blog_title'))
        if 'blog_image' in  request.FILES :
            old_pic= request.POST.get("old_pic")
            if json.dumps(str(user.photo))!=old_pic and  "post" not in old_pic:
                os.remove( str(os.getcwd()) + str("/media/"+old_pic))
            post.image=request.FILES['blog_image']
        post.content=request.POST.get('content')
        Auth_id = request.session["RazzMyBlog_user_id"]
        post.author=User.objects.get(id=Auth_id)
        post.status="Submitted"
        post.save()
        # clear old relationships
        post.categories.clear()
        post.tags.clear()

        categories = request.POST.getlist('categories')
        tags = request.POST.getlist('tags') 
        # Adding New relationships
        for cat in categories:
            cate=Category.objects.filter(id=cat).first()
            cate.posts.add(post)                
        for tag in tags:
            tag1=Tag.objects.filter(id=tag).first()
            tag1.posts.add(post)
        
        messages.success(request, 'Post Updated Successfully!!')
        
        return redirect (reverse("Author:Personal_Blogs"))
  
def deletePost(request,id):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    post=Post.objects.get(id=id)
    if post.author!=user:
             return  render(request,'Author/404.html')
    post.delete()
    return redirect (reverse("Author:Personal_Blogs"))

def approveComment(request,id,t='c'):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    if t == "c":
        comment=Comment.objects.get(id=id)
        comment.status="Approved"
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    elif t == "s":
        comment=SubComment.objects.get(id=id)
        comment.status="Approved"
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return  render(request,'Author/404.html')

def pendingComment(request,id,t='c'):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    if t == "c":
        comment=Comment.objects.get(id=id)
        comment.status="Pending"
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    elif t == "s":
        comment=SubComment.objects.get(id=id)
        comment.status="Pending"
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return  render(request,'Author/404.html')

def rejectComment(request,id,t='c'):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    if t == "c":
        comment=Comment.objects.get(id=id)
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    elif t == "s":
        comment=SubComment.objects.get(id=id)
        comment.status="Rejected"
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return  render(request,'Author/404.html')

def getDataByDate(request):
    try:
        user=User.objects.get(id=request.session["RazzMyBlog_user_id"])
        if user.role=="User" :
                return  render(request,'Author/404.html')
    except:
        return  render(request,'Author/404.html')
    
    posts=Post.objects.filter(author=user)
    dpost=posts.filter(created_on__month=1,created_on__year=2020,created_on__day=30)
    print(dpost)
    return HttpResponse(dpost)




    