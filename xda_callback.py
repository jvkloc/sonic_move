"""
Jonne Klockars 2023
HUMEA Lab

Class for handling incoming data from sensors.
"""

from threading import Lock
# https://www.movella.com/support/software-documentation
import xsensdeviceapi as xda


class XdaCallback(xda.XsCallback):

    def __init__(self, max_buffer_size = 5):
        """max_buffer_size defines the maximum length 
        of the data packet list. Default is 5.
        """        
        
        xda.XsCallback.__init__(self)
        self.max_buffered_packets = max_buffer_size
        self.packet_buffer = []
        self.lock = Lock()

    def packet_available(self):
        """Returns a boolean indicating availability of packets 
        in the buffer.
        """
        
        self.lock.acquire()
        available = len(self.packet_buffer) > 0
        self.lock.release()
        return available

    def get_next_packet(self):
        """Returns a packet by popping it from the buffer."""
        
        self.lock.acquire()
        if len(self.packet_buffer) <= 0:
            return None
        oldest_packet = xda.XsDataPacket(self.packet_buffer.pop(0))
        self.lock.release()
        return oldest_packet    
    
    def onLiveDataAvailable(self, device, packet):
        """Overrides Xsens Device API onLiveDataAvailable method."""
        
        self.lock.acquire()
        if packet != 0:
            while len(self.packet_buffer) >= self.max_buffered_packets:
                self.packet_buffer.pop()
            self.packet_buffer.append(xda.XsDataPacket(packet))
            self.lock.release()
