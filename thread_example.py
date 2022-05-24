from threading import Thread, currentThread, Lock
from queue import Queue
from datetime import datetime
from netmiko import ConnectHandler

NUM_THREADS = 3
PRINT_LOCK = Lock()

BREAKOUT_HOST_IP = "192.168.20.3"
BREAKOUT_PORTS = [9000, 9002, 9004]
COMMAND = "show ip int brief"

BASE_DEVICE_SETTINGS = {
    "device_type": "cisco_ios_telnet",
    "host": BREAKOUT_HOST_IP,
    "port": "",
    "global_delay_factor": 2,
}

def mt_print(msg):
    with PRINT_LOCK:
        print(msg)

def run_mt(mt_function, q, **kwargs):
    num_threads = min(NUM_THREADS, len(BREAKOUT_PORTS))

    for i in range(num_threads):
        thread_name = f'Thread-{i}'
        worker = Thread(name=thread_name, target=mt_function, args=(q, kwargs))
        worker.start()
        
    q.join()

def send_command(q, kwargs):
    command = kwargs['command']

    while True:
        thread_name = currentThread().getName()

        if q.empty():
            mt_print(f"{thread_name}: Closing as there's no jobs left in the queue.")
            return

        device_details = q.get()
        port = device_details["port"]

        mt_print(f"{thread_name}: Connecting to port {port}...")
        net_connect = ConnectHandler(**device_details)
        mt_print(f"{thread_name}: Connected!")
        mt_print(f"{thread_name}: Executing command:\n{command}")
        sh = net_connect.send_command(command)
        mt_print(f"{thread_name}: {port} output -\n{sh}")
        mt_print(f"{thread_name}: Done!")

        q.task_done()

def main():
    start_time = datetime.now()

    device_queue = Queue(maxsize=0)

    for port in BREAKOUT_PORTS:
        new_device = BASE_DEVICE_SETTINGS.copy()
        new_device["port"] = port
        device_queue.put(new_device)

    run_mt(mt_function=send_command, q=device_queue, command=COMMAND)

    print("\nElapsed time: " + str(datetime.now() - start_time))

if __name__ == '__main__':
    main()