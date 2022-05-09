import logging
import netmiko

logging.basicConfig(filename='bigip.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

def log_msg(lvl, msg):
    """
    :param lvl:
    :param msg:
    :return:
    """
    global LOGGER
    if LOGGER:
        LOGGER.log(lvl, msg)
    else:
        print(msg)

def device_connection(**kwargs):
    """
    Connect to device using netmiko
    :type kwargs: dict
    """
    if 'key_file' in kwargs:
        device_password = {
            'use_keys': True,
            'key_file': kwargs['key_file']
        }
    else:
        device_password = {
            'password': kwargs['password']
        }
    device = {
        'device_type': kwargs['device_type'],
        'host': kwargs['ip'],
        'username': kwargs['username'],
        'port': kwargs['port'],
        'blocking_timeout': kwargs.get('blocking_timeout', 20),
        'keepalive': kwargs.get('keepalive', 1),
        'session_log': 'bigip.log'
    }
    device.update(device_password)
    try:
        handl = netmiko.ConnectHandler(**device)
        return handl
    except netmiko.ssh_exception.NetMikoTimeoutException as err1:
        log_msg(logging.WARNING, "Timeout({}): {}".format(kwargs['ip'], err1))
        raise DeviceConnectionTimeout(err1)
    except netmiko.ssh_exception.NetMikoAuthenticationException as err2:
        raise DeviceAuthenticationFailure(err2)
    except Exception as err3:
        log_msg(logging.WARNING,
                "Exception({}): {}".format(kwargs['ip'], err3))
        raise err3

if __name__ == "__main__":
    device_data = {
            'device_type': 'f5_linux',
            'ip': 'xxxxxxxx',
            'username': 'xxxx',
            'password': 'xxxxxxx',
            'port': 22
            }
    handle = device_connection(**device_data)
    cmd = 'tmsh create net ipsec ike-peer dgtbptxhnfvt app-service none ca-cert-file none crl-file none description none dpd-delay 30 generate-policy off lifetime 1440 mode main my-cert-file none my-cert-key-file none my-cert-key-passphrase none my-id-type address my-id-value 15.1.1.1 nat-traversal off passive false peers-cert-file none peers-cert-type none peers-id-type address peers-id-value 15.1.1.10 phase1-auth-method pre-shared-key phase1-encrypt-algorithm aes256 phase1-hash-algorithm sha256 phase1-perfect-forward-secrecy modp1024 preshared-key-encrypted test@123 prf sha256 proxy-support enabled remote-address 15.1.1.10 replay-window-size 64 state enabled traffic-selector replace-all-with { /Common/xhgynrlwyzvk} verify-cert true version replace-all-with { v2 }'
    expect_prompt = r"(root@.*#|\s*|[#|\$]\s*$)"
    handle.send_command_expect(cmd, expect_string=expect_prompt)
