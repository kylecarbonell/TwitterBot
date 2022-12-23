import multiprocessing as mp
from Message import Message
import time

if __name__ == "__main__":
    msg = Message()
    val ="10:20 pm".partition(":")
    user_response = mp.Process(target=msg.run_response)
    test_process = mp.Process(target=msg.run_reminders)
    # user_response.start()
    # test_process.start()


