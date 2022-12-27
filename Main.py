import multiprocessing as mp
from Message import Message
import time

if __name__ == "__main__":
    msg = Message()
    user_response = mp.Process(target=msg.run_response)
    reminder_process = mp.Process(target=msg.run_reminders)
    delete_process = mp.Process(target=msg.run_delete)

    user_response.start()
    reminder_process.start()
    delete_process.start()


