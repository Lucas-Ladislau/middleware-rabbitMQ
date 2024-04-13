
# Simulação de uma aplicação de IoT para detecção de incêndio

Uma aplicação simples de IoT para simular a detecção de incêndio em um ambiente, utilizando a temperatura da CPU como referência. Usando o RabbitMQ como middleware. 

**INDICADO PARA LINUX**

## Implementações feitas 

- Implementação de um produtor que publica a temperatura da CPU em um tópico do RabbitMQ.
- Implementação de um consumidor que recebe a temperatura da CPU do RabbitMQ e verifica se ela está acima de 50 graus Celsius. Caso a temperatura esteja acima do limite, o consumidor publica uma mensagem em um novo tópico indicando que foi detectado um incêndio.
- Implementação de mais um consumidor para receber a mensagem do tópico de detecção de incêndio e disparar um alarme sonoro, esse efeito sonoro foi disparado usando a biblioteca Pygame.
- Além de disparar o alarme, o consumidro envia uma mensagem para um outro tópico indicando que o sistema de prevenção de incêndio deve ser ativado.




## Como utilizar esta aplicação 

Para rodar a aplicação, rode os seguintes comandos nesta ordem 

```bash
  sudo apt install lm-sensors
```
```bash
  pip install pika
```

```bash
  python3 consumidor-alerta.py
```

```bash
  python3 consumidor_verificacao.py
```

```bash
  python3 produtor-temp.py
```

