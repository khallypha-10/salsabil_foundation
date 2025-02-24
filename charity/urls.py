from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.home, name="home"),
    path('about-us/', views.about, name="about"),
    path('contact-us/', views.contact, name="contact"),
    path('blogs/', views.blogs, name="blogs"),
    path('organizations/', views.organizations, name="organizations"),
    path('organization-detail/<user>', views.organization_detail, name="organization-detail"),
    path('register/', views.register, name="register"),
    path('create-profile/', views.create_profile, name="create-profile"),
    path('create-project/<user>', views.create_project, name="create-project"),
    path('create-collaboration/<slug>', views.create_collaboration, name="create-collaboration"),
    path('collaborate/<slug>/', views.collaborate, name="collaborate"),
    path('my-profile/<user>', views.my_profile, name="profile"),
    path('edit-profile/<user>', views.edit_profile, name="edit-profile"),
    path('blog/<slug>', views.blog_detail, name="blog"),
    path('events/', views.events, name="events"),
    path('search/', views.search, name="search"),
    path('collaboration-requests/', views.collaboration_requests, name="collaboration-requests"),
    path('collaboration-requests/<user>', views.collaboration_requests_ngo, name="collaboration-requests-ngo"),
    path('collaboration-detail/<slug>', views.collaboration_detail, name="collaboration-detail"),
    path('edit-project/<slug>', views.edit_project, name="edit-project"),
    path('edit-collaboration/<slug>', views.edit_collaboration, name="edit-collaboration"),
    path('delete-collaboration/<slug>', views.delete_collaboration, name="delete-collaboration"),
    path('projects/', views.projects, name="projects"),
    path('my-projects/<user>', views.my_projects, name="my-projects"),
    path('event/<slug>', views.event_single, name="event"),
    path('project/<slug>', views.single_project, name="project"),
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('unlike/<int:blog_id>/', views.unlike_blog, name='unlike_blog'),
    path('causes/', views.causes, name='causes'),
    path('cause/<slug>', views.cause_detail, name="cause"),
    path('initiate-payment-cause/<slug>', views.initiate_payment_cause, name='initiate_payment_cause'),
    path('initiate-payment-project/<slug>', views.initiate_payment_project, name='initiate_payment_project'),
    path('verify-payment-cause/<str:ref>/', views.verify_payment_cause, name='verify_payment_cause'),
    path('verify-payment-project/<str:ref>/', views.verify_payment_project, name='verify_payment_project'),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)