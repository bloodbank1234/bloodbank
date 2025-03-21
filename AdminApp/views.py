import contextlib

from django.shortcuts import render
import Database
import random
import string
from django.core.mail import EmailMultiAlternatives
from BloodBankManagement.settings import DEFAULT_FROM_EMAIL
from urllib.parse import unquote
import pandas as pd
import os
import pickle
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'AdminApp/Login.html')

def LogAction(request):
    if request.method=='POST':
        uname=request.POST['username']
        pwd=request.POST['password']

        if uname == 'Admin' and pwd == 'Admin':
            con=Database.connect()
            cur=con.cursor()
            cur.execute("select distinct blood_type  from donation_request")
            aa=cur.fetchall()
            b_data = ""
            for a in aa:
                bg=a[0]
                cur = con.cursor()
                cur.execute("select count(blood_type) from donation_request where blood_type='"+bg+"'")
                aaa = cur.fetchall()
                for ab in aaa:
                    bg_acount=ab[0]
                    b_data+="<div class='col-md-3'>"
                    b_data+="<div class='card'>"
                    b_data+="<div class='card-icon text-danger'>"
                    b_data+=bg+" <i class='bi bi-droplet-fill'></i>"
                    b_data+="</div>"
                    b_data+="<div>"+str(bg_acount)+"</div>"
                    b_data+="</div>"
                    b_data+="</div>"
            b_data += ""

            curr = con.cursor()
            curr.execute("select count(*) from donation_request")
            td = curr.fetchone()
            total_donor=""
            if td is not None:
                to_donor=td[0]
                total_donor+=" <div class='col-md-3'>"
                total_donor+="<div class='card'>"
                total_donor+="<div class='card-icon text-primary'>"
                total_donor+="Total Donors <i class='bi bi-people-fill'></i>"
                total_donor+="</div>"
                total_donor+="<div>"+str(to_donor)+"</div>"
                total_donor+="</div>"
                total_donor+="</div>"

            cur3 = con.cursor()
            cur3.execute("select count(*) from patient_request")
            tdd = cur3.fetchone()
            if tdd is not None:
                to_req = tdd[0]
                total_donor += " <div class='col-md-3'>"
                total_donor += "<div class='card'>"
                total_donor += "<div class='card-icon text-primary'>"
                total_donor += "Total Requests <i class='bi bi-clipboard-data'></i>"
                total_donor += "</div>"
                total_donor += "<div>" + str(to_req) + "</div>"
                total_donor += "</div>"
                total_donor += "</div>"

            cur1 = con.cursor()
            cur1.execute("select count(*) from patient_request where status='Approved'")
            td1 = cur1.fetchone()
            if td1 is not None:
                to_req_a = td1[0]
                total_donor += " <div class='col-md-3'>"
                total_donor += "<div class='card'>"
                total_donor += "<div class='card-icon text-success'>"
                total_donor += "Approved Requests <i class='bi bi-check-circle-fill'></i>"
                total_donor += "</div>"
                total_donor += "<div>" + str(to_req_a) + "</div>"
                total_donor += "</div>"
                total_donor += "</div>"

            cur12 = con.cursor()
            cur12.execute("select sum(no_of_units) from total_units")
            td12 = cur12.fetchone()
            if td12 is not None:
                to_units = int(td12[0])
                total_donor += " <div class='col-md-3'>"
                total_donor += "<div class='card'>"
                total_donor += "<div class='card-icon text-info'>"
                total_donor += "Total Blood Unit (ml) <i class='bi bi-droplet'></i>"
                total_donor += "</div>"
                total_donor += "<div>" + str(to_units) + "</div>"
                total_donor += "</div>"
                total_donor += "</div>"

            total_donor+=""


            context={"b_data":b_data,"total_donor":total_donor}
            return render(request,'AdminApp/AdminHome.html',context)
        else:
            context={'msg':'Login Failed..!!'}
            return render(request,'AdminApp/Login.html', context)

def home(request):
    return render(request,'AdminApp/AdminHome.html')


def AddHsp(request):
    return render(request,'AdminApp/AddHsp.html')

def generate_password():
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(characters, k=6))

def AddHspAction(request):
    name = request.POST['name']
    email = request.POST['email']
    contact = request.POST['contact']
    address = request.POST['address']
    con = Database.connect()
    cur = con.cursor()
    password = generate_password()

    cur.execute("select count(*) from hospital where name='" + name + "' and address='" + address + "'")
    d = cur.fetchone()
    print(d)
    if int(d[0]) > 0:
        context = {'msg': 'Hospital Name Already Exist...!!'}
        return render(request, 'AdminApp/AddHsp.html', context)
    else:
        cur.execute("insert into hospital values(null,'" + name + "','" + contact + "','"+email+"','"+address+"','"+password+"')")
        con.commit()

        # email settings
        subject = "LOGIN CREDENTIALS"
        text_content = ""
        html_content = "<br/><p>USERNAME :<strong>" + email + "</strong></p><br><p>PASSWORD :<strong>" + password + "</strong></p>"
        from_mail = DEFAULT_FROM_EMAIL
        to_mail = [email]
        # if send_mail(subject,message,from_mail,to_mail):
        msg = EmailMultiAlternatives(subject, text_content, from_mail, to_mail)
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            sts = 'sent'
            print(sts)


        context = {'msg': 'Hospital Name Added Successfully...!! AND Login Credentials Sent to Mail'}
        return render(request, 'AdminApp/AddHsp.html', context)

def ViewHsp(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from hospital")
    dd = cur.fetchall()
    table_data="<table>"
    table_data+="<tr><th>Hospital Name</th>"
    table_data+="<th>Hospital Contact</th>"
    table_data += "<th>Hospital Email</th>"
    table_data += "<th>Hospital Address</th>"
    table_data += "<th>Account Status</th>"
    table_data += "<th>Action</th></tr>"

    for d in dd:
        status = d[6]
        if status == 'Pending':
            table_data += "<tr><td>"+d[1]+"</td>"
            table_data += "<td>"+d[2]+"</td>"
            table_data += "<td>"+d[3]+"</td>"
            table_data += "<td>"+d[4]+"</td>"
            table_data += "<td><a href=/Accepthsp?id=" + str(d[0]) + ">Pending</a></td>"
            table_data += "<td><a href=/deletehsp?id=" + str(d[0]) + ">Delete</a></td></tr>"
        else:
            table_data += "<tr><td>" + d[1] + "</td>"
            table_data += "<td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><a href=/deletehsp?id=" + str(d[0]) + ">Delete</a></td></tr>"

    table_data+="</table>"
    context={'table_data':table_data}
    return render(request, 'AdminApp/ViewHsp.html', context)
def Accepthsp(request):
    id = request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("update hospital set status='Authorized' where id='" + str(id) + "'")
    con.commit()

    cur.execute("select * from hospital")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr><th>Hospital Name</th>"
    table_data += "<th>Hospital Contact</th>"
    table_data += "<th>Hospital Email</th>"
    table_data += "<th>Hospital Address</th>"
    table_data += "<th>Account Status</th>"
    table_data += "<th>Action</th></tr>"

    for d in dd:
        status = d[6]
        if status == 'Pending':
            table_data += "<tr><td>" + d[1] + "</td>"
            table_data += "<td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td><a href=/Accepthsp?id=" + str(d[0]) + ">Pending</a></td>"
            table_data += "<td><a href=/deletehsp?id=" + str(d[0]) + ">Delete</a></td></tr>"
        else:
            table_data += "<tr><td>" + d[1] + "</td>"
            table_data += "<td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><a href=/deletehsp?id=" + str(d[0]) + ">Delete</a></td></tr>"


    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'AdminApp/ViewHsp.html', context)
def deletehsp(request):
    id = request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("delete  from hospital where id='" + str(id) + "'")
    con.commit()

    cur.execute("select * from hospital")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr><th>Hospital Name</th>"
    table_data += "<th>Hospital Contact</th>"
    table_data += "<th>Hospital Email</th>"
    table_data += "<th>Hospital Address</th>"
    table_data += "<th>Action</th></tr>"

    for d in dd:
        table_data += "<tr><td>" + d[1] + "</td>"
        table_data += "<td>" + d[2] + "</td>"
        table_data += "<td>" + d[3] + "</td>"
        table_data += "<td>" + d[4] + "</td>"
        table_data += "<td><a href=/deletehsp?id=" + str(d[0]) + ">Delete</a></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'AdminApp/ViewHsp.html', context)

def search(request):
    return render(request,'Search.html')

def SearchAction(request):
    location=request.POST['location']
    blood_type=request.POST['blood_type']

    con = Database.connect()
    cur=con.cursor()
    cur.execute("select * from hospital where address like '%"+location+"%'")
    dd = cur.fetchall()

    table_data = "<table>"
    table_data += "<tr><th>Hospital Name</th>"
    table_data += "<th>Donor Name</th>"
    table_data += "<th>Donor Email</th>"
    table_data += "<th>Last Donation</th>"
    table_data += "<th>Blood Group</th>"
    table_data += "<th>Blood Request</th></tr>"

    for d in dd:
        iid=d[0]
        curr=con.cursor()
        curr.execute("select * from donation_request where hsp='"+str(iid)+"' and blood_type='"+blood_type+"'")
        ddd=curr.fetchall()

        for dd in ddd:
            table_data += "<tr><td>" + d[1] + "</td>"
            table_data += "<td>" + dd[2] + "</td>"
            table_data += "<td>" + dd[3] + "</td>"
            table_data += "<td>" + dd[7] + "</td>"
            table_data += "<td>" + dd[5] + "</td>"
            table_data += "<td><a href=/RequestForBlood?hsp_id=" + str(iid) + "&group="+dd[5]+">Request</a></td>"


    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'ViewResult.html', context)

def RequestForBlood(request):
    hsp_id=request.GET['hsp_id']
    group = request.GET['group']

    context = {'hsp_id': hsp_id,'group':group}
    return render(request, 'RequestBlood.html', context)

def RequestAction(request):
    hsp_id = request.POST['hsp_id']
    patient_name = request.POST['patient_name']
    blood_type = request.POST['blood_type']
    contact = request.POST['contact']
    address = request.POST['address']

    con = Database.connect()
    cur1 = con.cursor()
    i = cur1.execute(
        "insert into patient_request values(null,'" + hsp_id + "','" + blood_type + "','" + patient_name + "','" + contact + "','" + address + "','Pending')")
    con.commit()
    if i > 0:
        context = {'msg': 'Request Sent To Hospital Successful..!!'}
        return render(request, 'RequestBlood.html', context)
    else:
        context = {'msg': 'Request Failed..!!'}
        return render(request, 'RequestBlood.html', context)

def BRequestStatus(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from patient_request ")
    dd = cur.fetchall()
    table_data = ""

    for d in dd:
        status = d[6]
        if status == 'Pending':
            table_data += "<div class='col-md-4'>"
            table_data += "<div class='blood-request-card'>"
            table_data += "<h4>Request ID:" + str(d[0]) + "</h4>"
            table_data += "<p>Patient Name: " + d[3] + "</p>"
            table_data += "<p>Blood Group: " + d[2] + "</p>"
            table_data += "<p class='status pending'>Status: <font color='yellow'>" + d[6] + "</font></p>"
            table_data += "</div>"
            table_data += "</div>"

        elif status == 'Rejected':
            table_data += "<div class='col-md-4'>"
            table_data += "<div class='blood-request-card'>"
            table_data += "<h4>Request ID:" + str(d[0]) + "</h4>"
            table_data += "<p>Patient Name: " + d[3] + "</p>"
            table_data += "<p>Blood Group: " + d[2] + "</p>"
            table_data += "<p class='status pending'>Status: <font color='red'>" + d[6] + "</font></p>"
            table_data += "</div>"
            table_data += "</div>"

        else:
            table_data += "<div class='col-md-4'>"
            table_data += "<div class='blood-request-card'>"
            table_data += "<h4>Request ID:" + str(d[0]) + "</h4>"
            table_data += "<p>Patient Name: " + d[3] + "</p>"
            table_data += "<p>Blood Group: " + d[2] + "</p>"
            table_data += "<p class='status pending'>Status: <font color='green'>" + d[6] + "</font></p>"
            table_data += "</div>"
            table_data += "</div>"

    table_data += ""
    context = {'table_data': table_data}
    return render(request, 'AdminApp/BloodRequest.html', context)

def donorlist(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from donation_request")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr>"
    table_data += "<th>Donor Name</th>"
    table_data += "<th>Disease</th>"
    table_data += "<th>Age</th>"
    table_data += "<th>Blood Group</th>"
    table_data += "<th>Unit</th>"
    table_data += "<th>Request Date</th>"
    table_data += "<th>Status</th></tr>"

    for d in dd:
        status = d[8]
        if status == 'Pending':
            table_data += "<tr><td>" + d[2] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[9] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td>" + d[7] + "</td>"
            table_data += "<td><font color='yellow'>" + d[8] + "</font></td></tr>"
        elif status == 'Rejected':
            table_data += "<tr><td>" + d[2] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[9] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td>" + d[7] + "</td>"
            table_data += "<td><font color='red'>" + d[8] + "</font></td></tr>"
        else:
            table_data += "<tr><td>" + d[2] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[9] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td>" + d[7] + "</td>"
            table_data += "<td><font color='green'>" + d[8] + "</font></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'AdminApp/DonorList.html', context)

# def ADDFAQ(request):
#     return render(request, 'AdminApp/AddFAQ.html')

# def AddFAQAction(request):
#     question = request.POST['question']
#     ans = request.POST['answer']
#
#     con = Database.connect()
#     cur = con.cursor()
#     cur.execute("select count(*) from faq where question='" + question + "'")
#     d = cur.fetchone()
#     print(d)
#     if int(d[0]) > 0:
#         context = {'msg': 'Question Already Exist...!!'}
#         return render(request, 'AdminApp/AddFAQ.html', context)
#     else:
#         cur.execute(
#             "insert into faq values(null,'" + question + "','" + ans + "')")
#         con.commit()
#
#         context = {'msg': 'Question Added Successfully...!!'}
#         return render(request, 'AdminApp/AddFAQ.html', context)


# Preprocessing function
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def BotModel(request):
    MODEL_DIR = "Model"
    os.makedirs(MODEL_DIR, exist_ok=True)
    MODEL_PATH = os.path.join(MODEL_DIR, "chatbot_model.pkl")
    VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

    # Load dataset
    df = pd.read_csv("Dataset/dataset.csv")
    questions = df["Question"].tolist()
    answers = df["Answer"].tolist()

    # Preprocess all questions
    questions_processed = [preprocess(q) for q in questions]

    # Vectorization using TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(questions_processed)
    y = answers

    # Train Naïve Bayes Model
    model = MultinomialNB()
    model.fit(X, y)

    # Save model and vectorizer
    with open(MODEL_PATH, "wb") as model_file:
        pickle.dump(model, model_file)
    with open(VECTORIZER_PATH, "wb") as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

    context = {'msg': 'Chatbot Model Successfully Generated...!!'}
    return render(request, 'AdminApp/ModelResult.html', context)

def feedback(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from hospital")
    data = cur.fetchall()
    str_data = ""
    for d in data:
        print(d)
        str_data += "<option value=" + str(d[0]) + ">" + d[1] + "</option>"
    str_data += ""
    context = {'data': str_data}
    return render(request, 'FeedBack.html', context)

def FeedbackAction(request):
    hsp = request.POST['hsp']
    email = request.POST['email']
    mobile = request.POST['mobile']
    date = request.POST['date']
    service = request.POST['service']
    request_handle = request.POST['request_handle']
    desc = request.POST['desc']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("insert into feedback values(null,'" + hsp + "','" + email + "','" + mobile + "','" + date + "','" + service + "','" + request_handle + "','"+desc+"')")
    con.commit()

    context = {'msg': 'Feedback Submitted Successfully...!!'}
    return render(request, 'FeedBack.html', context)

def ViewFeedback(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from feedback")
    dd = cur.fetchall()

    table_data = "<table>"
    table_data += "<tr><th>Hospital ID</th>"
    table_data += "<th>Email</th>"
    table_data += "<th>Mobile</th>"
    table_data += "<th>Date of Feedback</th>"
    table_data += "<th>Overall Service</th>"
    table_data += "<th>Request Handling</th>"
    table_data += "<th>Description</th></tr>"

    for d in dd:
        table_data += "<tr><td>" + d[1] + "</td>"
        table_data += "<td>" + d[2] + "</td>"
        table_data += "<td>" + d[3] + "</td>"
        table_data += "<td>" + d[4] + "</td>"
        table_data += "<td>" + d[5] + "</td>"
        table_data += "<td>" + d[6] + "</td>"
        table_data += "<td>" + d[7] + "</td></tr>"


    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'AdminApp/ViewFeedback.html', context)