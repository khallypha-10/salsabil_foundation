from django.db import models
from django_resized import ResizedImageField
from django.utils.text import slugify
import secrets
from django.utils import timezone
from .paystack  import  Paystack
# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=70)
    message = models.TextField()

class Event(models.Model):
    slug = models.SlugField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=70)
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
    image = ResizedImageField(size=[400, 300], quality=100, crop=['middle', 'center'], upload_to='causes')
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



class Payment(models.Model):
    cause = models.ForeignKey("Cause", on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=70)    
    amount = models.PositiveIntegerField()
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

class Subscribers(models.Model):
    email = models.EmailField(max_length=254)
    class Meta:
        verbose_name_plural = 'Subscribers'