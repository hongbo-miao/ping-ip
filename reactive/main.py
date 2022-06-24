import ipaddress
import multiprocessing
from threading import current_thread

import config
import numpy as np
import reactivex as rx
from reactivex import operators as ops
from reactivex.scheduler import ThreadPoolScheduler
from utils.ops import ops_ping

if __name__ == "__main__":
    skip_set = set(config.SKIP_LIST)
    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

    # Get [("192.168.1.1", "192.168.2.1"), ("192.168.1.2", "192.168.2.2"), ...]
    ip_tuple_list = list(
        zip(
            map(
                lambda ip: str(ip),
                list(ipaddress.ip_network(config.IP_ADDRESS_1).hosts()),
            ),
            map(
                lambda ip: str(ip),
                list(ipaddress.ip_network(config.IP_ADDRESS_2).hosts()),
            ),
        )
    )

    # Split the IP list into chunks based on the number of CPUs in the system
    ip_tuple_list_chunks = np.array_split(ip_tuple_list, optimal_thread_count)
    print(ip_tuple_list_chunks)

    for ip_tuple_list_chunk in ip_tuple_list_chunks:
        rx.of(*ip_tuple_list_chunk).pipe(
            # Exclude both 192.168.1.x and 192.168.2.x by last x
            ops.filter(lambda ips: ips[0][ips[0].rindex(".") + 1 :] not in skip_set),
            # Ping the IP by the pair (192.168.1.x and 192.168.2.x)
            ops_ping(),
            # Concurrency
            ops.subscribe_on(pool_scheduler),
            # Hide if both 192.168.1.x and 192.168.2.x are not pingable
            ops.filter(lambda ips: ips[0] or ips[1]),
        ).subscribe(
            on_next=lambda ip: print(f"{current_thread().name} {ip}"),
            on_error=lambda e: print(e),
        )
