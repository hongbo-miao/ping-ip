import ipaddress
import subprocess
from multiprocessing import Pool, freeze_support


def ping(ip):
    retval = subprocess.call(
        ["ping", "-c1", "-n", "-i0.1", "-W1", ip], stdout=subprocess.DEVNULL
    )
    if retval == 0:
        return ip
    else:
        return None


def ping_ips(ip1, ip2):
    res1 = ping(ip1)
    res2 = ping(ip2)
    if res1 or res2:
        print((res1, res2))
    return res1, res2


def main():
    ip_list = zip(
        map(lambda ip: str(ip), list(ipaddress.ip_network("192.168.1.0/24").hosts())),
        map(lambda ip: str(ip), list(ipaddress.ip_network("192.168.2.0/24").hosts())),
    )
    with Pool() as pool:
        raw_ips = pool.starmap(ping_ips, ip_list)
        print(list(filter(lambda ips: any(ips), raw_ips)))


if __name__ == "__main__":
    freeze_support()
    main()
