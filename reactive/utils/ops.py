from typing import Callable, Optional, Tuple

import reactivex as rx
from reactivex.abc import DisposableBase, ObserverBase, SchedulerBase

from .ping import ping_ips


def ops_ping() -> Callable[
    [rx.Observable[Tuple[str, str]]], rx.Observable[Tuple[Optional[str], Optional[str]]]
]:
    """
    Ping two IP addresses and return the IPs if they are pingable.

    Returns
    -------
    Callable[[rx.Observable[Tuple[str, str]]], rx.Observable[Tuple[Optional[str], Optional[str]]]]
    """

    def _ping(
        source: rx.Observable[Tuple[str, str]]
    ) -> rx.Observable[Tuple[Optional[str], Optional[str]]]:
        def subscribe(
            observer: ObserverBase, scheduler: SchedulerBase = None
        ) -> DisposableBase:
            def on_next(ips: Tuple[str, str]) -> None:
                try:
                    res = ping_ips(ips[0], ips[1])
                    observer.on_next(res)
                except Exception as e:
                    observer.on_error(e)

            return source.subscribe(on_next, observer.on_error, observer.on_completed)

        return rx.create(subscribe)

    return _ping
