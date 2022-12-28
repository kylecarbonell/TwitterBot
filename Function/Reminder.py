import json
import time


class Reminder:
    def __init__(self) -> None:
        self.users_file_name = 'Data/Reminders.json'
        self.load()
        
    def load(self):
        '''
        Loads the new Reminders.json file
        '''
        with open(self.users_file_name) as file:
            self.users_file = json.load(file)
            self.reminders = self.users_file['Reminders']

    def get_reminders(self) -> list:
        '''
        Gets all reminders
        '''
        self.load()
        return self.reminders

    def get_user_reminders(self, number : str) -> list:
        '''
        Gets all reminders of the user

        @param number
        '''
        user_reminder = []
        index = 1
        self.load()
        for i in self.reminders:
            if(i.get("phone_number") == number):
                user_reminder.append(str(index) + ". " + self.unformat_time(i.get('time')) + " : " + i.get("reminder") + "\n")
                index += 1
        print(user_reminder)
        return user_reminder

    def send_reminder(self):
        '''
        Sends reminder when the time is right
        '''
        reminders = self.get_reminders()
        reminders_sending = []
        #Loops through each reminder in list
        for reminder in reminders:
            if(reminder.get("time") == time.strftime("%H:%M")):
                reminders_sending.append([reminder.get("reminder"), reminder.get("phone_number")])
        return reminders_sending

    def add_reminder(self, reminder : str, time : str, number : str):
        '''
        Adds a reminder to the Reminders.json file

        @param reminder
        @param time
        @param number
        '''
        rem = {"phone_number" : number, "reminder" : reminder, "time" : self.format_time(time)}
        with open(self.users_file_name, 'r+') as js:
            file = json.load(js)
            file['Reminders'].append(rem)
            js.seek(0)
            json.dump(file, js, indent=4)

    def clear_all(self, phone_number):
        '''
        Deletes all reminders from the phone_number

        @param phone_number
        '''
        keep = []
        s = {"Reminders" : keep}
        
        with open(self.users_file_name, 'r+') as js:
            file = json.load(js)
            rem  : list = file['Reminders']

            for i in rem:
                if(i.get("phone_number") != phone_number):
                    keep.append(i)

        with open(self.users_file_name, 'w') as write:
            json.dump(s, write, indent = 4)


    def delete_reminder(self, phone_number : str, number : int):
        '''
        Deletes specific reminder

        @param phone_number
        @param number
        '''
        keep = []
        users_reminder = self.get_user_reminders(phone_number)

        with open(self.users_file_name, 'r+') as js:
            file = json.load(js)
            rem  : list = file['Reminders']

            if(number >= len(users_reminder) or number <= 0):
                return
            
            delete = users_reminder[number-1]

            for i in rem:
                if(i.get("phone_number") == phone_number):
                    if(i.get("time") == delete.get('time')):
                        if(i.get('reminder') == delete.get("reminder")):
                            pass
                        else:
                            keep.append(i)
                    else:
                        keep.append(i)
                else:
                    keep.append(i)
                    

        s = {"Reminders" : keep}
        with open(self.users_file_name, 'w') as write:
            json.dump(s, write, indent = 4)


    def format_time(self, time : str) -> str:
        '''
        Changes time to 24-hr format

        @param time
        '''
        formatted_time = time.partition(":")
        no_space = formatted_time[2].partition(" ")[0]

        if('PM' in time or 'pm' in time):
            return str(int(formatted_time[0]) + 12) + ":" + no_space

        return formatted_time[0] + ":" + no_space

    def unformat_time(self, time : str):
        '''
        Changes time to 12-hr format with am/pm

        @param time
        '''
        formatted_time = time.partition(":")

        if(int(formatted_time[0]) > 12):
            return str(int(formatted_time[0]) - 12) + ":" + formatted_time[2] + " PM"

        return time + " AM"


    



    