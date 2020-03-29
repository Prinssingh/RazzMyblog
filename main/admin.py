from django.contrib import admin
from .models import *

#Admin View 
admin.site.site_header="RazzMyBlog Admin"

# Register your models here.
admin.site.register(Comment)
admin.site.register(SubComment)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Subscribers)
admin.site.register(Query)
admin.site.register(Prins)