from reactivex import operators as ops
from reactivex.scheduler import ThreadPoolScheduler
from threading import current_thread
import ipaddress
import multiprocessing
import reactivex as rx
import subprocess
import numpy as np


def ping(ip):
    retval = subprocess.call(["ping", "-c1", "-n", "-i0.1", "-W1", ip], stdout=subprocess.DEVNULL)
    if retval == 0:
        return True  # host is up
    else:
        return False  # host is down


def ping_ips(ip1, ip2):
    res1 = ping(ip1)
    res2 = ping(ip2)
    if res1 and not res2:
        return ip1
    elif res2 and not res1:
        return ip2
    else:
        return None


def ops_ping():
    def _ping(source):
        def subscribe(observer, scheduler=None):
            def on_next(ips):
                res = ping_ips(ips[0], ips[1])
                observer.on_next(res)

            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed)
        return rx.create(subscribe)
    return _ping


if __name__ == "__main__":
    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

    ip_tuple_list = list(zip(
        map(lambda ip: str(ip), list(ipaddress.ip_network('192.168.33.0/24').hosts())),
        map(lambda ip: str(ip), list(ipaddress.ip_network('192.168.34.0/24').hosts())),
    ))
    ip_tuple_list_chunks = np.array_split(ip_tuple_list, optimal_thread_count)

    for ip_tuple_list_chunk in ip_tuple_list_chunks:
        rx.of(*ip_tuple_list_chunk).pipe(
            ops_ping(), ops.subscribe_on(pool_scheduler),
            ops.filter(lambda ip: ip),
        ).subscribe(
            on_next=lambda ip: print(f"{current_thread().name} {ip}"),
            on_error=lambda e: print(e),
        )
