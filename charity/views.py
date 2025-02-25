from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Event, Blog, Comment, Cause, Comment_Cause, Member, Payment, Profile, Project, Volunteer, Collaboration, Personnel
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from . form import CommentForm, CauseCommentForm, SignupForm, CreateProfileForm, CreateProjectForm, VolunteerForm, CollaborationForm, PersonnelForm
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .utils import search_models  
# Create your views here.

def home(request):
    events = Event.objects.all().order_by('-date')[:3]
    blogs = Blog.objects.all().order_by('-id')[:3]
    causes = Cause.objects.all().order_by('raised')[:7]
    projects = Project.objects.all().order_by('amount_raised')[:7]
    causes_total = Cause.objects.all()
    causes_count = Cause.objects.all().count()
    events_count = Event.objects.all().count()
    total = 0
    for p in causes_total:
        amount = p.raised 
        total = total + amount
    context = {'events': events, 'blogs': blogs, 'causes': causes, 'projects': projects, "total": total, 'causes_count': causes_count, 'events_count': events_count}
    return render(request, "home.html", context)


def about(request):
    members = Member.objects.all()
    context = {'members': members}
    return render(request, "about.html", context)

def register(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            obj=form.save()
            login(request, obj, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("create-profile")
    context = {'form': form}
    return render(request, "register.html", context)

@login_required(login_url='login')
def my_profile(request, user):
    user = User.objects.get(username=user)
    profile = Profile.objects.get(user=user)
    context = {'user': user, 'profile': profile}
    return render(request, "profile.html", context)

@login_required(login_url='login')
def create_profile(request):
    form = CreateProfileForm()
    if request.method == 'POST':
        category = request.POST.getlist('category')
        sub_category = request.POST.getlist('sub_category')
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.category =','.join(category)
            obj.sub_category =','.join(sub_category)
            obj.save()
            messages.success(request, 'profile created successfully')
            return redirect('home')
    context = {'form': form}
    return render(request, "create_profile.html", context)

@login_required(login_url='login')
def edit_profile(request, user):
    user = User.objects.get(username=user)
    profile = Profile.objects.get(user=user)
    form = CreateProfileForm(instance=profile)
    if request.method == 'POST':
        category = request.POST.getlist('category')
        sub_category = request.POST.getlist('sub_category')
        form = CreateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.category =','.join(category)
            obj.sub_category =','.join(sub_category)
            obj.save()
            messages.success(request, 'profile updated successfully')
            return redirect('profile', user=user)
    context = {'form': form, "profile": profile}
    return render(request, "edit_profile.html", context)

@login_required(login_url='login')
def create_project(request, user):
    profile = Profile.objects.get(user__username=user)
    form = CreateProjectForm()
    if request.method == 'POST':
        date = request.POST.get('date')
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organization = profile
            obj.date = date
            obj.save()
            messages.success(request, 'project created successfully')
            return redirect('profile', user=user)
    context = {'form': form}
    return render(request, "create_project.html", context)

@login_required(login_url='login')
def create_collaboration(request, slug):
    project = Project.objects.get(slug=slug)
    form = CollaborationForm()
    if request.method == 'POST':
        form = CollaborationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.project = project
            obj.save()
            messages.success(request, 'collaboration created successfully')
            return redirect('home')
    context = {'form': form}
    return render(request, "create_collaboration.html", context)

def projects(request):
    p = Paginator(Project.objects.all().order_by('-date'), 6)
    page = request.GET.get('page')
    projects = p.get_page(page)
    context = {'projects': projects}
    return render(request, "projects.html", context)

def single_project(request, slug):
    project = Project.objects.get(slug=slug)
    projects = Project.objects.all()
    volunteers_number = Volunteer.objects.filter(project=project).count()
    form = VolunteerForm()
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.project = project
            obj.save()
            messages.success(request, "You have become a volunteer")
            return redirect('project', slug=slug)

    context= {"form": form, "project": project, "projects": projects, "volunteers_number": volunteers_number}
    return render(request, "single_project.html", context)

def my_projects(request, user):
    profile = Profile.objects.get(user__username=user)
    project = Project.objects.filter(organization=profile)
    p = Paginator(Project.objects.filter(organization=profile).order_by('-date'), 6)
    page = request.GET.get('page')
    projects = p.get_page(page)
    context = {'projects': projects}
    return render(request, "my_projects.html", context)

def edit_project(request, slug):
    profile = Profile.objects.get(user__username=request.user)
    project = Project.objects.get(slug=slug)
    form = CreateProjectForm(instance=project)
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.organization = profile
            obj.save()
            messages.success(request, "Project updated successfully")
            return redirect('profile', user=request.user)
    context={"form": form}
    return render(request, "edit_project.html", context)
    

def collaboration_requests(request):
    p = Paginator(Collaboration.objects.all().order_by('-id'), 6)
    page = request.GET.get('page')
    collaborations = p.get_page(page)
    context = {'collaborations': collaborations}
    return render(request, "collaboration_requests.html", context)


def collaboration_requests_ngo(request, user):
    p = Paginator(Collaboration.objects.filter(project__organization__user__username=user).order_by('-id'), 6)
    page = request.GET.get('page')
    collaborations = p.get_page(page)
    context = {'collaborations': collaborations}
    return render(request, "collaboration_requests_ngo.html", context)

@login_required(login_url='login')
def collaboration_detail(request, slug):
    collaboration = Collaboration.objects.get(slug=slug)
    collaborations = Collaboration.objects.all()[:4]
    current_personnel = Personnel.objects.filter(collaboration=collaboration).count()
    profile = Profile.objects.get(user__username=request.user)
    ngo_exists = Collaboration.objects.filter(ngos_in_collaboration_with=profile)
    form = PersonnelForm()
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.collaboration = collaboration
            obj.save()
            messages.success(request, "Your request has been received")
            return redirect('collaboration-detail', slug=slug)
    context = {"form": form, "collaboration": collaboration, 'collaborations': collaborations, 'current_personnel': current_personnel, 'ngo_exists': ngo_exists}
    return render(request, "collaboration_detail.html", context)

def edit_collaboration(request, slug):
    collaboration = Collaboration.objects.get(slug=slug)
    form = CollaborationForm(instance=collaboration)
    if request.method == 'POST':
        form = CollaborationForm(request.POST, instance=collaboration)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.project = collaboration.project
            obj.save()
            messages.success(request, "Collaboration updated successfully")
            return redirect('collaboration-detail', slug=slug)
    context = {"form": form}
    return render(request, "edit_collaboration.html", context)

def delete_collaboration(request, slug):
    collaboration = Collaboration.objects.get(slug=slug)
    if request.method == 'POST':
        collaboration.delete()
        messages.success(request, "Collaboration deleted")
        return redirect('home')

@login_required(login_url='login')
def collaborate(request, slug):
    collaboration = Collaboration.objects.get(slug=slug)
    profile = Profile.objects.get(user__username=request.user)
    if request.method == 'POST':
        collaboration.ngos_in_collaboration_with.add(profile)
        messages.success(request, "Collaboration request submitted successfully")
        return redirect('collaboration-detail', slug=slug)

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

def organizations(request): 
    category = request.GET.get('category')
    state = request.GET.get('state')
    organizationss = None
    organizations = None
    
    if category:
        profiles = Profile.objects.filter(category__icontains=category)
        p = Paginator(profiles, 3)
        page = request.GET.get('page')
        organizationss = p.get_page(page)
    else:
        profiles = Profile.objects.all().order_by('-id')
        p = Paginator(profiles, 3)
        page = request.GET.get('page')
        organizations = p.get_page(page)
    
    if state:
        profiles = Profile.objects.filter(state=state)
        p = Paginator(profiles, 3)
        page = request.GET.get('page')
        organizationss = p.get_page(page)
    else:
        profiles = Profile.objects.all().order_by('-id')
        p = Paginator(profiles, 3)
        page = request.GET.get('page')
        organizations = p.get_page(page)
        
    

    # Use `organizationss` if it is set, otherwise use `organizations`
    context = {'organizations': organizationss or organizations, 'profile': profiles, 'selected_category': category, 'selected_state': state}
    
    return render(request, "organizations.html", context)

def organization_detail(request, user):
    organization = Profile.objects.get(user__username=user)
    context = {'organization': organization}
    return render(request, "organization_detail.html", context)

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

def initiate_payment_cause(request, slug):
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
        return render(request, 'make_payment_cause.html', context)

    return render(request, 'payment.html')

def initiate_payment_project(request, slug):
    project = Project.objects.get(slug=slug)
    if request.method == "POST":
        amount = request.POST['amount']
        email = request.POST['email']
        name = request.POST['name']

        pk = settings.PAYSTACK_PUBLIC_KEY

        payment = Payment.objects.create(amount=amount, email=email, project=project, name=name, sub_account_ID=project.organization.sub_account_ID)
        payment.save()

        context = {
            'payment': payment,
            'field_values': request.POST,
            'paystack_pub_key': pk,
            'amount_value': payment.amount_value(),
        }
        return render(request, 'make_payment_project.html', context)

    return render(request, 'payment.html')

def verify_payment_cause(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()
    amount_raised = payment.cause.raised
    if verified:
        cause = payment.cause
        cause.raised += payment.amount  
        cause.save()
        return render(request, "success.html")
    return render(request, "success.html", {"payment": payment})

def verify_payment_project(request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()
    amount_raised = payment.project.amount_raised
    if verified:
        project = payment.project
        project.amount_raised += payment.amount  
        project.save()
        return render(request, "success.html")
    return render(request, "success.html", {"payment": payment})



def search(request):
    query = None
    results = []
    if request.method == 'POST':
        query = request.POST.get('search')
        if query and query.strip():  # Check if query is not empty or just whitespace
            results = search_models(query)
        else:
            print("Empty query submitted.")  # Debug: Handle empty query
    return render(request, 'search.html', {'results': results, 'query': query})