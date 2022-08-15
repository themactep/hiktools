# MIT License
# 
# Copyright (c) 2022 MatrixEditor
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
__all__ = [
  'EthernetHeader', 'PacketType', 'CSADPMessage',
  'parse'
]

import ctypes
import struct
import enum

from . import itos, mtos, packet, stom

class EthernetHeader:
  """Small wrapper for raw ethernet message headers."""
  def __init__(self, dest_mac: str, src_mac: str, eth_type: int) -> None:
    self._dest_mac = dest_mac 
    self._src_mac = src_mac 
    self._eth_type = eth_type 

  @property
  def destination(self) -> str:
    """The destination MAC address."""
    return self._dest_mac

  @property
  def source(self) -> str:
    """The source MAC address."""
    return self._src_mac

  @property
  def eth_type(self) -> str:
    """EtherType: 0x8033"""
    return self._eth_type
  
  def __bytes__(self) -> bytes:
    buffer = bytearray()
    stom(self.destination, buffer, 0)
    stom(self.source, buffer, 6)
    buffer[12] = self.eth_type >> 8 & 0xFF
    buffer[13] = self.eth_type & 0xFF
    return bytes(buffer[:14])

class PacketType(enum.Enum):
  """See sadp.lua for explaination of the packet types."""
  REQUEST = 0x02
  RESPONSE = 0x01

  @staticmethod
  def valueof(value: int) -> 'PacketType':
    for xy in PacketType:
      if xy == value:
        return xy

class CSADPMessage:
  """An object representation of the SADPPacket byte version.
  
  Attributes:
    header: EthernetHeader
      The ethernet frame header at the front.
    pkt_type: int
      either 0x01 or 0x02
    counter: int
      internal counter to compute the checksum
    qry_type: int
      query type 
    qry_params: int
      query parameters
    checksum: int
      the calculated checksum
    payload: bytes
      raw payload section
    current_mac: str
      sender MAC address
    current_ip: str
      sender IP address
    dest_mac: str
      destination MAC address
    dest_ip: str
      destination IP address
    subnet: str
      subnet mask
  """
  def __init__(self, header: EthernetHeader = None, pkt_type: PacketType = PacketType.REQUEST,
               counter: int = 0, query_type: int = 0, query_params: int = 0,
               checksum: int = 0, payload: bytes = None, current_mac: str = "ff:ff:ff:ff:ff:ff", 
               current_ip: str = "0.0.0.0", dest_mac: str = "ff:ff:ff:ff:ff:ff", 
               dest_ip: str = "0.0.0.0", subnet: str = "0.0.0.0") -> None:
    self.header = header
    self.pkt_type = pkt_type
    self.counter = ctypes.c_uint32(counter)
    self.qry_type = ctypes.c_uint8(query_type)
    self.qry_params = ctypes.c_uint8(query_params)
    self.checksum = ctypes.c_uint32(checksum)
    self.payload = payload if payload else bytes([])
    self.current_mac = current_mac
    self.current_ip = current_ip
    self.dest_mac = dest_mac
    self.dest_ip = dest_ip
    self.subnet = subnet

  def __bytes__(self) -> bytes: 
    return packet(self.current_mac, self.current_ip, self.qry_type,
                  self.counter, self.payload, self.qry_params,
                  self.checksum, self.dest_mac, self.dest_ip,
                  self.subnet)
  
  def __repr__(self) -> str:
    return '<SADP from="%s" to="%s">' % (self.current_mac, self.dest_mac)

def parse(buffer: bytes) -> CSADPMessage:
  """Converts the input buffer into a CSADPMessage object.
  
  Arguments:
    buffer: bytes
      The received or packed bytes.
  
  Returns: CSADPMessage
    An object containing all relevant packet information.
  """
  message = CSADPMessage()
  if buffer is None or len(buffer) == 0:
    return message

  message.header = EthernetHeader(
    mtos(buffer, 0),
    mtos(buffer, 6),
    struct.unpack('!H', buffer[12:14])[0]
  )
  
  tp, _, _, c, _, qt, qp, csum = struct.unpack('!BBBIHBBH', buffer[15:28])
  message.pkt_type = PacketType.valueof(tp)
  message.counter = ctypes.c_uint32(c)
  message.qry_type = ctypes.c_uint8(qt)
  message.qry_params = ctypes.c_uint8(qp)
  message.checksum = ctypes.c_uint32(csum)

  message.current_mac = mtos(buffer, 28)
  message.current_ip = itos(buffer, 34)
  message.dest_mac = mtos(buffer, 38)
  message.dest_ip = itos(buffer, 44)
  message.subnet = itos(buffer, 48)

  message.payload = buffer[52:]
  return message
