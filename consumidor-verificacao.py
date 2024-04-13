import pika
import json

def callback(ch, method, properties, body):
    temperature_data = json.loads(body)
    temperature = temperature_data['temperature']
    if temperature > 45:
        print("Incêndio detectado! Temperatura:", temperature)
        publish_fire_alert()

def publish_fire_alert():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='alerts', exchange_type='topic')
    message = "Tá pegando fogo bicho!"
    channel.basic_publish(exchange='alerts', routing_key='fire.alerts', body=message)
    print("Alerta de incêndio publicado.")
    connection.close()

def consume_temperature():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='temperatures', exchange_type='topic')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='temperatures', queue=queue_name, routing_key='fire.temperature')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print('Aguardando as temperaturas...')
    channel.start_consuming()

if __name__ == "__main__":
    consume_temperature()
