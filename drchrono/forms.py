from django import forms

# forms go here

# This form is to enter the subject and the Body of the mail.

class ContactForm(forms.Form):
    Type = forms.CharField(required=True, widget=forms.HiddenInput())
    uId = forms.CharField(required=True, widget=forms.HiddenInput())
    Subject = forms.CharField(required=True)
    DOB = forms.CharField(required=True, widget=forms.HiddenInput())
    Email = forms.CharField(required=True, widget=forms.HiddenInput())
    Greeting = forms.CharField(
        required=True,
        widget=forms.Textarea
    )