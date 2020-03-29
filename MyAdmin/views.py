from django.shortcuts import render,HttpResponse,redirect
from main.models import *

# Create your views here.

def index(request):
    return render (request,"MyAdmin/index.html")

def tables(request):
    allUsers=User.objects.all()
    authors=allUsers.filter(role="Author")
    users=allUsers.filter(role="User")
    posts=Post.objects.all()
    categories=Category.objects.all()
    tags=Tag.objects.all()
    subscribers=Subscribers.objects.all()
    comments=Comment.objects.all()
    subcomments=SubComment.objects.all()
    queries=Query.objects.all()

    data={"authors":authors,"users":users,"posts":posts,"categories":categories,"tags":tags,
    "subscribers":subscribers,"comments":comments,"subcomments":subcomments,"queries":queries}
    return render(request,"MyAdmin/DataTables.html",data)


def preview(request):
    id=request.GET.get("id")
    post=Post.objects.get(id=id)
    tagged=post.tags.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    latest_post=Post.objects.order_by('created_on').filter(status="Approved").reverse()[:4]
    popular_posts=Post.objects.order_by('-views').filter(status="Approved")[:4]
    return render(request,"MyAdmin/blogDetails.html",{"post":post,"tagged":tagged,"category":categories,'latest':latest_post,'popular_posts':popular_posts,"tags":tags})


def delfunction(request):
    id= request.GET.get('id')
    type= request.GET.get('type')
    print("id:",id,"type:",type)
    if type=="User":
        User.objects.get(id=id).delete()
    
    return HttpResponse("Success")

def updateUser(request):
    id= request.GET.get('id')
    type= request.GET.get('type')
    print("id:",id,"type:",type)
    if type=="Demote":
        user=User.objects.get(id=id)
        user.role="User"
        user.save()
    if type=="Promote":
        user=User.objects.get(id=id)
        user.role="Author"
        user.save()
    return HttpResponse("Success")


def messageAuthor(request):
    id= request.GET.get('id')
    title= request.GET.get('title')
    body= request.GET.get('body')
    print("=============================================",id,title,body)
    return HttpResponse("Success")

