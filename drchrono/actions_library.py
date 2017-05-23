import time
from django.core.mail import EmailMessage
from drchrono.models import PatientDetails
from django.template import Context
from django.template.loader import get_template


# This is the comparator used for sorting of the Patient objects based on their DOB,
# for Ex: if a patient DOB is 1999-05-23, then the "monthdate" value is 0523, computed this value for all the Patients and sorted based on that.


def comparator(x, y):
    return cmp(x['monthdate'], y['monthdate'])

# This adjust is needed after sorting,
# with this adjust the Patients who's birthdays are completed, are removed from the begining of the list and appended at the end.
# The advantage is we can see the most recent next birthday first.

def adjust(objects):
    t = "".join(time.strftime("%x").split("/"))
    i = 0
    while i < len(objects):
        if cmp(objects[i]['monthdate'], t) < 0:
            temp = objects[i]
            objects.remove(temp)
            objects.append(temp)
        else:
            return objects

# This function is to send the email.

def sendEmail(Greeting, Subject, Email):
    try:
        template = get_template('bdayTemplate.html')
        context = Context({'Greeting': Greeting})
        content = template.render(context)
        email = EmailMessage(Subject, content, 'drchrono.api@gmail.com', [Email])
        email.content_subtype = "html"
        email.send()
        print "Successfully Email Sent!"
    except Exception as e:
        print e
        print "Unable To Send the Email"

# Here we are going to add the scheduled birthdays to the database. They will be sent automatically.

def addToDb(uId, Greeting, Subject, Email, DOB):
    P = PatientDetails()
    P.email = Email
    P.subject = Subject
    P.dob = "-".join(DOB.split("-")[1:3])
    P.greet = Greeting
    P.userId = uId
    P.save()