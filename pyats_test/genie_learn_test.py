# Import Genie
from genie import testbed

# Look at the bottom for an example of a testbed file
testbed = testbed.load('testbed.yaml')

# Find the device I want to connect to
device = testbed.devices['nx-osv-1']

# Connect to it
device.connect()

# Parse device output
output = device.parse('show version')

# Print it nicely
import pprint
pprint.pprint(output)

{'platform': {'hardware': {'bootflash': '3184776 kB',
                           'chassis': 'NX-OSv Supervisor Module',
                           'device_name': 'nx-osv-1',
                           'model': 'NX-OSv',
                           'processor_board_id': 'TM00010000B',
                           'slots': 'None'
                           },
            }
}
