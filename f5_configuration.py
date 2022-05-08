import os
from utils.get_task import get_task
from envtools.setup_environment import SetupEnvironment
from netmikotools.netmiko_command import NetmikoCommand

F5_DEVICE_LIST = os.getcwd() + '/src/f5_configuration_device_inventory.csv'
F5_ENVIRONMENT = os.getcwd() + '/src/configuration_environment.yaml'

class F5Configuration:
    def __init__(self):
        self.task_list = []
        self.task_select = ""

        try:
            self.task_list, self.task_select = get_task(F5_ENVIRONMENT, 'sub_tasks')
        except KeyboardInterrupt:
            pass

    def f5_config(self):
        f5_env = SetupEnvironment(F5_ENVIRONMENT)
        if f5_env.change_number != "":
            f5_env.setup_configuration_netmiko(F5_DEVICE_LIST, F5_ENVIRONMENT, self.task_select)
            
            devices = f5_env.device_list
            commands = f5_env.command_list

            print("####### devices ############")
            print(devices)
            print("########### commands #############")
            print(commands)
            print("\n" + "-"*20 + " all devices to be configured " + "-"*20)
            for dev in devices:
                print('{} : {} '.format(dev['device_type'], dev['host'] ))
            print("-" * (40 + len(" all devices to be configured ")) +"\n")

            netmiko_dev = NetmikoCommand()
            netmiko_dev.config(devices, commands)


def main():
    cv = F5Configuration()
    cv.f5_config()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n tast aborted")