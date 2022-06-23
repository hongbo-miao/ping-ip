from reactivex import operators as ops
from reactivex.scheduler import ThreadPoolScheduler
from threading import current_thread
import ipaddress
import multiprocessing
import reactivex as rx
import subprocess

def ping_():
    def _ping(source):
        def subscribe(observer, scheduler=None):
            def on_next(ip):
                retval = subprocess.call(["ping", "-c1", "-n", "-i0.1", "-W1", ip])
                # host is up
                if retval == 0:
                    observer.on_next(ip)
                else:
                    # host is down
                    observer.on_next("")

            return source.subscribe(
                on_next,
                observer.on_error,
                observer.on_completed)
        return rx.create(subscribe)
    return _ping

if __name__ == "__main__":
    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

    ip_list = map(lambda ip: str(ip), list(ipaddress.ip_network('192.168.1.0/24').hosts()))
    rx.of(*ip_list).pipe(
        ping_(), ops.subscribe_on(pool_scheduler)
    ).subscribe(
        on_next=lambda i: print("PROCESS 3: {0} {1}".format(current_thread().name, i)),
        on_error=lambda e: print(e),
    )
