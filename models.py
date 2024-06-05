from mongoengine import Document, StringField, BooleanField, connect

connect('contacts_db')

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
    extra_info = StringField() 
