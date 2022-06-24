IP_ADDRESS_1 = "192.168.1.0/24"
IP_ADDRESS_2 = "192.168.2.0/24"

# Retry times for ping if the IP is not pingable
RETRY_ATTEMPTS = 3

# Allow specific IP addresses to be skipped based on their last octet,
# so for example we can exclude 192.168.1.56 and 192.168.2.56 by specifying 56
SKIP_LIST = ["56"]
