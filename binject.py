__package__ = "binject"

import ittybitty

__doc__ = "embed bits in binary"

class Binject:
    """a mechanism for transmitting data in specific bits of binary"""
    ############needs to control the order in which bits are extracted/injected
    ############should the positions be a tuple of (octet, bit) tuples?
    def __init__(self, positions = ()):
        self.positions = positions
    
    def extract(self, generator, trail = False):
        """generate extracted octets from the generated binaries"""
        dest_index = 0
        octet = ittybitty.BitAccess('\0')
        
        for binary in generator:
            binary = ittybitty.BitAccess(binary)
            
            for pos in self.positions:
                octet[dest_index] = binary[pos]
                dest_index += 1

                if dest_index == 8:
                    yield str(octet)
                    dest_index = 0
                    octet.clear()
        
        if not str(octet) == '\0' and trail: # yield the trailing bits
            yield str(octet)
    
    def inject(self, generator, src = ''):
        """
        inject the octets across the generated binaries

        note that the output binaries will be of the same type as
        the input ones; their type's constructor must be able to
        handle a single bytearray argument
        """
        src = ittybitty.BitAccess(src)
        src_index = 0
        
        for binary in generator:
            _type = type(binary) # the expected type of the binary
            
            if src: # avoid unnecessary work
                binary = ittybitty.BitAccess(binary)
                
                for pos in self.positions:
                    if src_index >= len(src): # early termination
                        break
                    binary[pos] = src[src_index]
                    src_index += 1
                binary = _type(binary)
            yield binary
