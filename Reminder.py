import json
import time


class Reminder:
    def __init__(self) -> None:
        self.load()

    def load(self):
        with open('Users.json') as file:
            self.users_file = json.load(file)
            self.reminders = self.users_file['Reminders']

    def get_reminders(self) -> list:
        self.load()
        return self.reminders

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
        with open('Users.json', 'r+') as js:
            file = json.load(js)
            file['Reminders'].append(rem)
            js.seek(0)
            json.dump(file, js, indent=4)

    def format_time(time : str):
        formatted_time = time.partition(":")
        no_space = formatted_time[2].partition(" ")[0]
        if('AM' in time or 'am' in time):
            return formatted_time[0] + ":" + no_space
        elif('PM' in time or 'pm' in time):
            return (int(formatted_time[0]) + 12) + ":" + no_space


    



    