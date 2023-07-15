from threading import Lock
# Xsens Device API documentation provided with SDK download:
# https://www.movella.com/support/software-documentation
import xsensdeviceapi as xda


class XdaCallback(xda.XsCallback):
    """Class for handling incoming data from sensors. XdaCallback
    inherits the Xsens Device API XsCallback class.
    """

    def __init__(self, max_buffer_size = 5):
        """Initialise XdaCallback object.
        Parameters
        --------------
        max_buffer_size : int
            The maximum length of data packet list.
        Attributes
        ------------
        max_buffered_packets : int
            Receives the parameter max_buffer_size
        packet_buffer : list
            A list for data packets waiting to be processed.
        lock : Lock object
            A Lock object for packet handling.
         """
        xda.XsCallback.__init__(self)
        self.max_buffered_packets = max_buffer_size
        self.packet_buffer = []
        self.lock = Lock()

    def packet_available(self):
        self.lock.acquire()
        res = len(self.packet_buffer) > 0
        self.lock.release()
        return res

    def get_next_packet(self):
        self.lock.acquire()
        if len(self.packet_buffer) <= 0:
            return None
        oldest_packet = xda.XsDataPacket(self.packet_buffer.pop(0))
        self.lock.release()
        return oldest_packet
    
    # Overwriting Xsens Device API onLiveDataAvailable method.
    def on_live_data_available(self, device, packet):
        self.lock.acquire()
        if packet != 0:
            while len(self.packet_buffer) >= self.max_buffered_packets:
                self.packet_buffer.pop()
            self.packet_buffer.append(xda.XsDataPacket(packet))
            self.lock.release()
