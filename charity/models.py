from django.db import models
from django_resized import ResizedImageField
from django.utils.text import slugify
import secrets
from django.utils import timezone
from .paystack  import  Paystack
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=70)
    message = models.TextField()

class Event(models.Model):
    slug = models.SlugField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=70)
    location = models.CharField(max_length=70)
    description = models.TextField()
    schedule = models.TextField()
    image_1 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='events')    
    image_2 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='events', blank=True, null=True)    
    image_3 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='events', blank=True, null=True)    
    image_4 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='events', blank=True, null=True)    
    image_5 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='events', blank=True, null=True)    
    image_6 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='events', blank=True, null=True)    
    time = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_account_ID = models.CharField(max_length=50, blank=True, null=True)
    organization_name = models.CharField(max_length=100)
    email = models.EmailField( max_length=254)
    phone_number = PhoneNumberField()
    state = models.CharField(max_length=40)
    city = models.CharField(max_length=20)
    description = models.TextField()
    category = models.TextField()
    sub_category =models.TextField()
    cac_certificate= models.FileField(upload_to='cac', max_length=100)
    scuml= models.FileField(upload_to='scuml', max_length=100)
    cac_number= models.CharField(max_length=50)
    bank_account_name = models.CharField(max_length=200)
    bank_account_number = models.CharField(max_length=10)
    bank = models.CharField(max_length=100)
    organization_image = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='profiles')    
    instagram = models.URLField( max_length=200, blank=True, null=True)
    twitter = models.URLField( max_length=200, blank=True, null=True)
    facebook = models.URLField( max_length=200, blank=True, null=True)

    def __str__(self):
        return self.organization_name
    


class Blog(models.Model):
    
    food = 'Food'
    water = 'Water'
    education = 'Education'
    charity = 'Charity'
    medical_aid = 'Medical Aid'
    category_choices = [
        (food , 'Food'), (water ,'Water'), (education, 'Education'), (charity, 'Charity'), (medical_aid, 'Medical Aid')
    ]
    slug = models.SlugField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=70)
    message = models.TextField()
    image_1 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='blogs')    
    image_2 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='blogs', blank=True, null=True)    
    image_3 = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='blogs', blank=True, null=True)    
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=category_choices)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    @property
    def is_reply(self):
        return self.parent is not None

    class Meta:
        verbose_name_plural = 'Blogs comments'

class Cause(models.Model):
    slug = models.SlugField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=40)
    description = models.TextField()
    image = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='cause')
    goal = models.PositiveIntegerField()
    raised = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def status(self):
        status = (self.raised/self.goal) * 100
        status = int(status)

        return status

    
        

class Comment_Cause(models.Model):
    cause = models.ForeignKey(Cause, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    @property
    def is_reply(self):
        return self.parent is not None

    class Meta:
        verbose_name_plural = 'Causes comments'

class Member(models.Model):
    name = models.CharField(max_length=70)
    title = models.CharField(max_length=40)
    email = models.EmailField(max_length=254)
    image = image = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='member')





class Project(models.Model):
    slug = models.SlugField(max_length=150, blank=True, null=True)
    organization=models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    budget = models.PositiveIntegerField()
    description = models.TextField()
    location = models.CharField(max_length=60)
    volunteers_needed = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    schedule = models.TextField(blank=True, null=True)
    amount_raised = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.organization.organization_name} {self.title} {self.date}")
        super().save(*args, **kwargs)

    def percentage(self):
        return (self.amount_raised/self.budget) * 100

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', args=[str(self.slug)])
        

class Volunteer(models.Model):
    project = models.ForeignKey(Project,  on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField()
    occupation = models.CharField(max_length=50)
    address = models.CharField(max_length=150)


class Collaboration(models.Model):
    slug = models.SlugField(max_length=150, blank=True, null=True)
    project = models.ForeignKey(Project,  on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    resources_needed = models.TextField()
    personnel_needed = models.TextField()
    ngos_in_collaboration_with = models.ManyToManyField(Profile)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.project.title} {self.title} ")
        super().save(*args, **kwargs)

class Personnel(models.Model):
    collaboration = models.ForeignKey(Collaboration,  on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField()
    role = models.CharField(max_length=30)
    occupation = models.CharField(max_length=50)
    address = models.CharField(max_length=150)


class Payment(models.Model):
    cause = models.ForeignKey("Cause", on_delete=models.SET_NULL, blank=True, null=True)
    project = models.ForeignKey("Project", on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=70)    
    amount = models.PositiveIntegerField()
    sub_account_ID = models.CharField(max_length=50, blank=True, null=True)
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: ₦{self.amount} | by {self.name} {self.email}"

    def amount_value(self):
        return int(self.amount) * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)
