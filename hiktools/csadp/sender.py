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
  'ByteBuffer', 'stom', 'mtos', 'itos', 'stoi',
  'packet'
]

import binascii
import socket
import ctypes

class ByteBuffer:
  """A bytes like class implementing utility methods for creating buffers.
  
  This class contains a read only sequence behaviour.
  """
  def __init__(self, size: int = 0) -> None:
    super().__init__()
    self._items = [0x00 for _ in range(size)]
  
  def __getitem__(self, index: int) -> int:
    return self._items[index]
  
  def __setitem__(self, index: int, value: int):
    self._items[index] = value
  
  def __len__(self) -> int:
    return len(self._items)
  
  def __iter__(self):
    return iter(self._items)

  def insert_bytes(self, buf: bytes, offset: int = 0):
    """Inserts the given bytes starting at the given offset."""
    for i, val in enumerate(buf):
      self._items.insert(offset+i, val)

  def __iadd__(self, buf: bytes) -> 'ByteBuffer':
    for i in buf:
      self._items.append(i)
    return self
  
  def __bytes__(self) -> bytes:
    """Returns the bytes version of this object"""
    return bytes(self._items)

def stom(mac: str, buffer: ByteBuffer, index: int):
  """Inserts the string mac address into the given buffer."""
  buffer.insert_bytes(binascii.unhexlify(mac.replace(':', '').replace('-', '')), index)

def mtos(buffer: bytes, index: int) -> str:
  """Converts bytes to a MAC address."""
  return binascii.b2a_hex(buffer[index:index+6], sep=':').decode('utf-8')

def stoi(ip: str, buffer: ByteBuffer, index: int):
  """Inserts the string ip address into the given buffer."""
  buffer.insert_bytes(socket.inet_aton(ip), index)

def itos(buffer: bytes, index: int):
  """Converts bytes to an IP address."""
  return socket.inet_ntoa(buffer[index:index+4])

def _pack_into(buffer: ByteBuffer, value: int, nBits: type, index: int):
  if nBits == ctypes.c_uint8:
    buffer[index] = value & 0xFF
  elif nBits == ctypes.c_uint16:
    buffer[index] = (value >> 8) & 0xFF
    _pack_into(buffer, value, ctypes.c_uint8, index+1)
  elif nBits == ctypes.c_uint32:
    _pack_into(buffer, value >> 16, ctypes.c_uint16, index)
    _pack_into(buffer, value, ctypes.c_uint16, index+2)

def packet(current_mac: str, current_ip: str, query_type: int, counter: int, 
           payload: bytes, query_params: int = 0, checksum: int = 0, 
           dest_mac: str = 'ff:ff:ff:ff:ff:ff', dest_ip: str = '0.0.0.0',
           subnet: str = '0.0.0.0') -> bytes:
  """Creates a new CSADPPacket (bytes).

  Arguments:
    counter: int
      internal counter to compute the checksum
    query_type: int
      query type 
    query_params: int
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

  Returns: bytes
    A byte buffer covering all relevant message bytes.
  """
  checksum = ctypes.c_uint32(checksum)
  counter = ctypes.c_uint32(counter)
  query_type = ctypes.c_uint8(query_type)
  query_params = ctypes.c_uint8(query_params)

  # CheckSum.verify(checksum.value, counter.value)
  buffer = ByteBuffer(size=0x200)

  stom(dest_mac, buffer, 0)
  stom(current_mac, buffer, 6)

  start = 14
  ether_type = 0x8033
  _pack_into(buffer, ether_type, ctypes.c_uint16, 12)
  _pack_into(buffer, 0x21020142, ctypes.c_uint32, start)
  _pack_into(buffer, counter.value, ctypes.c_uint32, start+4)
  _pack_into(buffer, 0x0604, ctypes.c_uint16, start+8)
  _pack_into(buffer, query_type.value, ctypes.c_uint8, start+10)
  _pack_into(buffer, query_params.value, ctypes.c_uint8, start+11)
  _pack_into(buffer, checksum.value, ctypes.c_uint32, start+12)

  stom(current_mac, buffer, start+14)
  stoi(current_ip, buffer, start+20)
  stom(dest_mac, buffer, start+24)
  stoi(dest_ip, buffer, start+30),
  stoi(subnet, buffer, start+34)
  buffer.insert_bytes(payload, start + 38)
  
  buffer_len = start + 38 + len(payload)
  if buffer_len < 80:
    buffer_len = 80
  
  result = bytes(buffer[:buffer_len])
  del buffer
  return result
