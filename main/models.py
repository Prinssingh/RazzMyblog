from django.db import models

User_Roles=[('User',"User"),
            ('Developer','Developer'),
            ('Admin','Admin'),
            ('Author','Author')]

Status=[('Pending','Pending'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('Submitted','Submitted')]
SOLUTION=[('Pending','Pending'),
          ('Evaluating','Evaluating'),
          ('Given','Given'),
          ('Submitted',"Submitted") ]
Gender=[('Male','Male'),('Female','Female'),('Select','Select')]

# Create your models here.

class User(models.Model):
    name= models.CharField(max_length=100,null=False)
    user_id =models.CharField(max_length=50,unique=True,null=False)
    email = models.CharField(max_length=70, unique=True, null=False)
    mobile = models.CharField(max_length=15, unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    gender = models.CharField(max_length=12,choices=Gender,default='Select')
    country =models.CharField(max_length=50,default='India')
    state = models.CharField(max_length=50,default="Madhya Pradesh")
    role = models.CharField(max_length=20,choices=User_Roles,default='User')
    otp = models.CharField(max_length=12,default="Not Verified")
    photo=models.ImageField(upload_to='main/Users',default='main/Users/default.png')
    
    def __repr__(self):
        return f"{self.id}:{self.name}"
    def __str__(self):
        return self.name


class Post(models.Model):
    image= models.ImageField(upload_to='main/Posts')
    title=models.CharField(max_length=300, unique=True, null=False)
    slug =models.SlugField( max_length=120,unique=True, null=False)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User,related_name='liked')
    views=models.IntegerField(default=0,null=True)
    status= models.CharField(max_length=200,choices=Status,default='Submitted')
    #user post relationship
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted',null=True)    

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title)
    def __str__(self):
        return "{}\t\t:\t\t {}".format(self.title,self.status)
    def getLikes(self):
        return len(self.likes.all())  

        
class Comment(models.Model):
    title=models.CharField(max_length=300, null=False)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status= models.CharField(max_length=30,choices=Status,default='Submitted')
    #user comments on
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_on',null=True)
    # Post and comment relationship
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews', null=True)

    def __repr__(self):
        return f"{self.id}:{self.title}"
    def __str__(self):
        return "{}\t\t:\t\t {}".format(self.title,self.status)
    
class SubComment(models.Model):
    title=models.CharField(max_length=300, null=False)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status= models.CharField(max_length=30,choices=Status,default='Submitted')
    # user subcomments on
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='sub_comment_on',null=True)
     # Post and subcomment relationship
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='sub_reviews',null=True)
    parent=models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='child',null=True)

    def __repr__(self):
        return f"{self.id}:{self.title}"
    def __str__(self):
        return "{}\t\t:\t\t {}".format(self.title,self.status)

class Category(models.Model):
    name=models.CharField(max_length=120, unique=True, null=False)
    slug = models.SlugField( max_length=120,unique=True, null=False)
    # M2M relation For Category and Post
    posts =models.ManyToManyField(Post,related_name='categories')

    def __repr__(self):
         return f"{self.id}:{self.name}"
    def __str__(self):
        return self.name
    def ApprovedPostCount(self):
        return len(self.posts.filter(status="Approved"))

class Tag(models.Model):

    name=models.CharField(max_length=50, unique=True, null=False)
    slug = models.SlugField( max_length=120,unique=True, null=False)
    posts =models.ManyToManyField(Post,related_name='tags')

    def __repr__(self):
         return f"{self.id}:{self.name}"
    def __str__(self):
        return self.name
    

class Subscribers(models.Model):
    email = models.EmailField(max_length=100,unique=True)

    def __str__(self):
        return self.email
    

class Query(models.Model):
    name= models.CharField(max_length=100,null=False)
    email = models.EmailField(max_length=100,unique=True)
    title=models.CharField(max_length=300,null=False)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    solution = models.TextField(null=True)
    status= models.CharField(max_length=30,choices=SOLUTION,default='Submitted')
    def __repr__(self):
        return f"{self.title}:{self.status}"

    def __str__(self):
        return "{}\t\t:\t\t {}".format(self.title,self.status)
    

class Prins(models.Model):
    name= models.CharField(max_length=100,null=False)
    email = models.EmailField(max_length=100,unique=True)
    title=models.CharField(max_length=300, unique=True, null=False)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=30,choices=SOLUTION, default='Submitted')

    def __repr__(self):
        return f"{self.title}:{self.ststus}"
    def __str__(self):
        return "{}\t\t:\t\t {}".format(self.title,self.status)
    
'''u=User(name='Prins Singh',user_id='Prinssingh',password='Prins123@',email='prinssingh7448@gmail.com',mobile='9981282308',gender=0,role=1,otp='Verified')
u.save()'''
