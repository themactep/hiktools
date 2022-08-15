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
  'InvalidFileFormatException', 'FileAccessException', 'DigiCapHeader',
  'read_raw_header', 'decode_xor16', 'split_header', 'split_files',
  'fopen_dav', 'DigiCap'
]

from ctypes import c_uint32, c_uint8
from io import TextIOWrapper
from typing import Generator, Iterator, overload

###############################################################################
# Exception Classes
###############################################################################
class InvalidFileFormatException(Exception):
  """Base class for DAV file exceptions."""
  pass

class FileAccessException(Exception):
  """Base class for permission related issues."""
  pass

###############################################################################
# Data Types
###############################################################################
BIG_ENDIAN = 0x01
LITTLE_ENDIAN = 0x02

def uint32(value: bytes, encoding: int = LITTLE_ENDIAN) -> c_uint32:
  if type(value) == bytes:
    if encoding == BIG_ENDIAN:
      return c_uint32(value[0] << 24 | value[1] << 16 | value[2] << 8 | value[3])
    elif encoding == LITTLE_ENDIAN:
      return c_uint32(value[0] | value[1] << 8 | value[2] << 16 | value[3] << 24)
    else:
        raise ValueError('Unexpected Encoding!')

def uint24(value: bytes, encoding: int = LITTLE_ENDIAN) -> int:
  if type(value) == bytes:
    if encoding == BIG_ENDIAN:
      return value[0] << 16 | value[1] << 8 | value[2]
    elif encoding == LITTLE_ENDIAN:
      return value[0] | value[1] << 8 | value[2] << 16
    else:
      raise ValueError('Unexpected Encoding!')

@overload
def uint8(value: int) -> c_uint8: ... 
def uint8(value: bytes) -> c_uint8:
  if type(value) == bytes:
    return c_uint8(value[0])
  else:
    return c_uint8(value & 0xFF)

class DigiCapHeader:
  """A class covering important configuration information.
  
  Attributes:
    magic: c_uint32
      magic header bytes indicating the used firmware
    header_checksum: c_uint32
      unused.
    header_length: c_uint32
      The header length is used to indicate the end of the filesystem index.
    files: c_uint32
      The amount of files stored in this firmware image.
    language: c_uint32
      The used language
    device_class: c_uint32
      unidentified
    oem_code: c_uint32
      maybe system verfication key
    signature: c_uint32
      unidentified
    features: c_uint32
      unidentified
  """
  def __init__(self, magic: c_uint32 = 0x00, header_checksum: c_uint32 = 0x00, 
               header_length: c_uint32 = 0x00, files: c_uint32 = 0x00, 
               language: c_uint32 = 0x00, device_class: c_uint32 = 0x00, 
               oem_code: c_uint32 = 0x00, signature: c_uint32 = 0x00, 
               features: c_uint32 = 0x00) -> None:
    self.magic = magic
    self.header_checksum = header_checksum
    self.header_length = header_length
    self.files = files
    self.language = language
    self.device_class = device_class
    self.oem_code = oem_code
    self.signature = signature
    self.features = features

  def __repr__(self) -> str:
    return '<DigiCapHeader length=%d, files=%d>' % (self.header_length, self.files)

###############################################################################
# Funtions
###############################################################################
def fopen_dav(file_name: str, mode: str = 'rb') -> TextIOWrapper:
  """Opens a file with te 'dav' extension.
  
  Arguments:
    file_name: str
      The absolute or relative path to the file
    mode: str
      The mode this file shoul be opened with (either 'r' or 'rb')
  
  Raises:
    InvalidFileFormatException :
      on invalid file extension
    ValueError:
      on invalid argument values
    FileAccessException:
      if there are issues with open the file
  
  Returns: TextIOWrapper
    A file reader instance.
  """
  if not file_name or not file_name.endswith('dav'):
    raise InvalidFileFormatException('Expected a *.dav file on input.')
  
  if not mode or mode not in ['r', 'rb']:
    raise ValueError('Expected a reading mode.')

  try:
    _res = open(file_name, mode)
  except OSError as open_error:
    raise FileAccessException(open_error)
  else:
    if _res is None or not _res:
      raise FileAccessException('Unable to open *.dav file')
    else:
      return _res

@overload
def read_raw_header(resource: str) -> bytes: ...
def read_raw_header(resource: TextIOWrapper) -> bytes:
  """Reads the first 108 bytes from the resource stream."""
  if type(resource) == str:
    resource = fopen_dav(resource, 'rb')
  
  if not resource or not resource.mode == 'rb':
    raise ValueError('Expected a reading bytes mode resource.')
  
  buf_len = 0x6c # 108 bytes
  try:
    buffer = resource.read(buf_len)
  except OSError as error:
    raise FileAccessException(error)
  else:
    return buffer

def decode_xor16(buffer: bytes, key: bytes, length: int) -> bytes:
  """Decodes (XOR) the given buffer with a key."""
  result = bytearray()
  key_byte = 0x00

  if length > 0 or len(key) != 0xF:
    for index in range(length):
      key_byte = key[index + (index >> 4) & 0xF]
      result.append(key_byte ^ buffer[index])
  
  return bytes(result)

def split_header(buffer: bytes) -> DigiCapHeader:
  """"Extracts information from the decoded firmware header."""
  if not buffer or len(buffer) == 0:
    raise ValueError('Invalid buffer object len() == 0 or object is None.')  
  
  # REVISION: maybe add magic value check to validate the right firmware
  # file is going to be inspected.
  magic = uint32(buffer)
  header_checksum = uint32(buffer[4:8])
  header_length = uint32(buffer[8:12])
  files = uint32(buffer[12:16])
  language = uint32(buffer[16:20])
  device_class = uint32(buffer[20:24])
  oem_code = uint32(buffer[24:28])
  signature = uint32(buffer[28:32])
  features = uint32(buffer[32:36])

  checksum = uint8(buffer[8]) + (uint24(buffer[9:12]) * 0x100)
  if checksum != header_length:
    raise InvalidFileFormatException('Invalid header size: expected %d' % checksum)
  
  return DigiCapHeader(
    magic, header_checksum, header_length, files, language,
    device_class, oem_code, signature, features
  ) 

@overload
def split_files(buffer: TextIOWrapper, length: int = 0x0) -> Generator[tuple, None, None]: ...
def split_files(buffer: bytes, length: int = 0x40) -> Generator[tuple, None, None]:
  """Iterates over all files located in the given filesystem index."""
  if type(buffer) != bytes:
    if not buffer or not buffer.mode == 'rb':
      raise ValueError('Expected a reading bytes mode resource.')
    
    if length <= 0:
      raise ValueError('Expected a length > 0.')

    buffer.seek(0, 0)
    buffer = buffer.read(length)
  
  index = 0x40
  amount = uint32(buffer[12:16])
  for _ in range(amount):
    file_name = buffer[index:index+32].replace(b'\x00', b'')
    index += 32
    
    file_length = uint32(buffer[index:index+4])
    file_pos = uint32(buffer[index+4:index+8])
    file_checksum = uint32(buffer[index+8:index+12])
    index += 12
    yield file_name.decode('utf-8'), file_length, file_pos, file_checksum

###############################################################################
# Classes
###############################################################################
class DigiCap:
  """The base class for operating with digicap.dav files."""
  
  
  KEY_XOR = b'\xBA\xCD\xBC\xFE\xD6\xCA\xDD\xD3\xBA\xB9\xA3\xAB\xBF\xCB\xB5\xBE'
  """The key used to encrypt/decrypt the firmware files."""

  @overload
  def __init__(self, resource: TextIOWrapper = None) -> None: ...
  def __init__(self, resource: str = None) -> None:
    self._file = None
    self._name = None
    self._filelist = []
    self._len = 0
    self._head = None

    if resource is not None:
      if type(resource) == str:
        if not self.fopen(resource):
          raise InvalidFileFormatException('Invalid input file: %s' % resource)

      elif type(resource) == TextIOWrapper:
        self._file = resource
        self._name = resource.name
      else:
        raise ValueError('Invalid argument type: %s' % resource.__class__.__name__)

  def fopen(self, resource: str) -> bool:
    """Opens the given resource. 

    Will be called automatically when this class is used in a with statement.
    """
    if resource is not None:
      self._file = fopen_dav(resource)
      self._name = resource 
      return True

  def fclose(self):
    """Closes the current file reader. 

    Will be called automatically when this class is used in a with statement.
    """
    self._file.close()

  def reset(self) -> bool:
    """Sets the reader's position to the start of the stream."""
    self._file.seek(0, 0)
    return self._file.seekable()

  def fread(self, length: int, offset: int = -1) -> bytes:
    """Reads the given amount of bytes from the underlying stream."""
    if self._file.closed:
      raise ValueError('FileInoutStream is closed!')
    
    if offset >= 0: self._file.seek(offset)
    return self._file.read(length)

  def fparse(self):
    """Parses the firmware file."""
    if self._file is not None:
      raw_head = read_raw_header(self._file)
      decoded_head = decode_xor16(raw_head, self.KEY_XOR, 0x6c)

      self._head = split_header(decoded_head)
      self.reset()
      raw_data = decode_xor16(
        self._file.read(self.head.header_length), 
        self.KEY_XOR, 
        self.head.header_length
      )
      self._filelist = [x for x in split_files(raw_data)]
    else:
      raise ValueError('Input source is None.')

  @property
  def name(self) -> str:
    """The file name (absolute or relative)"""
    return self._name
  
  @property
  def head(self) -> DigiCapHeader:
    """The header object storing important configuration data."""
    return self._head
  
  def __enter__(self) -> 'DigiCap':
    self.fparse()
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    self.fclose()
    if exc_value is not None:
      raise exc_value

  def __len__(self) -> int:
    return len(self._filelist) if not self._len else self._len 

  def __iter__(self) -> Iterator[tuple]:
    return iter(self._filelist)

  def __getitem__(self, index: int) -> tuple:
    return self._filelist[index]

  def __repr__(self) -> str:
    return '<DigiCap file="%s">' % self._name


