import pika
import subprocess
import json
import time

def get_cpu_temperature():
    try:
        output = subprocess.check_output(['sensors']).decode('utf-8')
        cpu_temperature_lines = [line.strip() for line in output.split('\n') if 'Core' in line]
        # Pegando apenas as linhas que contêm a temperatura do núcleo da CPU
        cpu_temperatures = []
        for line in cpu_temperature_lines:
            parts = line.split(':')
            temperature_str = parts[1].split()[0]  # Extrair apenas o valor da temperatura como uma string
            temperature = float(temperature_str[:-2])  # Remover o '°C' e converter para float
            cpu_temperatures.append(temperature)
        return cpu_temperatures
    except (subprocess.CalledProcessError, ValueError):
        return None


def publish_temperature():
    while True:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='temperatures', exchange_type='topic')

        cpu_temperatures = get_cpu_temperature()
        if cpu_temperatures is not None:
            average_temperature = sum(cpu_temperatures) / len(cpu_temperatures)
            message = json.dumps({'temperature': average_temperature})
            channel.basic_publish(exchange='temperatures', routing_key='fire.temperature', body=message)
            print("Temperatura:", average_temperature)
            print("Enviado ao tópico fire.temperaturas")
        else:
            print("Failed to read CPU temperatures.")
        connection.close()
        
        # Espera 10 s antes da próxima execução
        time.sleep(10)

if __name__ == "__main__":
    publish_temperature()
