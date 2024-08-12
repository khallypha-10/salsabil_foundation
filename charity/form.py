from django import forms
from .models import Comment, Comment_Cause

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