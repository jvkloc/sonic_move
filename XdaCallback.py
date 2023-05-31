# class for handling incoming data from sensors
# Xsens Device API documentation provided with SDK download from https://www.movella.com/support/software-documentation
import xsensdeviceapi as xda
from threading import Lock

class XdaCallback(xda.XsCallback):
    def __init__(self, max_buffer_size = 5):
        xda.XsCallback.__init__(self)
        self.m_maxNumberOfPacketsInBuffer = max_buffer_size
        self.m_packetBuffer = []
        self.m_lock = Lock()
    # check if there is a data packet available
    def packetAvailable(self):
        self.m_lock.acquire()
        res = len(self.m_packetBuffer) > 0
        self.m_lock.release()
        return res
    # get the next data packet
    def getNextPacket(self):
        self.m_lock.acquire()
        if len(self.m_packetBuffer) <= 0:
            return None
        oldest_packet = xda.XsDataPacket(self.m_packetBuffer.pop(0))
        self.m_lock.release()
        return oldest_packet
    # overwrite Xsens Device API onLiveDataAvailable method
    def onLiveDataAvailable(self, device, packet):
        self.m_lock.acquire()
        if packet != 0:
            while len(self.m_packetBuffer) >= self.m_maxNumberOfPacketsInBuffer:
                self.m_packetBuffer.pop()
            self.m_packetBuffer.append(xda.XsDataPacket(packet))
            self.m_lock.release()
