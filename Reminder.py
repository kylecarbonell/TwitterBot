import json
import time


class Reminder:
    def __init__(self) -> None:
        self.users_file_name = 'Data/Users.json'
        self.load()
        
    def load(self):
        with open(self.users_file_name) as file:
            self.users_file = json.load(file)
            self.reminders = self.users_file['Reminders']

    def get_reminders(self) -> list:
        self.load()
        return self.reminders

    def get_user_reminders(self, number : str) -> list:
        user_reminder = []

        self.load()
        for i in self.reminders:
            if(i.get("phone_number") == number):
                user_reminder.append("@" + self.unformat_time(i.get('time')) + " : " + i.get("reminder") + "\n")
        print(user_reminder)
        return user_reminder

    def send_reminder(self):
        reminders = self.get_reminders()
        reminders_sending = []
        #Loops through each reminder in list
        for reminder in reminders:
            if(reminder.get("time") == time.strftime("%H:%M")):
                reminders_sending.append([reminder.get("reminder"), reminder.get("phone_number")])
        return reminders_sending

    def add_reminder(self, reminder : str, time : str, number : str):
        rem = {"phone_number" : number, "reminder" : reminder, "time" : self.format_time(time)}
        with open(self.users_file_name, 'r+') as js:
            file = json.load(js)
            file['Reminders'].append(rem)
            js.seek(0)
            json.dump(file, js, indent=4)

    def format_time(self, time : str) -> str:
        formatted_time = time.partition(":")
        no_space = formatted_time[2].partition(" ")[0]

        if('PM' in time or 'pm' in time):
            return str(int(formatted_time[0]) + 12) + ":" + no_space

        return formatted_time[0] + ":" + no_space

    def unformat_time(self, time : str):
        formatted_time = time.partition(":")

        if(int(formatted_time[0]) > 12):
            return str(int(formatted_time[0]) - 12) + ":" + formatted_time[2] + " PM"

        return time + " AM"


    



    