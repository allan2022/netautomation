from pyats.topology import Testbed, Device

device_a = Device('A')
device_b = Device('B')
device_c = Device('C')


testbed_a = Testbed(name = 'firstTestbed', alias = 'yetAnotherTestbed', devices = [device_a, device_b])
testbed_b = Testbed(name = 'secondTestbed')
testbed_b.add_device(device_c)
print(testbed_a)
print(testbed_b)