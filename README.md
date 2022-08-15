# Hiktools

![Module](https://img.shields.io:/static/v1?label=Module&message=hiktools&color=9cf)
![Build](https://img.shields.io:/static/v1?label=Python&message=>=3.5&color=green)
![Platform](https://img.shields.io:/static/v1?label=Platforms&message=Linux|Windows&color=yellowgreen)

This respository was former known as `hikvision-sdk-cam`, but has changed since the old content of this repository was deleted. This is now a small project with four main functionalities: 
* A Wireshark dissector for the Search Active Devices Protocol,
* Decrypt and extract hikvision firmware, 
* Send raw SADP packets (only Linux) and 
* Send commands via UDP Broadcast. 

To get familiar with the API provided in this repository, take a quick look at the documentation available **[here »]()**

### Overview
---
Unfortunately, the SADP packet creation does not work properly due to invalid checksum calculation. The disassembled source code for its algorithm is given in [Checksum.cpp](/gists/csadp/CheckSum.cpp). Therefore, a simple alternative with a pre-calculated checksum is used until the algorithm works. You can disassemble [this](/gists/libsadp.so) shared object library and try it yourself.

> Source code of the packet creation method is provided in [CPacketSender.cpp](/gists/csadp/CPacketSender.cpp).

Communication on UDP works fine at the moment - this API is just a small wrapper which can be used for a more general API. 

Firmware decryption and extraction will onl work on newer `digicap.dav` files with more than `1` file entry in the header. All firmware files and updates can be downloaded from the following endpoint (EU):

* https://www.hikvisioneurope.com/uk/portal

There is also a full list of files available at this enpoint stored in a JSON file named [firmwarelist.json](/gists/firmwarelist.json).

> Info: There is an interesting file located in the extracted files of a firmware image: /hroot.img/initrd/etc/passwd. A password is set to the root user:

    Name: passwd
    Folder: -
    Size: 44
    Packed Size: 1 024
    Mode: -rwxrwxr-x
    Last change: 2016-12-23 08:27:46
    Last modification: 2016-12-23 08:27:46
    -------------------------------------------

    root:ToCOv8qxP13qs:0:0:root:/root/:/bin/psh

Yet, the usage of this password is still unknown -> telnet and ssh-shell did not accept it. Login as root on the device web login page also did not work.

> Old exploit with authkey := YWRtaW46MTEK

### Basic Usage
---

- Firmware inspection and extraction

```python
from hiktools import fmod

# Open the resource at the specified path (loading is done automatically)
# or manually decrypt the firmware file (see documentation for actual code).
with fmod.DigiCap('filename.dav') as dcap:
  # Iterate over all files stored in the DigiCap object
  for file_info in dcap:
      print('> File name="%s", size=%d, pos=%d, checksum=%d' % file_info)

  # get file amount and current language
  print("Files: %d, Language: %d" % (dcap.head.files, dcap.head.language))

  # save all files stored in <filename.dav>
  fmod.export(dcap, "outdir/")
```

- Native interface on sending raw packets (only LINUX)
```python
from hiktools import csadp

# Because the following module requires root priviledges it has to be 
# imported directly
from hiktools.csadp import CService

sock = CService.l2socket('wlan0')
counter = 2855

# Building an inquiry packet
packet = csadp.packet(
  'src_mac', 'src_ip', 0x03, counter, 
  checksum=csadp.from_counter(counter),
  payload='\x00'*28
)

# If you want to have the packet as an object use parse()
packet_obj = csadp.parse(packet)

sock.send(packet) # or sock.send(bytes(packet_obj))
response = csadp.parse(sock.recv(1024))
```

- Interact with the device through UDP broadcast
```python
from hiktools import sadp
from uuid import uuid4

# create a packet from a simple dict object
inquiry = sadp.fromdict({
  'Uuid': str(uuid4()).upper(),
  'MAC': 'ff-ff-ff-ff-ff-ff',
  'Types': 'inquiry'
})

# Open up a client to communicate over broadcast
with sadp.SADPClient() as client:
  # send the inquiry packet
  client.write(inquiry)

  # iterate over all received packets (None is returned on error)
  for response in client:
    if response is None: break
    # initiate the response
    message = sadp.unmarhal(response.toxml())

    # message objects contain a dict-like implementation
    for property_name in message:
      print(message[property_name]) 
    
    # e.g.
    print('Device at', message['IPv4Address'])
```