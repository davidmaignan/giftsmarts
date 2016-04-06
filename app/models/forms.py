from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField

class ContactForm(Form):
  subject = TextField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")