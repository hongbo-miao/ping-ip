import ipaddress
import multiprocessing
from threading import current_thread

import numpy as np
import reactivex as rx
from reactivex import operators as ops
from reactivex.scheduler import ThreadPoolScheduler
from utils.ops_ping import ops_ping

SKIP_LIST = set(["108"])


if __name__ == "__main__":
    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

    ip_tuple_list = list(
        zip(
            map(
                lambda ip: str(ip),
                list(ipaddress.ip_network("192.168.1.0/24").hosts()),
            ),
            map(
                lambda ip: str(ip),
                list(ipaddress.ip_network("192.168.2.0/24").hosts()),
            ),
        )
    )
    ip_tuple_list_chunks = np.array_split(ip_tuple_list, optimal_thread_count)

    for ip_tuple_list_chunk in ip_tuple_list_chunks:
        rx.of(*ip_tuple_list_chunk).pipe(
            # Exclude both 192.168.1.56 and 192.168.2.56 by last "56"
            ops.filter(lambda ips: ips[0][ips[0].rindex(".") + 1 :] not in SKIP_LIST),
            ops_ping(),
            # ops.retry(3),
            ops.catch(rx.empty()),
            ops.subscribe_on(pool_scheduler),
            ops.filter(lambda ips: ips[0] or ips[1]),
        ).subscribe(
            on_next=lambda ip: print(f"{current_thread().name} {ip}"),
            on_error=lambda e: print(e),
        )
