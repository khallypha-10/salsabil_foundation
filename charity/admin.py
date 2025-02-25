from django.contrib import admin
from .models import Contact, Event, Blog, Comment, Cause, Comment_Cause, Member, Payment, Profile, Project, Volunteer, Collaboration, Personnel
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'subject', 'message']
    search_fields = ['first_name', 'last_name', 'email']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'schedule', 'description', 'time', 'date']
    search_fields = ['title', 'location']
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
    list_display  = ["name", "ref", 'amount', "verified", "date_created", "sub_account_ID"]
    list_filter = ["date_created", "verified"]
    search_fields = ["name", "ref", "cause__title", "sub_account_ID" ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user__username', 'organization_name', 'category', 'sub_category', 'email', 'phone_number']
    search_fields = ['user__username', 'organization_name', 'email', 'category', 'sub_category', 'phone_number']
    list_filter=['category']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['organization__organization_name', 'title', 'budget', 'amount_raised', 'location', 'date']    
    list_filter=['date']
    search_fields=['organization__organization_name', 'title', 'location',]


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'address']
    search_fields = ['name', 'email', 'phone_number']

@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display=['project__title', 'title', 'description']
    search_fields= ['project__title', 'title', 'profile__organization_name']

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'phone_number', 'address']
    search_fields = ['name', 'email', 'phone_number']