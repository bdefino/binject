# Copyright (C) 2018 Bailey Defino
# <https://bdefino.github.io>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__doc__ = "itty bitty ops on bits"

class BitAccess:
    """faculty for easy manipulation of a bit array"""
    
    def __init__(self, octets = ''):
        self._current = 0
        
        if not isinstance(octets, bytearray):
            octets = bytearray(octets)
        self.octets = octets

    def clear(self):
        """zero out the bits"""
        for i in range(len(self.octets)):
            self.octets[i] = 0
    
    def __getitem__(self, i):
        return (self.octets[i / 8] >> (i % 8)) & 1
    
    def getoctet(self, i):
        return self.octets[i]

    def __iter__(self):
        return self
    
    def __len__(self):
        return len(self.octets) * 8

    def next(self):
        if self._current >= len(self.octets) << 3:
            raise StopIteration()
        bit = self.__getitem__(self._current)
        self._current += 1
        return bit
    
    def __setitem__(self, i, high):
        assert high in (0, 1), "high must evaluate to either 0 or 1"
        shift = i % 8
        octet = self.octets[i / 8] & ~(1 << shift) # zero out indexed bit
        self.octets[i / 8] = octet | (high << shift)
    
    def setoctet(self, i, value):
        self.octets[i] = value & 255

    def __str__(self):
        return str(self.octets)

    def value(self, i):
        """return the value of an indexed bit within its corresponding octet"""
        return self.octets[i / 8] & (1 << (i % 8))
