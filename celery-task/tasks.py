from __future__ import absolute_import
import celery
import datetime as dt
from drchrono.models import PatientDetails
from drchrono.actions_library import sendEmail

# This module runs the automated sending mail task

@celery.task
def send_bday_mail():
    try:
        dat = dt.datetime.today().strftime("%Y-%m-%d")
        dat = "-".join(dat.split("-")[1:3])

        # get patients having today birthday from the DB

        patients = PatientDetails.objects.filter(dob = dat)
        print "Todays Date: %s" %(dat)
        if len(patients)==0:
            print "No Birthdays Today!"
        else:
            print "Patients having birthday today: "
            for patient in patients:
                print patient

                # Here sending the mail

                sendEmail(patient.greeting, patient.subject, patient.email)
            PatientDetails.objects.filter(dob = dat).delete()
    except Exception as e:
        print e