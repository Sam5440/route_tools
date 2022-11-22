#老毛子路由器端口转发转openwrt格式
#vslist自己抓包获得
VSList = [
    ["1688", "192.168.123.1", "1688", "UDP", "", "", "Kms"],
    ["48440", "192.168.123.46", "3389", "BOTH", "", "", ""],
    ["9000", "192.168.123.46", "", "BOTH", "", "", "parsec"],
    ["1723", "192.168.123.1", "", "BOTH", "", "", "parsec"],
    ["8000:8011", "192.168.123.46", "", "BOTH", "", "", "parsec"],
]


# 按端口大小排序
VSList.sort(key=lambda x: int(x[0].split(":")[0]))
# print(VSList)

demo_str = """config redirect
	option target 'DNAT'
	option proto 'tcp udp'
	option src_dport 'out_port'
	option dest_ip 'inner_ip'
	option dest_port 'inner_port'
	option name 'server_name'
	option src 'lan'
	option dest 'lan'
	list src_mac 'main_mac'
"""
# 主路由mac地址,需要指定,不然会转发这个端口全部的流量,
main_mac = "5C:02:14:5D:4A:7E"
demo_str = demo_str.replace('main_mac', main_mac)   
result = ""
for s in VSList:
    out_port = s[0]
    inner_ip = s[1]
    inner_port = s[2] if s[2] else out_port
    server_name = s[6] if s[6] else f"Forward{out_port}"
    result += str(
        demo_str.replace("out_port", out_port)
        .replace("inner_ip", inner_ip)
        .replace("inner_port", inner_port)
        .replace("server_name", server_name)
    )
#result写入config.txt文件
with open("config.txt", "w") as f:
    f.write(result)
