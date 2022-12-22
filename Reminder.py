import json
import time


class Reminder:
    def __init__(self) -> None:
        with open('Users.json') as file:
            self.users = json.load(file)
            self.users = self.users['Users']


    def get_reminders(self, number : str) -> list:
        return self.users.get(number).get('reminders')

    def send_reminder(self, numbers : list):
        #List of reminders(list)
        reminderList = []
        
        #Adds [all reminders of that phone number, phone number]
        for number in numbers:
            reminderList.append([self.get_reminders(number), number])

        reminders_sending = []
        #Loops through each reminder in list
        for reminders in reminderList:
            #Loops through remindres[0](All Reminders of each phone_number)
            for reminder in reminders[0]:
                if(reminder.get("time") == time.strftime("%H:%M")):
                    reminders_sending.append([reminder.get("reminder"), reminders[1]])
        print(reminders_sending)
        return reminders_sending

    



    