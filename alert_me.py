import smtplib
import yaml
import requests
import json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from time import time, ctime
import click


def send_text(config, subject, body):
    message = MIMEMultipart()
    message['Subject'] = subject
    message.attach(MIMEText(body))

    server = smtplib.SMTP(config['smtp']['server'], int(config['smtp']['port']))
    # Identify client to the SMTP server according to RFC 2821
    server.ehlo()
    # Start TLS session
    server.starttls()
    # Identify client again on the encrypted TLS session
    server.ehlo()
    server.login(str(config['smtp']['email_address']).split('@')[0],
                 config['smtp']['password'])
    server.sendmail(config['smtp']['email_address'],
                    config['message']['alertee'], message.as_string())

    server.quit()


@click.command()
@click.option('--text', is_flag=True, help='It will send a text if required')
@click.argument('config_file_name')
def check_weather(config_file_name, text):
    with open(config_file_name) as configuration_file:
        try:
            config = yaml.safe_load(configuration_file)

            if config['weather']['provider'] == "openweathermap":
                url = "http://api.openweathermap.org/data/2.5/forecast/daily?APPID=" \
                      + config['weather']['app_id'] \
                              + "&id=" + str(config['weather']['city_id']) \
                              + "&cnt=" + str(config['weather']['days']) \
                              + "&units=" + config['weather']['units'] \
                              + "&lang=" + config['weather']['language']
            else:
                print "Unsupported weather provider!"
                return

            req = requests.get(url)
            if req.status_code != 200:
                message = config['message']['failure_text']
                print "{} -> {}".format(message, ctime(time())).encode('UTF-8')
                if text:
                    send_text(config, message.encode('UTF-8'), "")
                return

            content = json.loads(req.text)
            forecast = content['list'][0]
            condition = forecast['weather'][0]
            if condition['main'] == "Rain":
                message = config['message']['rain_text']
                details = condition['description']
                print "{} -> {}".format(message, ctime(time())).encode('UTF-8')
                if text:
                    send_text(config, message.encode('UTF-8'),
                              details.encode('UTF-8'))
                return

            message = config['message']['no_rain_text']
            print "{} -> {}".format(message, ctime(time())).encode('UTF-8')
        except yaml.YAMLError:
            print "Incorrect config file. Please check sample file"
