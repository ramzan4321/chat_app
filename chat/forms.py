from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from chat.models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
        super(UserRegisterForm, self).clean()
        
        # getting username and password from cleaned_data
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # validating the username and password
        if len(username) < 5:
            self._errors['username'] = self.error_class(['A minimum of 5 characters is required'])

        if len(password1) < 8:
            self._errors['password1'] = self.error_class(['Password length should not be less than 8 characters'])
            
        if password1 != password2 :
            self._errors['password1'] = self.error_class(['Password DOES NOT match with password1'])
            return self.cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class GroupForm(forms.Form):
    users = User.objects.all()
    lst = []
    for x in users:
            lst.append([x.username, x.username])

    tuple_of_tuples = tuple(tuple(inner_list) for inner_list in lst)

    OPTIONS = tuple_of_tuples

    group_users = forms.MultipleChoiceField(choices=OPTIONS, widget=forms.SelectMultiple)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'dob', 'profile_image']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
