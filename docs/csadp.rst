.. _csadp:

Native Search Active Devices Protocol (CSADP)
=============================================

.. automodule:: hiktools.csadp

.. contents:: Table of Contents

CService
~~~~~~~~

.. automodule:: hiktools.csadp.CService

.. autofunction:: hiktools.csadp.CService.l2socket

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

Interface
~~~~~~~~~

Checksum interfaces
-------------------

.. autofunction:: hiktools.csadp.verify

.. autofunction:: hiktools.csadp.checksum

.. autofunction:: hiktools.csadp.from_buf

CSAPDMessages
-------------

.. autofunction:: hiktools.csadp.parse

Packet
------

.. autofunction:: hiktools.csadp.stom

.. autofunction:: hiktools.csadp.mtos

.. autofunction:: hiktools.csadp.stoi

.. autofunction:: hiktools.csadp.itos

.. autofunction:: hiktools.csadp.packet

Enums
~~~~~

.. autoclass:: hiktools.csadp.PacketType

Classes
~~~~~~~

Array
-----

.. autoclass:: hiktools.csadp.Array
  :members:

ByteBuffer
----------

.. autoclass:: hiktools.csadp.ByteBuffer
  :members:


Message
-------

.. autoclass:: hiktools.csadp.CSADPMessage
  :members:

.. autoclass:: hiktools.csadp.EthernetHeader
  :members:
