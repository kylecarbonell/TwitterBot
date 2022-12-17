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

class Message:
    def __init__(self) -> None:
        self.tweet = Tweet()
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.user = config['message']['user']
        self.pw = config['message']['pw']

    def send_message(self, body, to):
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = self.user

        msg.attach(MIMEText(body))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.user, self.pw)
        server.send_message(msg)

        server.quit()

    def send_file(self, file, to, mime_main, mime_sub):
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = self.user

        with open(file, "rb") as pic:
            part = MIMEBase(mime_main, mime_sub)
            part.set_payload(pic.read)
            encoders.encode_base64(part)
        
            msg.attach(part)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.user, self.pw)
        server.sendmail(self.user, to, msg.as_string())

    def tweetMsg(self, to):
        text = self.tweet.get_tweet('tylerperry')
        self.send_message(text[0], to)
        if(text[1] != None):
            self.send_file(text[1], to, 'image', 'jpeg')

    # def getResponse(self):
    #     host = 'imap.gmail.com'
        
    #     mail = imaplib.IMAP4_SSL(host)
    #     mail.login(self.user, self.pw)

    #     mail.select("inbox")

    #     result, data = mail.uid('search', None, "ALL")
    #     inbox = data[0].split()
    #     newest = inbox[-1]

    #     email_msg = mail.uid('fetch', newest, "(RFC822)")
    #     msg = email_msg[1][0][1].decode("utf-8")
    #     txt = email.message_from_string(msg)
    #     print(txt.get_payload(decode=True))

#USE MMS TO SEND NON FORMATTED TEXTS

#This works now


if __name__ == "__main__":
    msg = Message()
    #msg.alert("HElo ’ he",'4088588974@mms.att.net')
    msg.tweetMsg("kylecarbonell13@gmail.com")
    #msg.tweetMsg('4088588974@mms.att.net')
