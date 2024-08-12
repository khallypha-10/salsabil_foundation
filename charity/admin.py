from django.contrib import admin
from .models import Contact, Event, Blog, Comment, Cause, Comment_Cause, Member, Payment, Subscribers
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'subject', 'message']
    search_fields = ['first_name', 'last_name', 'email']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'schedule', 'description', 'time', 'date']
    search_fields = ['name', 'location']
    list_filter = ['time', 'date']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'likes', 'category', 'message', 'date_posted']
    search_fields = ['title']
    list_filter = ['date_posted', 'category']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

@admin.register(Cause)
class CauseAdmin(admin.ModelAdmin):
    list_display = ['title', 'raised', 'goal', 'description']
    search_fields = ['title']

@admin.register(Comment_Cause)
class Comment_CauseAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']

@admin.register(Payment)
class  PaymentAdmin(admin.ModelAdmin):
    list_display  = ["name", "ref", 'amount', "verified", "date_created"]
    list_filter = ["date_created", "verified"]
    search_fields = ["name", "ref", "cause__title" ]

@admin.register(Subscribers)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email']
