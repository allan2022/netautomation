
"""
1. Read task
2. Network validation
3. Implement change
    - ACI change
    - Cisco change
    - Juniper change
    - Fortinet change
    - Palo Alto change
    - F5 change
    - IPAM change
4. Network validation

"""
import yaml

tasks = "aci"

def run(tasks):
    match tasks:
        case "aci":
            print("aci")
        case "core":
            print("core")
        case _:
            print("not available")

