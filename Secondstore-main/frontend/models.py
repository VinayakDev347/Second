from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    mob = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    img = models.ImageField(upload_to="uimage",blank=True,null=True)

    def __str__(self):
        return f"{self.name}"

class Messages(models.Model):
    description = models.TextField()
    sender_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)


class Friends(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"

class adsdb(models.Model):
    pname = models.CharField(max_length=100,null=True,blank=True)
    bname = models.CharField(max_length=100,null=True,blank=True)
    category = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    details = models.CharField(max_length=300,null=True,blank=True)
    time = models.CharField(max_length=300,null=True,blank=True)
    uname = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to="images",null=True,blank=True)
    image1 = models.ImageField(upload_to="images",null=True,blank=True)
    image2 = models.ImageField(upload_to="images",null=True,blank=True)

class contactdb(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    sub = models.CharField(max_length=100,null=True,blank=True)
    msg = models.CharField(max_length=200,null=True,blank=True)

class wishlistdb(models.Model):
    pid = models.IntegerField(null=True,blank=True)
    user = models.CharField(max_length=100,null=True,blank=True)
    pname = models.CharField(max_length=100,null=True,blank=True)
    bname = models.CharField(max_length=100,null=True,blank=True)
    category = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    details = models.CharField(max_length=300,null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    uname = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to="images",null=True,blank=True)
    image1 = models.ImageField(upload_to="images",null=True,blank=True)
    image2 = models.ImageField(upload_to="images",null=True,blank=True)