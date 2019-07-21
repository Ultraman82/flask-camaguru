import os
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
mail.init_app(app)
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_DEFAULT_SENDER": os.environ['EMAIL_USER'],
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}

print(mail_settings)
app.config.update(mail_settings)

message = "<form action='http://localhost:5000/verify/%s' method='post'><input type='submit' value='Submit'></input></form>" % "df"
#message = "<a href=    'http://localhost:5000/verify/%s'>Click here to verify" % username    
msg = Message(subject="dsg",
                recipients="jaridiruhi@mail-click.net",
                body=message)
mail.send(msg)
