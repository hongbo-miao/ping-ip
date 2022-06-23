import subprocess


def ping(ip):
    retval = subprocess.call(["ping", "-c1", "-n", "-i0.1", "-W1", ip])
    if retval == 0:
        return True  # host is up
    else:
        return False # host is down
