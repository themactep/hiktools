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
  'Array', 'verify', 'checksum', 'from_buf', 'from_counter',
  'c_uint16', 'c_uint32', 'c_uint8'
]

from typing import Iterator, Sequence, TypeVar, Generic, overload
from ctypes import c_uint32, c_uint16, c_uint8
from socket import ntohs, ntohl

T_B = TypeVar('T_B', c_uint16, c_uint32, c_uint8, int)

class Array(Generic[T_B]):
  """A simple generic array wrapper.
  
  This class is used to convert byte arrays into unsigned short arrays - 
  (uint16 arrays). It can also be used to create c_uint8, c_uint32 and
  int arrays.
  """
  def __init__(self, values: Sequence[T_B]) -> None:
    super().__init__()
    self._items = []
    for value in values:
      self._items.append(value)
  
  def __getitem__(self, index: int) -> T_B:
    if type(index) == slice: return Array(self._items[index])
    if 0 <= index < len(self._items): 
      return self._items[index]
    else:
      return 0x00
  
  def __setitem__(self, index: int, value: T_B):
    self._items[index] = value
  
  def __len__(self) -> int:
    return len(self._items)
  
  def __iter__(self) -> Iterator[T_B]:
    return iter(self._items)

  @staticmethod
  def b2a16(buffer: bytes) -> 'Array':
    """Converts a byte buffer into an uint16 array."""
    seq = []
    for i in range(0, len(buffer), 2):
      seq.append(buffer[i+1] & 0xFF | buffer[i] << 8)
    return Array(seq)

def checksum(buffer: Array[c_uint16], counter: c_uint16) -> int:
  """Computes a checksum from the given SADP packet and the base counter.
  
  Note: This algorithm was converted from decompiled C source code and does not
  work yet. Improvents are greatly appreciated.
  
  Arguments:
    buffer: Array[c_uint16]
      A buffer of c_uin16 instances.
    counter: c_uin16
      An unsigned short value representing the current counter.
      
  Returns: int
    The generated checksum.
  """
  iVar1 = 0
  iVar2 = 0
  iVar3 = 0
  result = 0

  if 3 < (counter & 0xFFFFFFFE):
    iVar3 = (counter - 4 >> 2) + 1
    # if iVar3 > 3:
    #   raise NotImplementedError('Counters higher that 0x0d are not supported yet!')

    while iVar3 != 0:
      counter -= 4
      iVar1 += c_uint32(buffer[0]).value
      iVar2 += c_uint32(buffer[1]).value

      buffer = buffer[2:]
      iVar3 -= 1
    
  if 1 < counter:
    result = buffer[0]
    buffer = buffer[1:]
    counter -= 2

  result += c_uint32(iVar2 + iVar1).value
  if counter != 0:
    result += c_uint8(buffer[0]).value
  
  result = (result >> 0x10) + (result & 0xFFFF) 
  result = c_uint16(~((result >> 0x10) + result)).value
  return result

def from_counter(counter: int, p_type: int = 0x300) -> int:
  """Generates a checksum from the given counter: DEPRECATED"""
  counter = ntohs(counter)
  array = Array([0x0221, 0x4201, 0x0000, counter, 0x0604, p_type, 0x0000])
  return checksum(array, counter & 0xFF)

def from_buf(buffer: bytes) -> int:
  """Generates a checksum from the given buffer (contains the counter)."""
  array = Array.b2a16(buffer)
  counter = array[3] >>8& 0xFF
  return checksum(array, counter)

@overload
def verify(received: int, counter: bytes) -> bool: ...
def verify(received: int, counter: int) -> bool:
  """Verifies the received checksum: DEPRECATED"""
  checksum = from_counter(counter) if type(counter) == int else from_buf(counter)
  if checksum != received:
    raise ValueError('Invalid Checksum: %d != %d' % (received, checksum))
