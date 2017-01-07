import sys
import smtplib
import yaml
import requests
import json
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from time import time, ctime


def send_email(configuration, subject, body):
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
    server.login(str(configuration['smtp']['email_address']).split('@')[0],
                 configuration['smtp']['password'])
    server.sendmail(configuration['smtp']['email_address'],
                    configuration['message']['alertee'], message.as_string())

    server.quit()


def check_weather(configuration):
    if configuration['weather']['provider'] == "openweathermap":
        url = "http://api.openweathermap.org/data/2.5/forecast/daily?APPID=" \
                      + configuration['weather']['app_id'] \
                      + "&id=" + str(configuration['weather']['city_id']) \
                      + "&cnt=" + str(configuration['weather']['days']) \
                      + "&units=" + configuration['weather']['units'] \
                      + "&lang=" + configuration['weather']['language']
    else:
        print "Please specify weather provider in config.yaml"
        return "Fail", ""

    req = requests.get(url)

    if req.status_code != 200:
        return "Fail", ""

    content = json.loads(req.text)
    forecast = content['list'][0]
    condition = forecast['weather'][0]
    if condition['main'] == "Rain":
        return condition['main'], condition['description']

    return "No Rain", ""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Script usage: "
        print "python alert_me.py <config_file>"
        sys.exit()

    # Get the config information
    config_file = open(sys.argv[1])
    config = yaml.safe_load(config_file)
    config_file.close()

    result, detail = check_weather(config)
    if result == "Rain":
        send_email(config, config['message']['text'], detail)
        print "It's going to rain, sent you a text " + str(ctime(time()))
    elif result == "Fail":
        send_email(config, "FAILURE!", "Weather API failed")
        print "Weather API failure " + str(ctime(time()))
    else:
        print "It's not going to rain " + str(ctime(time()))
