import smtplib
import yaml
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

if __name__ == '__main__':

    #Get the config information about SMTP Server
    config_file = open('config.yaml')
    config = yaml.safe_load(config_file)
    config_file.close()

    msg = MIMEMultipart()
    msg['Subject'] = config['message']['text']
    if config['message']['deets'] == 'CHANCE':
        text = '90% CHANCE'
        msg.attach(MIMEText(text))
    elif config['message']['deets'] == 'TEMP':
        text = '70 degrees'
        msg.attach(MIMEText(text))

    server = smtplib.SMTP(config['smtp']['server'], int(config['smtp']['port']))
    #Identify client to the SMTP server according to RFC 2821
    server.ehlo()
    #Start TLS session
    server.starttls()
    #Identify client again on the encrypted TLS session
    server.ehlo()
    server.login(str(config['smtp']['email_address']).split('@')[0],
                 config['smtp']['password'])
    server.sendmail(config['smtp']['email_address'],
                    config['message']['alertee'], msg.as_string())

    server.quit()
