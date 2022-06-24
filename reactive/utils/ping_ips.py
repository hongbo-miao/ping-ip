from .ping import ping


def ping_ips(ip1, ip2):
    res1 = ""
    res2 = ""
    try:
        res1 = ping(ip1)
    except Exception:
        pass
    try:
        res2 = ping(ip2)
    except Exception:
        pass
    return res1, res2
