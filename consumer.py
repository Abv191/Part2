import pika
import json
from models import Contact

# Налаштування RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def send_email_stub(contact):
    print(f'Sending email to {contact.full_name} at {contact.email}')
    # Тут ми імітуємо відправку email
    return True

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    contact = Contact.objects(id=contact_id).first()
    if contact:
        if send_email_stub(contact):
            contact.message_sent = True
            contact.save()
            print(f'Email sent to {contact.full_name} and updated status in DB')
        else:
            print(f'Failed to send email to {contact.full_name}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=False)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
