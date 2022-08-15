namespace CSADP {

/**
 * @brief A small checksum generator for SADP Packets (Disassebled with Ghidra).
 *  
 * The call which is done in BuildSADPPacket() is the following:
 * 
 *  uVar7 = Checksum(
 *    *(ushort **)(buffer + 0x14), 
 *    (uint)*(byte *)((int)*(ushort **)(buffer + 0x14) + 3)
 *  );
 * 
 * Note, that the conversion to unsigned short * will produce a pointer that combine 
 * two bytes each position. Therefore, +3 at the end has the following effect:
 * 
 *  ubyte *buf = [0x10, 0x20, 0x30, 0x40];
 *  ushort *dest = (ushort *)buf;
 *  //           = [0x1020, 0x3040] 
 *
 * The next step is to convert the returned unsigned short value into a single byte value:
 * 
 *  ushort *buf = [0x1020, 0x3040]
 *  byte dest = *((byte *)buf)
 *  //        = 0x10
 * 
 * @param buffer 
 * @param counter 
 * @return unsigned int
 */
unsigned int __cdecl Checksum(unsigned short *buffer, unsigned int counter) 
{
  // ┌───────────────────────────────────────────────┐
  // │Buffer Structure                               │
  // ├─────────┬─────────┬─────┬─────┬─────────┬─────┤
  // │0x21 0x02│0x01 0x42│.. ..│.. ..│0x06 0x04│.. ..│
  // └─────────┴─────────┴─────┴─────┴─────────┴─────┘
  //                0      1       2     3       4       5

  int iVar1 = 0;
  int iVar2 = 0;
  int iVar3 = 0;
  int result = 0;
  int iVar2_temp = 0;

  if (3 < (counter & 0xFFFFFFFE)) {
    iVar3 = ((counter - 4) >> 2) + 1;
    do {
      counter -= 4;
      iVar1 += ((unsigned int) *buffer); 
      iVar2 = iVar2_temp + ((unsigned int)buffer[1]); 

      buffer = buffer + 2; 
      iVar3 -= 1; 
      iVar2_temp = iVar2; 
    } while (iVar3 != 0);
  }
  if (1 < counter) {
    result = (unsigned int)*buffer;
    buffer = buffer + 1;
    counter -= 2;
  }
  
  result += iVar2 + iVar1;
  if (counter != 0x00) {
    result += *((unsigned char *)buffer);
  }
  result = (result >> 16) + (result & 0xFFFF); 
  
  return (unsigned int) ~((result >> 16) + result); 
}

}