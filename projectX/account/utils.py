from flask import url_for
from projectX import mail
from flask_mail import Message


def withdrawal_request(bank_name, amount, firstname, lastname):
    msg = Message('withdrawal request', 
        sender='abdullahomotoke@gmail.com', 
        recipients=['tokelee@icloud.com'])
    msg.html=f'''<h4 style='text-align:center; font-family: Lucida Sans'>Withdrawal request</h4><br><br>
    <p>Your withdrawal request has been processed and is on the way to your account</p>
    <p>Withdrawal details</p>
    <p>Bank Name: {bank_name}</p>
    <p>Amount: {amount}</p>
    <p>Firstname: {firstname}</p>
    <p>Lastname: {lastname}</p>
    <p>If you think someone else might have initiated this withdrawal please <a href=''>contact us</a> immediately</p>
    <hr><br>
    <center><button style='padding:10px; background:green; width:90%; margin:auto auto'>Get Started</button></center> <br>
    <p>Welcome to Project X community</p>
    <p>-ProjectX</p>'''
    mail.send(msg)

def user_withdrawal_request(recipients,bank_name, amount, firstname, lastname):
    msg = Message('withdrawal request', 
        sender='abdullahomotoke@gmail.com', 
        recipients=[recipients])
    msg.html=f'''<h4 style='text-align:center; font-family: Lucida Sans'>Withdrawal request</h4><br><br>
    <p>Your withdrawal request has been processed and is on the way to your account</p>
    <p>Withdrawal details</p>
    <p>Firstname: {firstname}</p>
    <p>Lastname: {lastname}</p>
    <p>Bank Name: {bank_name}</p>
    <p>Amount: {amount}</p>
    <p>If you think someone else might have initiated this withdrawal please <a href=''>contact us</a> immediately</p>
    <hr><br>
    <center><button style='padding:10px; background:green; width:90%; margin:auto auto'>Get Started</button></center> <br>
    <p>Welcome to Project X community</p>
    <p>-ProjectX</p>'''
    mail.send(msg)

