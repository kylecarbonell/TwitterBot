import multiprocessing as mp
from Message import Message
import time
import mysql.connector

if __name__ == "__main__":
    msg = Message()
    user_response = mp.Process(target=msg.run_response)
    reminder_process = mp.Process(target=msg.run_reminders)

    user_response.start()
    reminder_process.start()


