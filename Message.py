from Twitter import Tweet
import smtplib
from email.message import EmailMessage
import email
import configparser
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Message:
    def __init__(self) -> None:
        self.tweet = Tweet()
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.user = config['message']['user']
        self.pw = config['message']['pw']

    def alert(self, body, to):
        # msg = EmailMessage()
        # msg.set_content(body)
        # msg['to'] = to
        # msg['Reply-To'] = "carbonell.alert@gmail.com"

        from_email = "carbonell.alert@gmail.com"

        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = from_email

        msg.attach(MIMEText(body))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.user, self.pw)
        server.send_message(msg)

        server.quit()

    def tweetMsg(self, to):
        text = self.tweet.get_tweet('CNN')
        self.alert(text, to)

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
if __name__ == "__main__":
    msg = Message()
    msg.alert("This is a working message",'4088588974@mms.att.net')
    #msg.tweetMsg("kylecarbonell13@gmail.com")
    #msg.tweetMsg('4088588974@mms.att.net')
