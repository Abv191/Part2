import pika
import json
from faker import Faker
from models import Contact

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

fake = Faker()

def generate_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            extra_info=fake.text()
        )
        contact.save()
        contacts.append(contact)
    return contacts

def send_to_queue(contact):
    message = json.dumps({'contact_id': str(contact.id)})
    channel.basic_publish(exchange='', routing_key='email_queue', body=message)
    print(f'Sent contact {contact.full_name} to queue')

if __name__ == '__main__':
    n = 10
    contacts = generate_contacts(n)
    for contact in contacts:
        send_to_queue(contact)

    connection.close()
