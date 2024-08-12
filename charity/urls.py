from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('home/', views.home, name="home"),
    path('about-us/', views.about, name="about"),
    path('contact-us/', views.contact, name="contact"),
    path('subscribe/', views.subscribers, name="subscribe"),
    path('blogs/', views.blogs, name="blogs"),
    path('blog/<slug>', views.blog_detail, name="blog"),
    path('events/', views.events, name="events"),
    path('event/<slug>', views.event_single, name="event"),
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('unlike/<int:blog_id>/', views.unlike_blog, name='unlike_blog'),
    path('causes/', views.causes, name='causes'),
    path('cause/<slug>', views.cause_detail, name="cause"),
    path('initiate-payment/<slug>', views.initiate_payment, name='initiate_payment'),
    path('verify-payment/<str:ref>/', views.verify_payment, name='verify_payment'),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)