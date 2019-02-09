from .models import RedditUser, Post, Comment
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm, UserChangeForm
from django.forms import Form, ModelForm
from django.forms.utils import ErrorList


class CustomErrorList(ErrorList):
    def __str__(self):
        return self.as_feedback()

    def as_feedback(self):
        return ''.join(['<div class="invalid-feedback">%s</div>' % e for e in self])

    def as_alert(self):
        return ''.join(['<div class="alert alert-danger">%s</div>' % e for e in self])


class CustomForm(Form):
    def __init__(self, *args, **kwargs):
        if 'error_class' not in kwargs and not len(args) > 5:
            kwargs['error_class'] = CustomErrorList
        super(CustomForm, self).__init__(*args, **kwargs)

        for label, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if label in self.errors:
                field.widget.attrs['class'] += ' is-invalid'


class RedditUserCreationForm(CustomForm, UserCreationForm):
    class Meta:
        model = RedditUser
        fields = ("username", 'phone_number')
        field_classes = {'username': UsernameField}


class AuthForm(CustomForm, AuthenticationForm):
    pass


class EditProfileForm(CustomForm, ModelForm):
    class Meta:
        model = RedditUser
        fields = ['email', 'phone_number', 'about']


class NewPostForm(CustomForm, ModelForm):
    class Meta:
        model = Post
        fields = ['text']
