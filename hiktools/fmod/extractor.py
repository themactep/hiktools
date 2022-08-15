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
  'export'
]

from .decrypter import DigiCap, FileAccessException
from os import mkdir

def export(dfile: DigiCap, location: str) -> bool:
  """Extracts all files stored in the given digicap file."""
  if not location or not dfile:
    raise ValueError('NullPointerError')

  try:
    mkdir(location)
  except OSError as e:
    raise FileAccessException(e)

  location = location.strip('/')
  for fname, flen, fpos, _ in dfile:
    try:
      with open('/'.join([location, fname]), 'wb') as exp_file:
        exp_file.write(dfile.fread(flen, fpos))
    except OSError as e:
      pass
