from Twitter import Tweet
import smtplib
from email.message import EmailMessage
import email
import configparser
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import urllib.request
import base64
from PIL import Image

import imaplib

class Message:
    def __init__(self) -> None:
        self.tweet = Tweet()
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.user = config['message']['user']
        self.pw = config['message']['pw']

        #Set up for requesting messages and commands
        host = 'imap.gmail.com'
        self.mail = imaplib.IMAP4_SSL(host)
        self.mail.login(self.user, self.pw)

        self.mail.select("Inbox")

        self.run = True

    #Sends text messages
    def send_message(self, body, to):
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = self.user

        msg.attach(MIMEText(body))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.user, self.pw)
        server.send_message(msg)

        server.quit()

    #Sends images as JPEG
    def send_file(self, file, to, mime_main, mime_sub):
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = self.user

        contents = urllib.request.urlopen(file).read()
        
        part = MIMEBase(mime_main, mime_sub)
        part.set_payload(contents)
        encoders.encode_base64(part)
    
        msg.attach(part)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.user, self.pw)
        server.sendmail(self.user, to, msg.as_string())

    #Sends tweets
    def tweetMsg(self, to):
        text = self.tweet.get_tweet('tylerperry')
        self.send_message(text[0], to)
        print (text)
        if(text[1] != None):
            self.send_file(text[1], to, 'image', 'jpeg')

    #Get response from user
    def getResponse(self):
        #Check for all 'UNSEEN' Mail 
        _, data = self.mail.search(None, 'UNSEEN')
        if(len(data[0].split()) > 0):
            result, msg = self.mail.fetch(data[0].split()[-1], "(RFC822)")
            message = email.message_from_bytes(msg[0][1])
            
            for part in message.walk():
                if(part.get_content_type() == "text/html"):
                    string = part.as_string()
                    #Returns message user sent and the id the user sent it from
                    return [string[string.index('<td>')+ 5: string.index('</td>')], message.get("From")]
        return [None, None]

    def run_command(self, command, to):
        if any(word in command for word in ['Help', 'help']):
            options = "1. Get Tweet"
            self.send_message(options, to)
        elif any(word in command for word in ['1', 'Tweet', 'tweet']):
            self.tweetMsg(to)
        elif any(word in command for word in ['Exit', 'Quit', 'exit', 'quit']):
            self.run = False
        

if __name__ == "__main__":
    msg = Message()
    while msg.run:
        res = msg.getResponse()
        to = res[1]
        message = res[0]
        if([to, message] != [None, None]):
            msg.run_command(message, to)

    msg.mail.close()
