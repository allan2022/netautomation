import csv
import threading
# from queue import Queue
from getpass import getpass
from netmiko import ConnectHandler

# Define username and password to login to all routers with
# USER = 'admin'
# PASSWORD = 'Admin_1234!'

# Define router IPs, you could also make a dictionary imported from a CSV file, or create a list from a text file of hostnames
routers = [ {"ip":"131.226.217.151", "user": "admin", "password": "Admin_1234!", "dev": "cisco_nxos"}, {"ip":"131.226.217.150", "user": "admin", "password": "C1sco12345", "dev":"cisco_xr"} ]

def ssh_session(router, output_q):
    # Place what you want each thread to do here, for example connect to SSH, run a command, get output
    output_dict = {}
    hostname = router["ip"]
    router = {'device_type': router["dev"], 'ip': router["ip"], 'username': router["user"], 'password': router["password"], 'verbose': False, }
    ssh_session = ConnectHandler(**router)
    output = ssh_session.send_command("show ip int brief")
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

    for item in output_q:
        print(item)
        print("##########################")