from queue import Queue
from netmiko import ConnectHandler
from threading import Thread, currentThread, Lock
from utils.save_output import save_output

class NetmikoCommand:
    def __init__(self):
        self.NUM_THREADS = 3
        self.PRINT_LOCK = Lock()

    def mt_print(self, msg):
        with self.PRINT_LOCK:
            print(msg)

    # log configuration for one device
    def snapshot_one (self, d_queue, env):

        commands = env.command_list
        s_folder = env.snapshot_folder
        cnum = env.change_number
        p_folder = env.parser_folder

        while True:
            t_name = currentThread().getName()

            if d_queue.empty():
                self.mt_print(f'No task left, {t_name} is closed. ')

            device = d_queue.get()
            hostname = device['host']
            cmds = commands[device['device_type']]

            self.mt_print(f'{t_name}: connecting to {hostname}...')
            netconnect = ConnectHandler(**device)
            self.mt_print(f'{t_name}: connected to {hostname}...')

            for command in cmds:
                d_type = device["device_type"]          

                if d_type == "fortinet":
                    netconnect.send_config_set(['config vdom', 'edit root'])

                self.mt_print(f'{t_name}: executing command on --- {hostname} --- {command}')
                output = netconnect.send_command(command)
                self.mt_print(f'{t_name} executing command on --- {hostname} --- {command} is done...')

                self.mt_print(f'{t_name}: generating output file on --- {hostname}')
                save_output(command, output, cnum, s_folder, p_folder, hostname, d_type)
                self.mt_print(f'{t_name}: output on --_ {hostname} is done... ')

            netconnect.disconnect()
            # d_queue.task_done() 

    # log configuration for all devices by calling exec_snapshot
    def snapshot_all (self, env):    
    
        devices = env.device_list
        num_threads = min (self.NUM_THREADS, len(devices))

        device_queue = Queue(maxsize=0)

        # multi threads - one thread per device    

        print("\n" + "_"*20 + " all devices to be validated " + "_"*20)
        for dev in devices:
            print('{} : {} '.format(dev['device_type'], dev['host']))
            device_queue.put(dev)
        print("_" * (40 + len(" all devices to be validated ")) + "\n")

        for i in range(num_threads):
            t_name = f'Thread - {i}'

            t1 = Thread(name=t_name, target=self.snapshot_one, args=(device_queue, env))
            t1.start()

        device_queue.join()


    def exec_f5_config(self, device, commands):
        netconnect = ConnectHandler(**device)
        devname = device['host']

        print("-"*20 + f' commands for {devname} ' + "-"*20)
        for command in commands:
            expect_prompt = r"(root@.*#|\s*|[#|\$]\s*$)"
            output = netconnect.send_command_expect(command, expect_string=expect_prompt, cmd_verify=False)

            if output == "":
                print(f'{command} \n -- succeed\n')
            else:
                print(f'{command} \n -- failed\n')

        netconnect.disconnect()   

    # config for all devices by calling exec_command
    def config (self, devices, commands):    

        # multi threads - one thread per device    
        for device in devices:        
            threads = [Thread(target=self.exec_f5_config, args=(device, commands)) for _ in range(8)] 
            for t1 in threads:
                t1.start()
                t1.join()

    def fortinet_vdom(self, device, commands):
        netconnect = ConnectHandler(**device)
        devname = device['host']

        print("-"*20 + f' commands for {devname} ' + "-"*20)
        for command in commands:
            expect_prompt = r"(root@.*#|\s*|[#|\$]\s*$)"
            output = netconnect.send_command_expect(command, expect_string=expect_prompt, cmd_verify=False)

            if output == "":
                print(f'{command} \n -- succeed\n')
            else:
                print(f'{command} \n -- failed\n')

        netconnect.disconnect()   
