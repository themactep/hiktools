import uuid
from xml.etree.ElementTree import Element
import xml.etree.cElementTree as tree

from socket import socket, timeout, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST


PARAM_TIMEOUT = 3 #standard timeout
PARAM_UDP_PORT = 37020
PARAM_UDP_BCAST = '239.255.255.250'
PARAM_BUFFER = 1024

PARAM_XML = '<?xml version="1.0" encoding="utf-8"?>'

def __udp__(xml: str, time_out=PARAM_TIMEOUT, udp_port=PARAM_UDP_PORT, 
        udp_bcast=PARAM_UDP_BCAST, udp_buffer=PARAM_BUFFER) -> list:
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    s.settimeout(time_out)

    print(f"Running with: \n{xml}")
    s.sendto(bytes(xml, 'UTF-8'), (udp_bcast, udp_port))
    response = []
    while 1:
        try:
            response.append(s.recv(udp_buffer))
        except timeout:
            print(f"Received {len(response)} udp packets(s) in {time_out}s timeout window.")
            break
    s.close()
    return response

def __textof__(by) -> str:
    txt = ""
    for line in by:
        txt += bytes.decode(line, 'UTF-8')
    return txt

def __inquiry__(id: str, xml=PARAM_XML) -> str:
    return __base__(id=id, type='inquiry')

def __base__(id: str, type: str, xml=PARAM_XML) -> str:
    return '%s<Probe><Uuid>%s</Uuid><Types>%s</Types></Probe>' % (xml, id, type)

def __base_mac__(id: str, type: str, mac: str, xml=PARAM_XML) -> str:
    return '%s<Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>%s</Types></Probe>' % (xml, id, mac, type)

def __exchangeCode__(id: str, mac: str, code: str, xml=PARAM_XML) -> str:
    return '%s<Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>exchangecode</Types><Code>%s</Code></Probe>' % (xml, id, mac, code)

def __reset__(id: str, mac: str, pwd: str, code: str, xml=PARAM_XML):
    return '%s<Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>reset</Types><Password>%s</Password><Code>%s</Code></Probe>' % (xml, id, mac, pwd, code)

def get_code(code: str) -> str:
    import uuid
    uuid = str(uuid.uuid4()).upper()

    txt = __textof__(__udp__(__exchangeCode__(uuid, '00-00-00-00-00-00', code=code)))
    xml_text = tree.fromstring(txt)
    if xml_text[2].text == 'failed':
        print('Could not get code...')
    else:
        print('Received Code: %s' % (txt))
        print(__textof__(__udp__(__reset__(uuid, '00-00-00-00-00-00', 'NN++OahVKVOZEFnXhxgMSgxKaEZl4VA0klV4I2RZyrA!', 'AwAAADU1ODM4MDEyNB+ZYT8=qSQRrSRSRe'))))
    

#rint(len('MIGJAoGBAJlIr+kLf/dY7nPHQ0CEGjb3i8ClJpt38cnxIpdCZ14KxYYxUDVmZ5GTHh3Wrh2209EXCSQ7OZfosL/5XKBTsT+lA3+IwEMCf9BaIfCU+SuVS2N7fY6yfx1AYhE+8TRd2cna4b3rYi2fRHrJXLiUjRVWUqD+b8f95+sxjhOVDMMDAgMBAAE='))
uuid = str(uuid.uuid4()).upper()
print(__textof__(__udp__('<?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>getBindList</Types></Probe>' % (uuid, '00-00-00-00-00-00'))))

get_code('MIGJAoGBAJlIr+kLf/dY7nPHQ0CEGjb3i8ClJpt38cnxIpdCZ14KxYYxUDVmZ5GTHh3Wrh2209EXCSQ7OZfosL/5XKBTsT+lA3+IwEMCf9BaIfCU+SuVS2N7fY6yfx1AYhE+8TRd2cna4b3rYi2fRHrJXLiUjRVWUqD+b8f95+sxjhOVDMMDAgMBAAE=')

    