import subprocess
from typing import Optional, Tuple

import config
from tenacity import RetryError, retry, retry_if_exception_type, stop_after_attempt


@retry(
    stop=stop_after_attempt(config.RETRY_ATTEMPTS),
    retry=retry_if_exception_type(ConnectionError),
)
def ping_ip(ip: str) -> str:
    """
    Ping an IP address and return the IP if it is pingable.

    Parameters
    ----------
    ip : str
        ip address to ping

    Returns
    -------
    str
        ip address

    Raises
    ------
    RetryError
        if the ip is not pingable after the configured number of retries
    """
    retval = subprocess.call(
        ["ping", "-c1", "-n", "-i0.1", "-W1", ip], stdout=subprocess.DEVNULL
    )

    # host is up
    if retval == 0:
        return ip
    else:
        raise ConnectionError(f"{ip} is not active")


def ping_ips(ip1: str, ip2: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Ping two IP addresses and return the IPs if they are pingable.

    Parameters
    ----------
    ip1 : str
        ip address to ping
    ip2 : str
        ip address to ping

    Returns
    -------
    Tuple[Optional[str], Optional[str]]
        ip addresses if they are pingable
    """
    res1 = None
    res2 = None
    try:
        res1 = ping_ip(ip1)
    except RetryError:
        pass
    try:
        res2 = ping_ip(ip2)
    except RetryError:
        pass
    return res1, res2
