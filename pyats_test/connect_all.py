# Example
# -------
#
# connecting to devices in parallel

# using the sample topology file from
from pyats import topology

testbedfile = os.path.join('sampleTestbed.yaml')
testbed = topology.loader.load(testbedfile)

# connect to all devices in this testbed
testbed.connect()

# connect to some devices in this testbed
testbed.connect(testbed.devices['uut'],
                testbed.devices['helper'])

# connect to some devices in this testbed
# and provide unique vias
testbed.connect(testbed.devices['uut'],
                testbed.devices['helper'],
                vias = {'uut': 'cli',
                        'helper': 'console'})

# connect to some devices in this testbed
# using unique vias per device, and shared kwargs (eg, log_stdout = False)
# shared keyword-arguments will be passed to every single connection
testbed.connect(testbed.devices['uut'],
                testbed.devices['helper'],
                vias = {'uut': 'cli',
                        'helper': 'console'},
                log_stdout = False)