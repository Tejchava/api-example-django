# Create your views here.
import requests
import json as simplejson
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from drchrono.forms import ContactForm
from drchrono.actions_library import *

# This is the home page of the application, checks for the authentication.

def home(request):
    if request.user.is_authenticated() == False:
        user = "logged"
    else:
        user = "login"
    return render(request, "index.html", {"user": user, "userName": request.user})

# This is the main page, This processes the login request and also responsible for displaying the user details.

def login(request):

    # Authentication Part

    user = "login"
    if request.user.is_authenticated() == False:
        return render(request, "index.html", {"user": "logged"})
    social = request.user.social_auth.get(provider='drchrono')
    access_token = social.extra_data['access_token']
    headers = {
        'Authorization': 'Bearer %s' %access_token,
    }

    # Using API getiing the Patient details.

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next']

    # Filtering the API results to send only the required ones.

    objects = []
    for patient in patients:
        obj = {}
        obj['name'] = patient['first_name'] + " " + patient['last_name']
        obj['email'] = patient['email'] if patient['email'] != "" else "No Email Id"
        if patient['date_of_birth'] == None:
            obj['dob'] = '1900-01-01'
        else:
            obj['dob'] = patient['date_of_birth']
        dat = obj['dob'].split('-')
        obj['monthdate'] = "".join(dat[1:3]) + dat[0]
        obj['image'] = patient['patient_photo']
        obj['userId'] = patient['id']
        if obj['email'] == "No Email Id" or obj['dob'] == '1900-01-01':
            obj['color'] = "burlywood"
            obj['hover'] = "No Email or DOB, Can't Send a Greeting"
        else:
            try:
                tpatient = PatientDetails.objects.get(userId=obj['userId'])
                obj['color'] = "darkkhaki"
                obj['hover'] = "Greeting was recorded, Send again to update greeting that exist."
            except Exception as e:
                obj['color'] = "white"
                obj['hover'] = "Use the below buttons to send a Greet!"
        objects.append(obj)

    # Sorting those objects based on the month and date values of the Date of birth, Not considered the Year for sorting.

    objects = sorted(objects, cmp = comparator)

    # Adjust is to remove the completed birthdays and add them to the end of the list.

    objects = adjust(objects)
    form_class = ContactForm
    return render(request, "main.html", {'user': user, 'patients': objects, 'form': form_class, "userName": request.user})

# This function is executed when the form is posted.

def greet(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print form['Type'].value()

            # This will send the mail immediately.

            if form['Type'].value()=="now":
                sendEmail(form['Greeting'].value(), form['Subject'].value(), form['Email'].value())

            # This schedules the mail, automatically mail will be sent on the Patient birthday.

            elif form['Type'].value()=="auto":
                addToDb(form['uId'].value(), form['Greeting'].value(), form['Subject'].value(), form['Email'].value(), form['DOB'].value())
            return HttpResponse({})
        else:
            print "Invalid Form"
            errors = form.errors
            return HttpResponse(simplejson.dumps(errors))
    else:
        return HttpResponse("Error in the Request")