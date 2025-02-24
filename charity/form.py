from django import forms
from .models import Comment, Comment_Cause, Profile, Project, Volunteer, Collaboration, Personnel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignupForm(UserCreationForm):
    organization_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Organization Name *'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email *'}))
    phone_number = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number *'}))
    class Meta:
        model = User 
        fields = ['organization_name', 'phone_number', 'username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'

        self.fields['username'].widget.attrs['placeholder']= 'Username *'
        self.fields['password1'].widget.attrs['placeholder']= 'Password *'
        self.fields['password2'].widget.attrs['placeholder']= 'Password Again *'

class CommentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Comment.objects.all(), widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment', 'parent']
        widgets = {'parent': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class']= 'form-control'
        self.fields['email'].widget.attrs['class']= 'form-control'
        self.fields['comment'].widget.attrs['class']= 'form-control'

class CauseCommentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Comment_Cause.objects.all(), widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment_Cause
        fields = ['name', 'email', 'comment', 'parent']
        widgets = {'parent': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CauseCommentForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class']= 'form-control'
        self.fields['email'].widget.attrs['class']= 'form-control'
        self.fields['comment'].widget.attrs['class']= 'form-control'

class CreateProfileForm(forms.ModelForm):
    class Meta:
        exclude = ['user', 'category', 'sub_category']
        model = Profile

    def __init__(self, *args, **kwargs):
        super(CreateProfileForm, self).__init__(*args, **kwargs)

        self.fields['organization_name'].widget.attrs['class']= 'form-control'
        self.fields['email'].widget.attrs['class']= 'form-control'
        self.fields['phone_number'].widget.attrs['class']= 'form-control'
        self.fields['description'].widget.attrs['class']= 'form-control'
        self.fields['cac_certificate'].widget.attrs['class']= 'form-control'
        self.fields['cac_number'].widget.attrs['class']= 'form-control'
        self.fields['bank'].widget.attrs['class']= 'form-control'
        self.fields['bank_account_number'].widget.attrs['class']= 'form-control'
        self.fields['bank_account_name'].widget.attrs['class']= 'form-control'
        self.fields['scuml'].widget.attrs['class']= 'form-control'
        self.fields['instagram'].widget.attrs['class']= 'form-control'
        self.fields['twitter'].widget.attrs['class']= 'form-control'
        self.fields['facebook'].widget.attrs['class']= 'form-control'
        self.fields['state'].widget.attrs['class']= 'form-control'
        self.fields['city'].widget.attrs['class']= 'form-control'
        
        self.fields['state'].widget.attrs['placeholder']= 'e.g Federal Capital Territory'
    


class CreateProjectForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'class': 'datetimepicker', 'placeholder': 'Select Date & Time'})
    )
    class Meta:
        exclude = ['organization']
        model = Project

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class']= 'form-control'
        self.fields['budget'].widget.attrs['class']= 'form-control'
        self.fields['description'].widget.attrs['class']= 'form-control'
        self.fields['location'].widget.attrs['class']= 'form-control'
        self.fields['volunteers_needed'].widget.attrs['class']= 'form-control'
        self.fields['schedule'].widget.attrs['class']= 'form-control'
        
    


class VolunteerForm(forms.ModelForm):
    class Meta:
        exclude = ['project']
        model = Volunteer

    def __init__(self, *args, **kwargs):
        super(VolunteerForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class']= 'form-control'
        self.fields['email'].widget.attrs['class']= 'form-control'
        self.fields['phone_number'].widget.attrs['class']= 'form-control'
        self.fields['address'].widget.attrs['class']= 'form-control'
        self.fields['occupation'].widget.attrs['class']= 'form-control'
        
        self.fields['name'].widget.attrs['placeholder']= 'Name*'
        self.fields['email'].widget.attrs['placeholder']= 'Email*'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Phone Number*'
        self.fields['address'].widget.attrs['placeholder']= 'Address*'
        self.fields['occupation'].widget.attrs['placeholder']= 'Occupation*'

class PersonnelForm(forms.ModelForm):
    class Meta:
        exclude = ['collaboration']
        model = Personnel

    def __init__(self, *args, **kwargs):
        super(PersonnelForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class']= 'form-control'
        self.fields['email'].widget.attrs['class']= 'form-control'
        self.fields['phone_number'].widget.attrs['class']= 'form-control'
        self.fields['role'].widget.attrs['class']= 'form-control'
        self.fields['address'].widget.attrs['class']= 'form-control'
        self.fields['occupation'].widget.attrs['class']= 'form-control'
        
        self.fields['name'].widget.attrs['placeholder']= 'Name*'
        self.fields['email'].widget.attrs['placeholder']= 'Email*'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Phone Number*'
        self.fields['role'].widget.attrs['placeholder']= 'Role(E.g Driver, Doctor)*'
        self.fields['address'].widget.attrs['placeholder']= 'Address*'
        self.fields['occupation'].widget.attrs['placeholder']= 'Occupation*'


class CollaborationForm(forms.ModelForm):
    class Meta:
        exclude = ['project', 'ngos_in_collaboration_with']
        model = Collaboration

    def __init__(self, *args, **kwargs):
        super(CollaborationForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class']= 'form-control'
        self.fields['description'].widget.attrs['class']= 'form-control'
        self.fields['resources_needed'].widget.attrs['class']= 'form-control'
        self.fields['personnel_needed'].widget.attrs['class']= 'form-control'
        
        self.fields['title'].widget.attrs['placeholder']= 'Title*'
        self.fields['description'].widget.attrs['placeholder']= 'Describe your collaboration*'
        self.fields['resources_needed'].widget.attrs['placeholder']= 'Resources Needed*'
        self.fields['personnel_needed'].widget.attrs['placeholder']= 'Workers, Drivers, etc*'