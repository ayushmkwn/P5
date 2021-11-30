from django import forms
from django.forms.widgets import NumberInput, RadioSelect, Widget

class Registration_Form(forms.Form):
    username = forms.CharField(required=True, max_length=20, label='User Name')
    email = forms.EmailField(required=True, label='Email ID')
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Password')
    cpassword = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirm Password')


class UserInfo_Form(forms.Form):
    birthDate = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), required=True, label='Birth Date')
    mobileNo = forms.CharField(required=True, max_length=10, label='Mobile No')
    gender = forms.ChoiceField(widget=RadioSelect(), choices=[('Male','Male'),('Female', 'Female'), ('Other','Other')], required=True, label='Gender')
    city = forms.CharField(required=True, label='City')
    pincode = forms.CharField(required=True, max_length=6, label='Pincode')
    state = forms.CharField(required=True, label='State')
    image = forms.ImageField(label='Upload an Image')
    file = forms.FileField(label='Upload a Document')