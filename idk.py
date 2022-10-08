# Python program to explain the
# use of is_alive() method

import time
import threading

def thread_1(i):
    time.sleep(5)
    print('Value by Thread 1:', i)

def thread_2(i):
    print('Value by Thread 2:', i)
    
# Creating three sample threads 
thread1 = threading.Thread(target=thread_1, args=(1,))
thread2 = threading.Thread(target=thread_2, args=(2,))

# Before calling the start(), both threads are not alive
print("Is thread1 alive:", thread1.is_alive())
print("Is thread2 alive:", thread2.is_alive())
print()

thread1.start()
thread2.start()
# Since thread11 is on sleep for 5 seconds, it is alive
# while thread 2 is executed instantly

print("Is thread1 alive:", thread1.is_alive())
print("Is thread2 alive:", thread2.is_alive())
