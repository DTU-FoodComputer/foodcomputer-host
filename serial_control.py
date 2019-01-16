import serial
import time
import serial.tools.list_ports


class SerialControl:
    """Class for controlling the food computer via serial"""

    def __init__(self, baudrate, debug=False):
        self.baudrate = baudrate
        self.debug = debug
        self.serialConnection = None
        self.connect()

    def connect(self):
        port = self.pick_serial_port()
        self.serialConnection = serial.Serial(port, self.baudrate, timeout=10)
        self.serialConnection.flushInput()
        time.sleep(1)

    def send(self, data):
        # send a single line through serial
        self.serialConnection.write((data + "\n").encode("utf-8"))
        if self.debug:
            print("Sent " + str(data))
        self.flushout()

    def readlines(self, timeout=30):
        # reads all available lines from serial
        lines = []
        line = ""
        start_time = time.time()
        while time.time() - start_time < timeout and self.serialConnection.in_waiting > 0:
            ch = self.serialConnection.read().decode("utf-8")
            if ch == '\n':
                lines.append(line.rstrip())
                line = ""
            else:
                line = line + ch
        return lines

    def wait_for_response(self, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.serialConnection.in_waiting > 0:
                return True

        return False

    def kill(self):
        self.serialConnection.close()

    def flushin(self):
        self.serialConnection.reset_input_buffer()

    def flushout(self):
        self.serialConnection.reset_output_buffer()

    @staticmethod
    def pick_serial_port():
        ports = serial.tools.list_ports.comports()
        result = []
        for port in ports:
            try:
                s = serial.Serial(port[0])
                s.close()
                result.append(port[0])
            except (OSError, serial.SerialException):
                pass
        return result[-1]
