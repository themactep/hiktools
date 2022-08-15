.. _csadp:

Native Search Active Devices Protocol (CSADP)
=============================================

.. automodule:: hiktools.csadp

.. contents:: Table of Contents

ReadTheDocs build fails on this module. Please refer to the documented source code
to get familiar with this module.

Usage:

.. code:: python

  from hiktools import csadp

  # Because the following module requires root priviledges it 
  # has to be imported directly.
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


