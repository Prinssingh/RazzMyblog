from django import template
from main.models import *
register = template.Library()
        
@register.filter(name="isLiked")
def isLiked(value,id):
    user=User.objects.filter(id=id)
    if user in value.likes.all():
        return True
    else: 
        return False

@register.filter(name="ApprovedLen")
def ApprovedLen(value):
    data = value.filter(status="Approved")
    return len(data)

@register.filter(name="PendingLen")
def PendingLen(value):
    data = value.filter(status="Pending")
    return len(data)

@register.filter(name="SubmittedLen")
def SubmittedLen(value):
    data = value.filter(status="Submitted")
    return len(data)

@register.filter(name="Submitted")
def Submitted(value):
    data=value.filter(status="Submitted")
    return data

@register.filter(name="Pending")
def Pending(value):
    data=value.filter(status="Pending")
    return data

@register.filter(name="Approved")
def Approved(value):
    data=value.filter(status="Approved")
    return data

@register.filter(name="TopPost")
def TopPost(value):
    data=value.order_by('likes').first()
    if data:
        return data.title,data.getLikes(),data.views
    else:
        return None 

@register.filter(name="index")
def indexval(value,index):
    return value[int(index)]
