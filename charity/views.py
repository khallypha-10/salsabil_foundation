from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Event, Blog, Comment, Cause, Comment_Cause, Member, Payment, Subscribers
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from . form import CommentForm, CauseCommentForm
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
# Create your views here.

def home(request):
    events = Event.objects.all().order_by('-date')[:3]
    blogs = Blog.objects.all().order_by('-id')[:3]
    causes = Cause.objects.all().order_by('raised')[:7]
    causes_total = Cause.objects.all()
    causes_count = Cause.objects.all().count()
    events_count = Event.objects.all().count()
    total = 0
    for p in causes_total:
        amount = p.raised 
        total = total + amount
    context = {'events': events, 'blogs': blogs, 'causes': causes, "total": total, 'causes_count': causes_count, 'events_count': events_count}
    return render(request, "home.html", context)

def subscribers(request):
    if request.method == 'POST':
        sub_name = request.POST['sub']
        sub = Subscribers(email=sub_name)
        sub.save()
        messages.success(request, 'You have subscribed!')
        return redirect('home')
    return render(request, "base.html")

def about(request):
    members = Member.objects.all()
    context = {'members': members}
    return render(request, "about.html", context)

def contact(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['lastname']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = Contact(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
        contact.save()
        send_mail(
                subject,
                message,
                "sabilcharityfoundation@gmail.com",
                ["sabilcharityfoundation@gmail.com"],
                fail_silently=False,
            )
        
        messages.success(request, 'Your message was received. We will get back to you shortly')
        return redirect("home")
    return render(request, "contact.html")

def events(request):
    p = Paginator(Event.objects.all().order_by('-date'), 6)
    page = request.GET.get('page')
    events = p.get_page(page)
    context = {'events': events}
    return render(request, "events.html", context)

def event_single(request, slug):
    event = Event.objects.get(slug=slug)
    events = Event.objects.all().order_by('-date')[:5]
    context = {'event': event, 'events': events}
    return render(request, "event-single.html", context)

def blogs(request): 
    category = request.GET.get('category')
    blogss = None
    blogs = None
    
    if category:
        blog_list = Blog.objects.filter(category=category)
        p = Paginator(blog_list, 3)
        page = request.GET.get('page')
        blogss = p.get_page(page)
    else:
        blog_list = Blog.objects.all().order_by('-id')
        p = Paginator(blog_list, 3)
        page = request.GET.get('page')
        blogs = p.get_page(page)
        
    blog = Blog.objects.all().order_by('-id')[:5]

    # Use `blogss` if it is set, otherwise use `blogs`
    context = {'blogs': blogss or blogs, 'blog': blog, 'blog_list': blog_list, 'selected_category': category}
    
    return render(request, "blogs.html", context)

def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.likes += 1
    blog.save()
    return JsonResponse({'likes': blog.likes})

def unlike_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.likes > 0:
        blog.likes -= 1
        blog.save()
    return JsonResponse({'likes': blog.likes})



def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    blogs = Blog.objects.all().order_by('-id')[:5]
    comments = blog.comments.filter(parent__isnull=True).order_by('-created_at')
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            obj = comment_form.save(commit=False)
            obj.blog = blog
            parent_id = request.POST['parent']
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                obj.parent = parent_comment
            obj.save()
            return redirect('blog', slug=blog.slug)
    

    context = {
        'blog': blog,
        'blogs': blogs,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'blog-single.html', context)


def causes(request):
    p = Paginator(Cause.objects.all().order_by('raised'), 6)
    page = request.GET.get('page')
    causes = p.get_page(page)
    context = {'causes': causes}
    return render(request, "causes.html", context)    


def cause_detail(request, slug):
    cause = Cause.objects.get(slug=slug)
    causes = Cause.objects.all().order_by('-id')[:5]
    comments = cause.comments.filter(parent__isnull=True).order_by('-created_at')
    comment_form = CauseCommentForm()

    if request.method == 'POST':
        comment_form = CauseCommentForm(request.POST)
        if comment_form.is_valid():
            obj = comment_form.save(commit=False)
            obj.cause = cause
            parent_id = request.POST['parent']
            if parent_id:
                parent_comment = Comment_Cause.objects.get(id=parent_id)
                obj.parent = parent_comment
            obj.save()
            return redirect('cause', slug=cause.slug)
    

    context = {
        'cause': cause,
        'causes': causes,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'causes-single.html', context)

def initiate_payment(request, slug):
    cause = Cause.objects.get(slug=slug)
    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']
        name = request.POST['name']

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, cause=cause, name=name)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
        }
        return render(request, 'make_payment.html', context)

    return render(request, 'payment.html')

def verify_payment(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()
    amount_raised = payment.cause.raised
    if verified:
        cause = payment.cause
        cause.raised += payment.amount  
        cause.save()
        return render(request, "success.html")
    return render(request, "success.html")