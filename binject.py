__package__ = "exfil"

import ittybitty

__doc__ = "embed bits in binary"

class Binject:
    """a mechanism for transmitting data in specific bits of binary"""
    ############needs to control the order in which bits are extracted/injected
    ############should the positions be a tuple of (octet, bit) tuples?
    def __init__(self, bit_positions = ()):
        self.bit_positions = bit_positions
    
    def extract(self, packet_generator, trail = False):
        """generate extracted octets from generated packets"""
        dest_index = 0
        octet = ittybitty.BitAccess('\0')
        
        for packet in packet_generator:
            packet = ittybitty.BitAccess(packet)
            
            for bit_position in self.bit_positions:
                octet[dest_index] = packet[bit_position]
                dest_index += 1

                if dest_index == 8:
                    yield str(octet)
                    dest_index = 0
                    octet.clear()
        
        if not str(octet) == '\0' and trail: # yield the trailing bits
            yield str(octet)
    
    def inject(self, packet_generator, src = ''):
        """inject the octets into generated packets"""
        src = ittybitty.BitAccess(src)
        src_index = 0
        
        for packet in packet_generator:
            if src: # avoid unnecessary work
                packet = ittybitty.BitAccess(packet)
                
                for bit_position in self.bit_positions:
                    if src_index >= len(src): # early termination
                        break
                    packet[bit_position] = src[src_index]
                    src_index += 1
                packet = str(packet)
            yield packet
