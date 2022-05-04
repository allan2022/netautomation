class SetupEnvironment:
    def __init__(self):
        self.device_list = ""
        self.command_list = ""
        self.change_number = ""
        self.test_type = ""

    def setup_pyats(self):
        # self.device_file = input("Specify device file: ")
        # self.command_file = input("Specify command file: ")
        self.device_file = "device2.csv"
        self.command_file = "command1.csv"
        self.change_number = input("Specify change numebr: ")
 
        ans = True
        while ans:
            print('''
            1. Pre-change test
            2. Post-change test and validation
            3. Exit 
            ''')
            ans = input("Select test type: ")
            if ans == "1":
                self.test_type = "before"
                ans = False
            elif ans == "2":
                self.test_type = "after"
                ans = False
            elif ans == "3":
                ans = False
            elif ans == "":
                ans = True
                print("\n Not a Valid Choice Try again")                
            else:    
                print("\n Not a Valid Choice Try again")

