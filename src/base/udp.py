from socket import socket, timeout, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

PARAM_TIMEOUT = 2 #standard timeout
PARAM_UDP_PORT = 37020
PARAM_UDP_BCAST = '239.255.255.250'
PARAM_BUFFER = 1024

PARAM_XML = '<?xml version="1.0" encoding="utf-8"?>'

class XmlRequest(object):
    def __init__(self) -> None:
        super().__init__()

        self.asstring = PARAM_XML + '<Probe>' # this is a must
    
    def __add__(self, node: str, value: str):
        if node and value:
            self.asstring += f'<{node}>{value}</{node}>'

    def __create__(self) -> str:
        return self.asstring + '</Probe>'

    def clear(self):
        self.asstring = PARAM_XML + '<Probe>'
        
def __udp__(xml: str, time_out=PARAM_TIMEOUT, udp_port=PARAM_UDP_PORT, 
        udp_bcast=PARAM_UDP_BCAST, udp_buffer=PARAM_BUFFER) -> list:
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.settimeout(time_out)

    print(f"Running with: \n{xml}\n")
    s.sendto(bytes(xml, 'UTF-8'), (udp_bcast, udp_port))
    response = []
    while 1:
        try:
            response.append(s.recv(udp_buffer))
        except timeout:
            print(f"Received {len(response)} udp packets(s) in {time_out}s timeout window.\n")
            break
    s.close()
    return response

def __textof__(by) -> str:
    txt = ""
    for line in by:
        txt += bytes.decode(line, 'UTF-8')
    return txt

#rint(len('MIGJAoGBAJlIr+kLf/dY7nPHQ0CEGjb3i8ClJpt38cnxIpdCZ14KxYYxUDVmZ5GTHh3Wrh2209EXCSQ7OZfosL/5XKBTsT+lA3+IwEMCf9BaIfCU+SuVS2N7fY6yfx1AYhE+8TRd2cna4b3rYi2fRHrJXLiUjRVWUqD+b8f95+sxjhOVDMMDAgMBAAE='))
#print(__textof__(__udp__('<?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>getBindList</Types></Probe>' % (uuid, '00-00-00-00-00-00'))))


    