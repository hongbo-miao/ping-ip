import reactivex as rx

from .ping_ips import ping_ips


def ops_ping():
    def _ping(source):
        def subscribe(observer, scheduler=None):
            def on_next(ips):
                try:
                    res = ping_ips(ips[0], ips[1])
                    observer.on_next(res)
                except Exception as e:
                    observer.on_error(e)

            return source.subscribe(on_next, observer.on_error, observer.on_completed)

        return rx.create(subscribe)

    return _ping
