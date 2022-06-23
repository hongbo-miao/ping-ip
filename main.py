import subprocess
import ipaddress
from multiprocessing import Pool, freeze_support


def ping(ip):
    retval = subprocess.call(["ping", "-c1", "-n", "-i0.1", "-W1", ip])
    if retval == 0:
        return True  # host is up
    else:
        return False  # host is down


def ping_ips(ip1, ip2):
    res1 = ping(ip1)
    res2 = ping(ip2)
    print(ip1, ip2)
    if res1 and not res2:
        return ip1
    elif res2 and not res1:
        return ip2
    else:
        return None


def main():
    ip_list = zip(
        map(lambda ip: str(ip), list(ipaddress.ip_network('192.168.1.0/24').hosts())),
        map(lambda ip: str(ip), list(ipaddress.ip_network('192.168.2.0/24').hosts())),
    )
    with Pool() as pool:
        res = pool.starmap(ping_ips, ip_list)
        print(res)


if __name__ == "__main__":
    freeze_support()
    main()
