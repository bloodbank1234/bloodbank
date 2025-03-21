from unittest.mock import inplace
from .chatbot_model import handle_chat_query

from django.shortcuts import render
import Database
import random
from django.core.mail import EmailMultiAlternatives
from BloodBankManagement.settings import DEFAULT_FROM_EMAIL
from django.http import HttpResponse
from datetime import datetime
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import numpy as np
import pickle
import string
import nltk
import urllib.parse




# Create your views here.
def login(request):
    return render(request,'Donor/Login.html')

def Register(request):
    return render(request, 'Donor/Register.html')

def RegAction(request):
    n = request.POST['fullname']
    e = request.POST['email']
    m = request.POST['mobile']
    p = request.POST['password']
    bt = request.POST['blood_type']
    address = request.POST['address']


    con = Database.connect()
    cur1 = con.cursor()
    cur1.execute("select * from donor where email='" + e + "'")
    d = cur1.fetchone()
    if d is not None:
        context = {'msg': 'Email Already Exist..!!'}
        return render(request, 'Donor/Register.html', context)
    else:
        cur = con.cursor()
        otp = str(random.randint(100000, 999999))
        i = cur.execute(
            "insert into donor values(null,'" + n + "','" + e + "','" + m + "','" + p + "','"+otp+"','"+bt+"','"+address+"','waiting')")
        con.commit()
        if i > 0:
            # email settings
            subject = "OTP from BloodBank"
            text_content = ""
            html_content = "<br/><p>OTP :<strong>" + otp + "</strong></p>"
            from_mail = DEFAULT_FROM_EMAIL
            to_mail = [e]
            # if send_mail(subject,message,from_mail,to_mail):
            msg = EmailMultiAlternatives(subject, text_content, from_mail, to_mail)
            msg.attach_alternative(html_content, "text/html")
            if msg.send():
                sts = 'sent'
                print(sts)
            request.session['email']=e
            context = {'msg': 'Registration Successful..!!AND OTP Sent to Mail','name':'register'}
            return render(request, 'Donor/OTPVerify.html', context)
        else:
            context = {'msg': 'Registration Failed..!!'}
            return render(request, 'Donor/Register.html', context)

def LogAction(request):
    e = request.POST['email']
    p = request.POST['password']

    con = Database.connect()
    cur1 = con.cursor()
    cur1.execute("select * from donor where email='" + e + "' and password='"+p+"'")
    d = cur1.fetchone()
    if d is not None:
        status = d[8]
        request.session['id'] = d[0]
        request.session['name'] = d[1]
        request.session['email'] = d[2]
        request.session['mobile'] = d[3]
        request.session['blood_type'] = d[6]

        if status=='waiting':
            context={'msg':'Verify OTP','name':'login'}
            return render(request, 'Donor/OTPVerify.html', context)
        else:
            return render(request, 'Donor/Home.html')
    else:
        context = {'msg': 'Login Failed..!!'}
        return render(request, 'Donor/Login.html', context)

def VerifyAction(request):
    email=request.session['email']
    print(email)
    otp=request.POST['otp']
    a_name=request.POST['a_name']

    con = Database.connect()
    cur1 = con.cursor()
    cur1.execute("select * from donor where email='" + email + "' and otp='" + otp + "'")
    d = cur1.fetchone()
    if d is not None:
        cur2 = con.cursor()
        cur2.execute("update donor set status='Verified' where email='" + email + "' and otp='" + otp + "'")
        con.commit()
        if a_name=='login':
            return render(request, 'Donor/Home.html')
        else:
            context = {'msg': 'Your Verification Successful..!!'}
            return render(request, 'Donor/Register.html', context)
    else:
        context = {'msg': 'Verification Failed..!!'}
        return render(request, 'Donor/OTPVerify.html', context)

def home(request):
    return render(request, 'Donor/Home.html')


def profile(request):
    email=request.session['email']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from donor where email='"+email+"'")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr><th>Full Name</th>"
    table_data += "<th>Email</th>"
    table_data += "<th>Mobile</th>"
    table_data += "<th>Address</th>"
    table_data += "<th>Blood Type</th>"
    table_data += "<th>Update</th></tr>"

    for d in dd:
        table_data += "<tr><td>" + d[1] + "</td>"
        table_data += "<td>" + d[2] + "</td>"
        table_data += "<td>" + d[3] + "</td>"
        table_data += "<td>" + d[7] + "</td>"
        table_data += "<td>" + d[6] + "</td>"
        table_data += "<td><a href=/donor/UpdateProfile?id=" + str(d[0]) + "&mobile=" + str(d[3]) + "&b_type=" + str(d[6]) + ">Update</a></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'Donor/ViewProfile.html', context)

def UpdateProfile(request):
    email = request.session['email']
    id = request.GET['id']
    mobile = request.GET['mobile']
    b_type = request.GET['b_type']

    context={'id':str(id),'mobile':mobile,'b_type':b_type}
    return render(request, 'Donor/UpdateProfile.html', context)

def UpdateAction(request):
    email = request.session['email']
    id = request.POST['d_id']
    mobile = request.POST['mobile']
    blood_type = request.POST['blood_type']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("update donor set mobile='"+mobile+"',blood_type='"+blood_type+"' where id='" + str(id) + "'")
    con.commit()
    cur.execute("select * from donor where email='"+email+"'")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr><th>Full Name</th>"
    table_data += "<th>Email</th>"
    table_data += "<th>Mobile</th>"
    table_data += "<th>Address</th>"
    table_data += "<th>Blood Type</th>"
    table_data += "<th>Update</th></tr>"

    for d in dd:
        table_data += "<tr><td>" + d[1] + "</td>"
        table_data += "<td>" + d[2] + "</td>"
        table_data += "<td>" + d[3] + "</td>"
        table_data += "<td>" + d[7] + "</td>"
        table_data += "<td>" + d[6] + "</td>"
        table_data += "<td><a href=/donor/UpdateProfile?id=" + str(d[0]) + "&mobile=" + str(d[3]) + "&b_type=" + str(d[6]) + ">Update</a></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'Donor/ViewProfile.html', context)


def Request(request):
    con=Database.connect()
    cur = con.cursor()
    cur.execute("select * from hospital")
    data = cur.fetchall()
    str_data = ""
    for d in data:
        print(d)
        str_data += "<option value=" + str(d[0]) + ">" + d[1] + "</option>"
    str_data += ""
    context = {'data': str_data}
    return render(request, 'Donor/DonationRequest.html',context)

def RequestAction(request):
    hsp =request.POST['hsp']
    name = request.POST['name']
    email = request.POST['email']
    disease = request.POST['disease']
    blood_type = request.POST['blood_type']
    b_unites = request.POST['b_unites']
    r_date = request.POST['r_date']
    age = request.POST['age']
    gender = request.POST['gender']

    con = Database.connect()
    cur1 = con.cursor()
    i = cur1.execute("insert into donation_request values(null,'" + hsp + "','" + name + "','" + email + "','" + disease + "','"+blood_type+"','" + b_unites + "','" + r_date + "','Pending','"+age+"','"+gender+"')")
    con.commit()
    if i > 0:
        cur = con.cursor()
        cur.execute("select * from hospital")
        data = cur.fetchall()
        str_data = ""
        for d in data:
            print(d)
            str_data += "<option value=" + str(d[0]) + ">" + d[1] + "</option>"
        str_data += ""
        context = {'msg': 'Request Sent To Hospital Successful..!!','data': str_data}
        return render(request, 'Donor/DonationRequest.html', context)
    else:
        context = {'msg': 'Donation Request Failed..!!'}
        return render(request, 'Donor/DonationRequest.html', context)

def ViewDonations(request):
    email = request.session['email']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from donation_request dr,hospital h where dr.hsp=h.id and dr.email='" + email + "'")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr><th>Hospital Name</th>"
    table_data += "<th>Name</th>"
    table_data += "<th>Email</th>"
    table_data += "<th>Disease</th>"
    table_data += "<th>Blood Group</th>"
    table_data += "<th>Unit</th>"
    table_data += "<th>Request Date</th>"
    table_data += "<th>Status</th></tr>"

    for d in dd:
        table_data += "<tr><td>" + d[12] + "</td>"
        table_data += "<td>" + d[1] + "</td>"
        table_data += "<td>" + d[3] + "</td>"
        table_data += "<td>" + d[4] + "</td>"
        table_data += "<td>" + d[5] + "</td>"
        table_data += "<td>" + d[6] + "</td>"
        table_data += "<td>" + d[7] + "</td>"
        table_data += "<td>" + d[8] + "</td></tr>"
        # table_data += "<td><a href=/deletehsp?id=" + str(d[0]) + ">Delete</a></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'Donor/DonationStatus.html', context)

def chatbot(request):
    return render(request, 'Donor/chatbot.html')




# def ChatAction(request):
#     question = request.GET['mytext']
#     con = Database.connect()
#     cur = con.cursor()
#     cur.execute("select * from faq where question like '%" + question + "%'")
#     data = cur.fetchall()
#     output = ''
#     for tg in data:
#         if question in tg[1]:
#             responses = tg[2]
#             output = responses
#         else:
#             output = "Sorry! I am not trained to answer above question"
#
#     print(question + " " + output)
#     return HttpResponse(output, content_type="text/plain")

MODEL_DIR = "Model"
MODEL_PATH = os.path.join(MODEL_DIR, "chatbot_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# Preprocessing function
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Load Model Function
def load_model():
    with open(MODEL_PATH, "rb") as model_file:
        loaded_model = pickle.load(model_file)
    with open(VECTORIZER_PATH, "rb") as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)
    return loaded_model, loaded_vectorizer

# Chatbot function
def chatbot_response(user_input):
    model, vectorizer = load_model()
    user_input = preprocess(user_input)
    user_vector = vectorizer.transform([user_input])
    prediction = model.predict(user_vector)[0]
    return prediction

def ChatAction(request):
    question = request.GET.get('mytext', '')
    if not question:
        return HttpResponse("Invalid request", content_type="text/plain")

    response = chatbot_response(question)
    return HttpResponse(response, content_type="text/plain")




def ViewAlert(request):

    bt=request.session['blood_type']
    mobile=request.session['mobile']


    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from blood_alert br, hospital h where br.hsp_id=h.id and blood_type='" + bt + "'")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr>"
    table_data += "<th>Hospital</th>"
    table_data += "<th>Requested Blood Group</th>"
    table_data += "<th>Contact</th>"
    table_data += "<th>Description</th>"
    table_data += "<th>Donor Name</th>"
    table_data += "<th>Donor Mobile</th>"
    table_data += "<th>Status</th></tr>"

    for d in dd:
        status = d[7]
        if status == 'Pending':
            table_data += "<tr><td>" + d[9] + "</td>"
            table_data += "<td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><a href=/donor/AcceptRequest?id=" + str(d[0]) + ">Approve</a></td></tr>"
        else:
            table_data += "<tr><td>" + d[9] + "</td>"
            table_data += "<td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><font color='green'>" + d[7] + "</font></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'Donor/ViewAlertStatus.html', context)

def AcceptRequest(request):
    id=str(request.GET['id'])
    name = str(request.session['name'])
    mobile = request.session['mobile']
    print(name)
    print(mobile)

    bt = request.session['blood_type']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("update blood_alert set donor_name='"+name+"',donor_mobile='"+mobile+"',status='Approved' where id='"+id+"'")
    con.commit()
    cur1 = con.cursor()
    cur1.execute("select * from blood_alert br, hospital h where br.hsp_id=h.id and blood_type='" + bt + "'")
    dd = cur1.fetchall()
    table_data = "<table>"
    table_data += "<tr>"
    table_data += "<th>Hospital</th>"
    table_data += "<th>Requested Blood Group</th>"
    table_data += "<th>Contact</th>"
    table_data += "<th>Description</th>"
    table_data += "<th>Donor Name</th>"
    table_data += "<th>Donor Mobile</th>"
    table_data += "<th>Status</th></tr>"

    for d in dd:
        status = d[7]
        if status == 'Pending':
            table_data += "<tr><td>" + d[9] + "</td>"
            table_data += "<td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><a href=/donor/AcceptRequest?id=" + str(d[0]) + ">Approve</a></td></tr>"
        else:
            table_data += "<tr><td>" + d[9] + "</td>"
            table_data += "<td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><font color='green'>" + d[7] + "</font></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'Donor/ViewAlertStatus.html', context)

def Predict(request):
    return render(request, 'Donor/Predict.html')

def PredictAction(request):
    gender =request.POST['gender']
    age = request.POST['age']
    b_type = request.POST['b_type']
    d_units = request.POST['d_units']
    l_date = request.POST['l_date']

    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(l_date, date_format)
    end_date = datetime.now()
    date_difference = start_date - end_date
    days_between_dates = date_difference.days

    print(f"The number of days between {start_date.date()} and {end_date.date()} is {days_between_dates} days.")
    if os.path.exists("Model/blood_donation_model.pkl"):
        loaded_model = joblib.load("Model/blood_donation_model.pkl")
        new_person = np.array(
            [[gender, age, b_type,d_units,days_between_dates]])
        predicted_months = loaded_model.predict(new_person)
        pred_months = int(predicted_months[0])
        print(pred_months)
        print(f'Next eligible donation in {predicted_months[0]:.2f} months')
        context = {'result': f'Next eligible donation in {pred_months} months'}
        return render(request, 'Donor/ViewPrediction.html', context)

    else:
        df = pd.read_csv("Dataset/blood_donation_data.csv")
        df.dropna(inplace=True)
        df['Gender']= df['Gender'].map({'Male':0,'Female':1})
        df['Blood_Type'] = df['Blood_Type'].map({'A+':0, 'A-':1, 'B+':2, 'B-':3, 'AB+':4, 'AB-':5, 'O+':6, 'O-':7})
        df['Donated_Date'] = pd.to_datetime(df['Donated_Date'], format='%Y-%m-%d')
        df['Days_Since_Last_Donation'] = (datetime.today() - df['Donated_Date']).dt.days
        df.drop(columns=['Donated_Date'], inplace=True)

        # Train ML Model
        X = df.drop(columns=['Next_Eligibility_Months'])
        print(X.columns)
        y = df['Next_Eligibility_Months']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save Model
        os.makedirs("Model", exist_ok=True)
        joblib.dump(model, "Model/blood_donation_model.pkl")
        # Predict & Evaluate
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f'MAE: {mae}')
        new_person = np.array(
            [[gender, age, b_type,d_units, days_between_dates]])
        predicted_months = model.predict(new_person)
        pred_months= int(predicted_months[0])
        print(pred_months)
        print(f'Next eligible donation in {predicted_months[0]:.2f} months')
        context = {'result': f'Next eligible donation in {pred_months} months'}
        return render(request, 'Donor/ViewPrediction.html', context)

def chat_action(request):
    """Process chatbot queries and return responses"""
    if request.method == 'GET':
        user_text = request.GET.get('mytext', '')
        response = handle_chat_query(user_text)
        return HttpResponse(response)
    return HttpResponse("Error processing request")