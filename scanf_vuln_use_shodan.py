
import shodan
api = shodan.Shodan("your_api_key")


def search_vuln(pattern: str, vuln_func):
    try:
        total_num = api.search(pattern)["total"]
        i = 0
        while total_num-i > 100:
            vuln_func(api.search(
                pattern, limit=100, offset=i)["matches"])
            i += 100
        vuln_func(api.search(
            pattern, limit=total_num-i, offset=i)["matches"])
    except shodan.APIError as e:
        print(e)


def find_redis_rce_vuln(results):
    log = open("vuln.txt", "a")
    for i in results:
        redis_info = i["data"]
        if "redis" not in redis_info:
            continue
        redis_version = redis_info.split("redis_version:")[1].split("\r\n")[0]
        if redis_version[0] == "5" or redis_version[0] == "4":
            redis_port = redis_info.split("tcp_port:")[1].split("\r\n")[0]
            ip = i["ip_str"]
            log.write(f"{ip}:{redis_port} {redis_version}\n")
    log.close()


#pattern = "product:redis country:US"
pattern = "product:redis country:UA"
search_vuln(pattern, find_redis_rce_vuln)
# find_redis_rce_vuln()

# except Error as e:
#     print(e)
#     print(redis_info)
