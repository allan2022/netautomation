from napalm.base import get_network_driver
import sys
import json

hostname = sys.argv[1]
acl_file = sys.argv[2]


with open("inventory.json", "r") as f:
    dev_db = json.load(f)
dev_param = dev_db[hostname.lower()]
driver = get_network_driver(dev_param['type'])

with driver(dev_param['IP'], dev_param['user'], dev_param['password']) as device:
    device.open()
    device.load_merge_candidate(acl_file)
    device.commit_config()
    device.close()