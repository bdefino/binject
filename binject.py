__package__ = __name__

import ittybitty

__doc__ = "embed bits in binary"

class Binject:
    """
    a mechanism for transmitting data in specific bits of binary

    injected bits appear in little-endian order (lowest order bit first)

    specifying alignment means that an octet's bits cannot be split along
    multiple binaries

    trail specifies whether to generate bits whose numbers don't
    make up an entire octet
    """
    
    def __init__(self, positions = (), align = False, trail = False):
        assert not align or len(positions) >= 8, "contradictory arguments"
        self.align = align
        self.positions = positions
        self.trail = trail
    
    def extract(self, generator):
        """generate extracted octets from the generated binaries"""
        dest_index = 0
        octet = ittybitty.BitAccess('\0')
        positions = self.positions

        if self.align:
            positions = positions[:len(positions) / 8 * 8]
        
        for binary in generator:
            binary = ittybitty.BitAccess(binary)
            
            for pos in positions:
                octet[dest_index] = binary[pos]
                dest_index += 1

                if dest_index >= 8:
                    yield str(octet)
                    dest_index = 0
                    octet.clear()
        
        if dest_index > 0 and self.trail: # yield the trailing bits
            yield str(octet)
    
    def inject(self, generator, src = ""):
        """
        inject the octets across the generated binaries

        note that the output binaries will be of the same type as
        the input ones; their type's constructor must be able to
        handle a single bytearray argument
        """
        positions = self.positions

        if self.align:
            positions = positions[:len(positions) / 8 * 8]
        src = ittybitty.BitAccess(src)
        src_index = 0
        
        for binary in generator:
            _type = type(binary) # the expected type of the binary
            
            if src: # avoid unnecessary work
                binary = ittybitty.BitAccess(binary)
                
                for pos in positions:
                    if src_index >= len(src): # early termination
                        break
                    binary[pos] = src[src_index]
                    src_index += 1
                binary = _type(binary)
            yield binary
