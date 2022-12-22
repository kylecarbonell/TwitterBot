import multiprocessing as mp
from Message import Message
from Reminder import Reminder
import time

res = []
def test():
    for number in range(1000000):
        print(number)
        time.sleep(2)

if __name__ == "__main__":
    msg = Message()
    
    print("Time ", time.strftime('%H:%M'))
    user_response = mp.Process(target=msg.run_response)
    test_process = mp.Process(target=msg.run_reminders)
    user_response.start()
    test_process.start()


