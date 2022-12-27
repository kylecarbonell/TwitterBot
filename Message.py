from Twitter import Tweet
from Reminder import Reminder

import smtplib
import email
import configparser
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import decode_header
from email import encoders

import urllib.request

import imaplib
import time

import json

class Message:
    def __init__(self) -> None:
        self.tweet = Tweet()
        self.reminder = Reminder()

        config = configparser.ConfigParser()
        config.read('Data/config.ini')

        self.username = config['message']['user']
        self.pw = config['message']['pw']

        self.users_file = 'Data/Users.json'
        with open(self.users_file) as file:
            self.users = json.load(file)
            self.recipients = []
            for key in self.users['Users']:
                self.recipients.append(key)

        self.running = True

    #Sends text messages using smtp library 
    def send_message(self, body : str, to : str):
        '''
        This sends any type of text message to the user

        @param body: Actual content of the text message
        @param to: Address the message is being sent to
        '''
        msg = MIMEMultipart()
        msg['To'] = to
        msg['From'] = self.username

        msg.attach(MIMEText(body))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
        server.login(self.username, self.pw)
        server.sendmail(self.username, to, msg.as_string())

        server.quit()

    #Sends images as JPEG
    def send_file(self, file : str, to : str, mime_main : str = 'image', mime_sub : str = 'jpeg'):
        '''
        This function is used to send an image to the user. Uses the MIMEMultipart object
        to store the image information onto a MIMEBase and encode it to send to the user.

        @param file: Link to image
        @param to: Address image is being sent to
        @param mime_main: Type of MIMEBase being sent, this defaults to an Image
        @param mime_sub: Subtype of MIMEBase being sent, this defaults to JPEG
        '''
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

    def tweetMsg(self, to : str, user : str):
        '''
        This uses the get_tweet function and gets the latest tweet from the user.
        This function uses the send_message function to send a message to the address

        @param to: Address that the message is being sent to
        @param user: Twitter username the tweet is being searched for
        '''
        text = self.tweet.get_tweet(user)
        if(text[0] == None):
            self.send_message("@ERROR:\nUSER NOT FOUND!", to)
            return
        self.send_message(text[0], to)
        if(text[1] != None):
            self.send_file(text[1], to, 'image', 'jpeg')

    def getResponse(self) -> tuple:
        '''
        This function is always running. 
        This gets the most recent "UNSEEN" response from Alert Bot's email. 
        If there are no current response Alert Bot will delete the oldest "SEEN" message

        :return: A tuple containing the message the user sent and the senders phone number or address it was sent from
        '''
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
                    if(any(word in body for word in ["@Subscribe", "@subscribe"])):
                        return [body, sender]
                    elif(sender in self.recipients):
                        return [body, sender]
                    else:
                        self.send_message("Please type '@Subscribe' to subscribe to Alert Bot followed by your NAME on a seperate lines", sender)
                        return [None, None]

        #Deletes messages
        _, delete = mail.search(None, 'SEEN')
        deleteMessage = delete[0].split(b' ')
        #print(delete)
        if(deleteMessage[0] != b''):
            mail.store(deleteMessage[0], "+FLAGS", "\\Deleted")
            mail.expunge()

        mail.close()
        return [None, None]


    #Adds user phone number, name and email to Users.json
    def add_user(self, name : str, phone_number : str, email : str = ''):
        '''
        This function adds a user to Users.json and allows user to 
        request commands from Alert bot

        @param name: This is the name of the user
        @param phone_number: This is the users phone number
        @param email: This is the users email
        '''

        new_user = {'name' : name, 'email' : email}
        with open(self.users_file, 'r+') as js:
            file = json.load(js)
            file['Users'][phone_number] = new_user
            js.seek(0)
            json.dump(file, js, indent=4)
        self.recipients.append(phone_number)
        self.send_message("Account created!", phone_number)

    #Runs commands based on user input from IMsg
    def run_command(self, command : str, to : str):
        '''
        This checks the command being passed in and sends a message back to the user

        @param command: A message sent by the user
        @param to: Address message is being sent to
        '''

        #Sends help text box
        if any(word in command for word in ['Help', 'help']):
            options =   "@Help:\n" \
                        "1. Type '@News' to get the current news\n\n" \
                        "2. Type @ and a twitter username to get their recent tweet\n\n" \
                        "3. Type '@Reminder' followed by your reminder and the time (03:20 am/pm) on 2 separate lines.\n\n"\
                        "4. Type '@Clear' to remove all your reminders\n\n"\
                        "5. Type '@Delete' followed by the number of the reminder you want to delete\n\n"\
                        "---------------------------------\n\n"\
                        "6. Type 'GET reminders' to get all your reminders"
            self.send_message(options, to)
        #Sends news from @cnn
        elif any(word in command for word in ['@News', '@news']):
            self.tweetMsg(to, "CNN")
        #Adds user data onto Users.json
        elif any(word in command for word in ['@Subscribe', '@subscribe']):
            if('\n' in command):
                info = command.split("\n")
                info.append("")
                self.add_user(info[1], to, info[2])
            else:
                self.send_message("@ERROR:\nCommand does not contain your name or your email!", to)
                self.run_command('help', to)
        #Gets all users reminders
        elif any(word in command for word in ['reminder', 'Reminder', 'reminders', 'Reminders']) and any(word in command for word in ["GET", "Get", "get"]):
            self.send_message("GET reminders\n" + "".join(self.reminder.get_user_reminders(to)).strip(), to)
        #Adds a reminder to User.json
        elif any(word in command for word in ["@reminder", "@Reminder"]):
            if('\n' in command):
                info = command.split("\n")
                self.reminder.add_reminder(info[1], info[2], to)
                self.send_message("Reminder created!", to)
            else:
                self.send_message("@ERROR:\nCommand does not contain the reminder or the time!", to)
                self.run_command('help', to)
        #Deletes all reminders
        elif any(word in command for word in ["@clear", "@Clear"]):
            self.reminder.clear_all(to)
            self.send_message("All reminders cleared!", to)
        #Deletes specific reminder
        elif any(word in command for word in ['@delete', '@Delete']):
            if('\n' in command):
                info = command.split('\n')
                self.reminder.delete_reminder(to, int(info[1]))
                self.send_message("Deleteing reminder...", to)
                self.run_command("GET reminders", to)
            else:
                self.send_message("@ERROR:\nCommand does not contain a reminder or a time to delete", to)
        #Sends latest tweet from the whoever the user @
        elif any(word in command for word in ['@']):
            self.tweetMsg(to, command.partition('@')[2])
        else:
            self.send_message("Alert bot does not understand this command", to)
            self.run_command('help', to)

    def run_response(self):
        print("Response bot starting...")
        while self.running:
            time.sleep(3)
            res = self.getResponse()
            to = res[1]
            message = res[0]
            if([to, message] != [None, None]):
                self.run_command(message, to)

    def run_reminders(self):
        print("Reminder bot starting...")
        self.send_message('I am a hacker. This is the chinese communist party. I am taking over your phone', "4088588974@mms.txt.net")
        while self.running:
            #List of tuples of [Reminder list, phone number]
            reminders = self.reminder.send_reminder()
            #Loops for each tuple(reminder = [reminder, phone number])
            for reminder in reminders:
                self.send_message("@Reminder:\n" + reminder[0], reminder[1])
            time.sleep(60)