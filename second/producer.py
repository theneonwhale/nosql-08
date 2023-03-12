import connect

from datetime import datetime
import json
import pika
import faker

from models import Contacts

fake = faker.Faker()


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def seed_contacts():
    for user in range(10):
        contact = Contacts(fullname=fake.name(), email=fake.email())
        contact.save()


def main():
    for i, contact in enumerate(Contacts.objects()):
        message = {
            "id": i + 1,
            "payload": str(contact.id),
            "date": datetime.now().isoformat()
        }
        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
        )
        print(f'Email was sent to contact {contact.fullname} with id {contact.id}')
        print(' [x] Sent %r' % message)
    connection.close()


if __name__ == '__main__':
    seed_contacts()
    main()
