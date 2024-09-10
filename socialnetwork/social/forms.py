from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))
    
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
            })
    )
    class Meta:
        model = Post
        fields = ['body']

# class CommentForm(forms.ModelForm):
#     comment = forms.CharField(
#         label='',
#         widget=forms.Textarea(
#             attrs={'rows': '3',
#                    'placeholder': 'Say Something...'}
#         ))

#     class Meta:
#         model = Comment
#         fields = ['comment']
        

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    image = forms.ImageField(required=False)  # إضافة حقل الصورة

    class Meta:
        model = Comment
        fields = ['comment', 'image']


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)

    image = forms.ImageField(required=False)

    class Meta:
        model = MessageModel
        fields = ['body', 'image']

class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
            }))

class ExploreForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder':'Explore tags'
        })
    )

class UserProfileForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'birth_date', 'location', 'picture']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserProfileForm22(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'birth_date', 'location', 'picture']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }



class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)  # إضافة حقل username

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'bio', 'birth_date', 'location', 'picture']

    def clean_username(self):
        # التحقق من أن `username` غير مكرر
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username


