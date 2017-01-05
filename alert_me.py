import sys
import smtplib
import yaml
import requests
import json
from email import MIMEMultipart
from email import MIMEText
import time


def send_email(configuration, message):
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

if __name__ == '__main__':
    # Get the config information
    config_file = open(sys.argv[1])
    config = yaml.safe_load(config_file)
    config_file.close()

    request_url = ""
    if config['weather']['provider'] == 'openweathermap':
        request_url = "http://api.openweathermap.org/data/2.5/forecast/daily?APPID=" \
                      + config['weather']['app_id'] \
                      + "&id=" + str(config['weather']['city_id']) \
                      + "&cnt=" + str(config['weather']['days']) \
                      + "&units=" + config['weather']['units'] \
                      + "&lang=" + config['weather']['language']
    else:
        print "Please specify weather provider in config.yaml"

    req = requests.get(request_url)
    msg = MIMEMultipart()
    if req.status_code != 200:
        msg['Subject'] = "FAILURE!"
        text = "Weather API failed"
        msg.attach(MIMEText(text))
        send_email(config, msg)
        print "Weather API failure " + str(time.time())
    else:
        content = json.loads(req.text)
        forecast = content['list'][0]
        condition = forecast['weather'][0]
        # Only send email if it's gonna rain
        if condition['main'] == 'Rain':
            msg['Subject'] = config['message']['text']
            text = condition['description']
            msg.attach(MIMEText(text))
            send_email(config, msg)
        print "It's going to rain, sent you an email " + str(time.time())

    print "It's not going to rain " + str(time.time())
