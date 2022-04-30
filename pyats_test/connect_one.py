# Example
# -------
#
#   connecting to device

# using the sample topology file from
import os
from pyats import topology

testbedfile = os.path.join(os.path.dirname(topology.__file__),
                           'sampleTestbed.yaml')
testbed = topology.loader.load(testbedfile)

# pick a device
n7k5 = testbed.devices['ott-tb1-n7k5']

# connect to it by calling connect()
#   this is actually a ConnectionManager method. the compound object
#   redirects the call to Device.connectionmgr.connect(), and:
#       - defaults to using connection alias "default"
#       - and creates the connection
#
#   in effect, this is the same as calling
#       n7k5.connectionmgr.connect()
n7k5.connect == n7k5.connectionmgr.connect
# True
n7k5.connect()
n7k5.is_connected()
# True

# since the connection above is aliased with default
# we can make calls to it directly.
n7k5.default
# ott-tb1-n7k5(default)
n7k5.default.execute('show clock')
# 00:56:54.569 EST Sat Mar 07 2015

# default connections are also shortcut to the device level, so users
# don't always have to type the default alias
n7k5.execute == n7k5.default.execute == n7k5.connectionmgr.default.execute
# True
n7k5.execute('show clock')
# 00:58:27.069 EST Sat Mar 07 2015

# the connection manager is capable of handling multiple connections
# each connection is referred to via its alias, and the connection object
# is again compounded to be callable directly under the device object.
# if supported, you can always create extra connections to
# the same connection type, as long as this is supported by the device

# creating a new connection to the alt (mgmt) connection definition
# and calling it 'mgmt'. After connecting, you can make calls to it.
n7k5.connect(alias = 'mgmt', via = 'alt')
n7k5.mgmt.execute('show version')
# ... etc