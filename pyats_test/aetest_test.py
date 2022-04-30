from pyats import aetest
from some_lib import configure_interface


print(type(aetest))
print(dir(aetest))

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_device(self, testbed):
        for device in testbed:
            device.connect()
