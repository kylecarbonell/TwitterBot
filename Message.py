from Twitter import Tweet
import smtplib
import email
import configparser
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import urllib.request

import imaplib
import time

import json

class Message:
    def __init__(self) -> None:
        self.tweet = Tweet()
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.username = config['message']['user']
        self.pw = config['message']['pw']

        file = open('Users.json')
        self.users = json.load(file)
        self.recipients = []
        for i in range(len(self.users['Users'])):
            provider = self.users['Users'][i].get('provider')
            number = self.users['Users'][i].get('phone_number')
            print(self.users['Users'][i])
            self.recipients.append(number + self.users['Providers'].get(provider))

        self.run = True



    #Sends text messages
    def send_message(self, body, to):
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = self.username

        msg.attach(MIMEText(body))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.username, self.pw)
        server.sendmail(self.username, to, msg.as_string())

        server.quit()

    #Sends images as JPEG
    def send_file(self, file, to, mime_main, mime_sub):
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = self.username

        contents = urllib.request.urlopen(file).read()
        
        part = MIMEBase(mime_main, mime_sub)
        part.set_payload(contents)
        encoders.encode_base64(part)
    
        msg.attach(part)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.username, self.pw)
        server.sendmail(self.username, to, msg.as_string())

    #Sends tweets
    def tweetMsg(self, to, user):
        text = self.tweet.get_tweet(user)
        self.send_message(text[0], to)
        if(text[1] != None):
            self.send_file(text[1], to, 'image', 'jpeg')

    #Get response from user
    def getResponse(self):
        #Check for all 'UNSEEN' Mail 
        #Set up for requesting messages and commands
        host = 'imap.gmail.com'
        mail = imaplib.IMAP4_SSL(host)
        mail.login(self.username, self.pw)

        mail.select("Inbox")

        _, data = mail.search(None, 'UNSEEN')
        whole_message = data[0].split()
        if(len(whole_message) > 0):
            result, msg = mail.fetch(whole_message[-1], "(RFC822)")
            message = email.message_from_bytes(msg[0][1])
            
            for part in message.walk():
                if(part.get_content_type() == "text/html"):
                    content = part.as_string()
                    #Returns message user sent and the id the user sent it from
                    #Only returns if the sender is subscribed
                    body = content[content.index('<td>')+ 5: content.index('</td>')].strip()
                    sender = message.get("From")

                    mail.close()
                    if(any(word in body for word in ["Subscribe", "subscribe"])):
                        return [body, sender]
                    elif(sender in self.recipients):
                        return [body, sender]
                    else:
                        return ["Please type 'Subscribe' to subscribe to Alert Bot followed by your NAME and your EMAIL (optional) on seperate lines", sender]
        mail.close()
        return [None, None]

    def add_user(self, name, phone_number, email = ''):
        new_user = {'name' : name, 'email' : email, 'phone_number' : phone_number}
        with open('Users.json', 'r+') as js:
            file = json.load(js)
            file['Users'].append(new_user)
            js.seek(0)
            json.dump(file, js, indent=4)
        self.recipients.append(self.users['Users'][-1].get('phone_number') + self.users['Providers'].get(self.users['Users'][-1].get('provider')))

    #Runs commands based on user input from IMsg
    def run_command(self, command, to):
        if any(word in command for word in ['Help', 'help']):
            options = "1. To get the current news \n2. To get a random Tweet\n3. Type @ and a twitter username to get their tweet"
            self.send_message(options, to)
        elif any(word in command for word in ['1', 'News', 'News']):
            self.tweetMsg(to, "CNN")
        elif any(word in command for word in ['2', '@']):
            self.tweetMsg(to, command.partition('@')[2])
        elif any(word in command for word in ['Exit', 'Quit', 'exit', 'quit']):
            self.send_message("Thank you for using Alert Bot! See you next time!", to)
            self.run = False
        elif any(word in command for word in ['Subscribe', 'subscribe']):
            info = command.split("\n")
            print(info)
            self.send_message("Creating your account...", to)
            self.add_user(info[1], info[2], to)
        else:
            self.send_message("Alert bot does not understand this command", to)

#Only run commands to people subscribed
#In response : check if number is subbed, if not type subscribe then enter name and/or email
#Combine phone number and provider into 1 and remove providers list

if __name__ == "__main__":
    msg = Message()
    #msg.add_user("Kyle", "kylecarbonell13@gmail.com", "4025238974", "att")
    #msg.send_message("Alert Bot is now on!", ', '.join(msg.recipients))
    print(msg.recipients)
    time.sleep(3)
    while msg.run:
        time.sleep(3)
        res = msg.getResponse()
        to = res[1]
        message = res[0]
        if([to, message] != [None, None]):
            print(message)
            msg.run_command(message, to)