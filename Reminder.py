import json
import time


class Reminder:
    def __init__(self) -> None:
        self.load()

    def load(self):
        with open('Users.json') as file:
            self.users = json.load(file)
            self.users = self.users['Users']

    def get_reminders(self, number : str) -> list:
        self.load()
        return self.users.get(number).get('reminders')

    def send_reminder(self, numbers : list):
        #List of reminders(list)
        reminderList = []
        
        #Adds [all reminders of that phone number, phone number]
        for number in numbers:
            reminderList.append([self.get_reminders(number), number])
        print(reminderList)
        reminders_sending = []
        #Loops through each reminder in list
        for reminders in reminderList:
            #Loops through remindres[0](All Reminders of each phone_number)
            for reminder in reminders[0]:
                if(reminder.get("time") == time.strftime("%H:%M")):
                    reminders_sending.append([reminder.get("reminder"), reminders[1]])
        return reminders_sending

    def add_reminder(self, reminder : str, time : str, number : str):
        rem = {"reminder" : reminder, "time" : time}
        with open('Users.json', 'r+') as js:
            file = json.load(js)
            file['Users'].get(number).get("reminders").append(rem)
            js.seek(0)
            json.dump(file, js, indent=4)
        self.users.get(number).get('reminders').append(rem)

    def format_time(time : str):
        if('AM' in time):
            return time[0:2] + ":" + time[2:4]
        elif('PM' in time):
            return (int(time[0:2]) + 12) + ":" + time[2:4]


    



    