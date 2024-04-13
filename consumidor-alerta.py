import pygame
import time
import pika

def callback(ch, method, properties, body):
    print("Alerta Recebido:", body.decode())
    emitir_beep()
    safety_measure()

def emitir_beep():
    pygame.init()
    pygame.mixer.init()
    beep = pygame.mixer.Sound('beep.mp3')  
    beep.play()
    time.sleep(4)  # Tempo de duração do som (em segundos)
    pygame.mixer.quit()
    pygame.quit()

def safety_measure():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='alerts', exchange_type='topic')
    message = "Acionando controle de segurança!"
    channel.basic_publish(exchange='alerts', routing_key='fire.safetyMeasure', body=message)
    print("Medidas de segurança solicitadas.")
    connection.close()


def consume_alerts():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='alerts', exchange_type='topic')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='alerts', queue=queue_name, routing_key='fire.alerts')
        print('Aguardando alertas...')
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    consume_alerts()
