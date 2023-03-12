import connect

import pika
import json

from models import Contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f"Message was received on channel {ch} by method {method} with properties {properties} and body {body}")

    message = json.loads(body.decode())
    print(f" [x] Received {message}")

    contact = Contacts.objects(id=message.get('payload'))
    contact.update(delivered=True)

    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
