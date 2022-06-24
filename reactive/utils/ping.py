import subprocess

from tenacity import retry, retry_if_exception_type, stop_after_attempt
import config


@retry(
    stop=stop_after_attempt(config.RETRY_ATTEMPTS),
    retry=retry_if_exception_type(ConnectionError),
)
def ping_ip(ip):
    retval = subprocess.call(
        ["ping", "-c1", "-n", "-i0.1", "-W1", ip], stdout=subprocess.DEVNULL
    )

    # host is up
    if retval == 0:
        return ip
    else:
        raise ConnectionError(f"{ip} is not active")


def ping_ips(ip1, ip2):
    # return ip1, ip2
    res1 = None
    res2 = None
    try:
        res1 = ping_ip(ip1)
    except Exception:
        pass
    try:
        res2 = ping_ip(ip2)
    except Exception:
        pass
    return res1, res2
