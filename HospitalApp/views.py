from django.shortcuts import render
import Database
import random,string
from django.core.mail import EmailMultiAlternatives
from BloodBankManagement.settings import DEFAULT_FROM_EMAIL

# Create your views here.
def login(request):
    return render(request,'Hospital/Login.html')
def Register(request):
    return render(request,'Hospital/Register.html')
def generate_password():
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(characters, k=6))

def RegAction(request):
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
        return render(request, 'Hospital/Register.html', context)
    else:
        cur.execute(
            "insert into hospital values(null,'" + name + "','" + contact + "','" + email + "','" + address + "','" + password + "','Pending')")
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
        return render(request, 'Hospital/Register.html', context)

def home(request):
    return render(request,'Hospital/HospitalHome.html')


def LogAction(request):
    e = request.POST['email']
    p = request.POST['password']

    con = Database.connect()
    cur1 = con.cursor()
    cur1.execute("select * from hospital where email='" + e + "' and password='"+p+"'")
    d = cur1.fetchone()
    if d is not None:
        status = d[6]
        if status == 'Pending':
            context = {'msg': 'Your account is still pending at Admin. please check after 24hrs..!!'}
            return render(request, 'Hospital/Login.html', context)
        else:
            request.session['id'] = d[0]
            request.session['name'] = d[1]
            request.session['email'] = d[3]

            return render(request, 'Hospital/HospitalHome.html')

    else:
        context = {'msg': 'Login Failed..!!'}
        return render(request, 'Hospital/Login.html', context)


def DonorRequest(request):
    id=request.session['id']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from donation_request where hsp='" + str(id) + "'")
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
        if status =='Pending':
            table_data += "<tr><td>" + d[2] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[9] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td>" + d[7] + "</td>"
            table_data += "<td><a href=/hsp/AcceptDonation?id=" + str(d[0]) + "&bg="+str(d[5])+"&unit="+d[6]+">Approve</a> OR <a href=/hsp/RejectDonation?id=" + str(d[0]) + ">Reject</a></td></tr>"
        elif status =='Rejected':
            table_data += "<tr><td>" + d[2] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[9] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td>" + d[7] + "</td>"
            table_data += "<td><font color='red'>"+ d[8] +"</font></td></tr>"
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
    return render(request, 'Hospital/DonationStatus.html', context)


def AcceptDonation(request):
    did=request.GET['id']
    bg = request.GET['bg']
    unit = request.GET['unit']

    id = request.session['id']
    con = Database.connect()
    cur1 = con.cursor()
    cur1.execute("update donation_request set status='Approved' where id='" + str(did) + "'")
    con.commit()
    cur12 = con.cursor()
    cur12.execute("select count(*) from total_units")
    t=cur12.fetchone()
    print(t)
    if t[0]==0:
        cur = con.cursor()
        cur.execute("insert into total_units values(null,'"+str(bg)+"','"+unit+"')")
        con.commit()
    else:
        curr=con.cursor()
        curr.execute("select * from total_units where blood_group='"+str(bg)+"'")
        ttt=curr.fetchall()
        t_u=0
        for tt in ttt:
            t_u=int(tt[2])+int(unit);

        cur2 = con.cursor()
        cur2.execute("update total_units set no_of_units='"+str(t_u)+"' where blood_group='"+bg+"'")
        con.commit()


    cur = con.cursor()
    cur.execute("select * from donation_request where hsp='" + str(id) + "'")
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
            table_data += "<td><a href=/hsp/AcceptDonation?id=" + str(
                d[0]) + "&bg="+str(d[5])+"&unit="+d[6]+">Approve</a> OR <a href=/hsp/RejectDonation?id=" + str(d[0]) + ">Reject</a></td></tr>"
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
    return render(request, 'Hospital/DonationStatus.html', context)


def RejectDonation(request):
    did=request.GET['id']

    id = request.session['id']
    con = Database.connect()
    cur1 = con.cursor()
    cur1.execute("update donation_request set status='Rejected' where id='" + str(did) + "'")
    con.commit()
    cur = con.cursor()
    cur.execute("select * from donation_request where hsp='" + str(id) + "'")
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
            table_data += "<td><a href=/hsp/AcceptDonation?id=" + str(
                d[0]) + "&bg="+d[5]+"&unit="+d[6]+">Approve</a> OR <a href=/hsp/RejectDonation?id=" + str(d[0]) + ">Reject</a></td></tr>"
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
    return render(request, 'Hospital/DonationStatus.html', context)

def Request(request):

    id = request.session['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from patient_request where hsp_id='" + str(id) + "'")
    dd = cur.fetchall()
    table_data = ""

    for d in dd:
        status = d[6]
        if status == 'Pending':
            table_data+="<div class='col-md-4'>"
            table_data+="<div class='blood-request-card'>"
            table_data+="<h4>Request ID:"+str(d[0])+"</h4>"
            table_data+="<p>Patient Name: "+d[3]+"</p>"
            table_data+="<p>Blood Group: "+d[2]+"</p>"
            table_data+="<p class='status pending'>Status: <a href=/hsp/AcceptRequest?id=" + str(d[0]) + ">Approve</a> OR <a href=/hsp/RejectRequest?id=" + str(
                d[0]) + ">Reject</a></p>"
            table_data+="</div>"
            table_data+="</div>"

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
    return render(request, 'Hospital/BloodRequest.html', context)

def AcceptRequest(request):
    rid=str(request.GET['id'])

    id = request.session['id']
    con=Database.connect()
    curr=con.cursor()
    curr.execute("update patient_request set status='Approved' where id='"+rid+"'")
    con.commit()
    cur = con.cursor()
    cur.execute("select * from patient_request where hsp_id='" + str(id) + "'")
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
            table_data += "<p class='status pending'>Status: <a href=/hsp/AcceptRequest?id=" + str(
                d[0]) + ">Approve</a> OR <a href=/hsp/RejectRequest?id=" + str(
                d[0]) + ">Reject</a></p>"
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
    return render(request, 'Hospital/BloodRequest.html', context)

def RejectRequest(request):
    rid = str(request.GET['id'])

    id = request.session['id']
    con = Database.connect()
    curr = con.cursor()
    curr.execute("update patient_request set status='Rejected' where id='" + rid + "'")
    con.commit()
    cur = con.cursor()
    cur.execute("select * from patient_request where hsp_id='" + str(id) + "'")
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
            table_data += "<p class='status pending'>Status: <a href=/hsp/AcceptRequest?id=" + str(
                d[0]) + ">Approve</a> OR <a href=/hsp/RejectRequest?id=" + str(
                d[0]) + ">Reject</a></p>"
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
    return render(request, 'Hospital/BloodRequest.html', context)

def UrgentRequest(request):
    return render(request, 'Hospital/UrgentRequest.html')

def RequestAlertAction(request):
    hsp_id = request.POST['hsp_id']
    blood_type = request.POST['blood_type']
    contact = request.POST['contact']
    desc = request.POST['desc']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from donation_request where hsp='"+str(hsp_id)+"'")
    data = cur.fetchall()
    name=request.session['name']

    for dd in data:
        # email settings
        subject = "BLOOD REQUIREMENT ALERT FROM "+name
        text_content = ""
        html_content = "<br/><p>Hospital Name :</strong>" + name + "</strong></p><br><p>Blood Type :<strong>" + blood_type + "</strong></p>\
        <br><p>contact :<strong>" + contact + "</strong></p><br><p>Description :<strong>" + desc + "</strong></p>"
        from_mail = DEFAULT_FROM_EMAIL
        to_mail = [dd[3]]
        # if send_mail(subject,message,from_mail,to_mail):
        msg = EmailMultiAlternatives(subject, text_content, from_mail, to_mail)
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            sts = 'sent'
            print(sts)
    cur1 = con.cursor()
    cur1.execute("insert into blood_alert values(null,'"+hsp_id+"','"+blood_type+"','"+contact+"','"+desc+"','waiting','waiting','Pending')")
    con.commit()
    context = {'msg': "Alert Generated Successfully...!!"}
    return render(request, 'Hospital/UrgentRequest.html', context)

def AlertStatus(request):
    id = request.session['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from blood_alert where hsp_id='" + str(id) + "'")
    dd = cur.fetchall()
    table_data = "<table>"
    table_data += "<tr>"
    table_data += "<th>Requested Blood Group</th>"
    table_data += "<th>Contact</th>"
    table_data += "<th>Description</th>"
    table_data += "<th>Donor Name</th>"
    table_data += "<th>Donor Mobile</th>"
    table_data += "<th>Status</th></tr>"

    for d in dd:
        status = d[7]
        if status == 'Pending':
            table_data += "<tr><td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><font color='orange'>" + d[7] + "</font></td></tr>"
        else:
            table_data += "<tr><td>" + d[2] + "</td>"
            table_data += "<td>" + d[3] + "</td>"
            table_data += "<td>" + d[4] + "</td>"
            table_data += "<td>" + d[5] + "</td>"
            table_data += "<td>" + d[6] + "</td>"
            table_data += "<td><font color='green'>" + d[7] + "</font></td></tr>"

    table_data += "</table>"
    context = {'table_data': table_data}
    return render(request, 'Hospital/ViewAlertStatus.html', context)
