import csv
import threading
from queue import Queue
from getpass import getpass
from netmiko import ConnectHandler

# Define username and password to login to all routers with
USER = 'admin'
PASSWORD = 'Admin_1234!'

# Define router IPs, you could also make a dictionary imported from a CSV file, or create a list from a text file of hostnames
routers = ['131.226.217.151', '131.226.217.151', '131.226.217.151']

def ssh_session(router, output_q):
    # Place what you want each thread to do here, for example connect to SSH, run a command, get output
    output_dict = {}
    hostname = router
    router = {'device_type': 'cisco_nxos', 'ip': router, 'username': USER, 'password': PASSWORD, 'verbose': False, }
    ssh_session = ConnectHandler(**router)
    output = ssh_session.send_command("show version")
    output_dict[hostname] = output
    output_q.append(output_dict)


if __name__ == "__main__":

    output_q = []
    
    # Start thread for each router in routers list
    for router in routers:
          my_thread = threading.Thread(target=ssh_session, args=(router, output_q))
          my_thread.start()

    # Wait for all threads to complete
    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    # Retrieve everything off the queue - k is the router IP, v is output
    # You could also write this to a file, or create a file for each router
    
    # for item in output_q:
    #     for k, val in item:
    #         print(k)
    #         print(val)

    print(output_q)