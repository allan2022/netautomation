# Example
# -------
#
# disconnecting from devices in parallel
# using the sample topology file from
from pyats import topology
testbed = topology.loader.load('your-testbed-file.yaml')
# connect to all devices in this testbed
testbed.connect()
# disconnect from all devices in this testbed
testbed.disconnect()
# disconnect from some devices in this testbed
testbed.disconnect(testbed.devices['uut'],
                testbed.devices['helper'])
# disconnect from some devices in this testbed
# and provide unique vias
testbed.disconnect(testbed.devices['uut'],
                testbed.devices['helper'],
                vias = {'uut': 'cli',
                        'helper': 'console'})
# disconnect from some devices in this testbed
# using unique vias per device, and shared kwargs
# shared keyword-arguments will be passed to every single connection
testbed.disconnect(testbed.devices['uut'],
                testbed.devices['helper'],
                vias = {'uut': 'cli',
                        'helper': 'console'},
                        log_stdout = False)