from flask import url_for
from projectX import mail
from flask_mail import Message

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
        sender='abdullahomotoke@gmail.com', 
        recipients=[user.email])
    msg.body=f'''
            To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

Thank you
    '''
    mail.send(msg)

def sign_up_message(recipient, name, referalNum):
    msg = Message('Welcome to ProjectX', 
        sender='abdullahomotoke@gmail.com', 
        recipients=[recipient])
    msg.body=f'Hi {name},'
    msg.html=f'''<h4 style='text-align:center; font-family: Lucida Sans'>Welcome to Pointula</h4><br>
    <p>Your referal code is {referalNum}</p>
    <p>Thank You for creating a pointula account.</p>
    <hr><br>
    <center><button style='padding:10px; background:blue; width:90%; margin:auto auto'>Get Started</button></center> <br>
    <p>Welcome to Project X community</p>
    <p>-ProjectX</p>'''
    mail.send(msg)
