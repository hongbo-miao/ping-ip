import subprocess

from tenacity import retry, stop_after_attempt
import config


@retry(stop=stop_after_attempt(config.RETRY_ATTEMPTS))
def ping(ip):
    retval = subprocess.call(
        ["ping", "-c1", "-n", "-i0.1", "-W1", ip], stdout=subprocess.DEVNULL
    )

    # host is up
    if retval == 0:
        return ip
    else:
        raise Exception(f"{ip} is not active")
