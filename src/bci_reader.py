import serial
import numpy as np
from config import config
from logger import logger

class BCIReader:
    def __init__(self):
        self.port = None
        self.buffer = np.zeros(config.BUFFER_SIZE)
        self.buffer_index = 0
        self.connected = False

    def connect(self):
        try:
            self.port = serial.Serial(
                config.SERIAL_PORT,
                config.BAUD_RATE,
                timeout=1
            )
            self.connected = True
            logger.info(f"Connected to BCI device on {config.SERIAL_PORT}")
        except serial.SerialException as e:
            logger.error(f"Failed to connect to BCI device: {e}")
            self.connected = False

    def disconnect(self):
        if self.port and self.port.is_open:
            self.port.close()
            self.connected = False
            logger.info("Disconnected from BCI device")

    def read_sample(self):
        if not self.connected:
            return None
        
        try:
            data = self.port.readline()
            if data:
                # Assuming comma-separated values
                values = [float(x) for x in data.decode().strip().split(',')]
                self.buffer[self.buffer_index] = values[0]  # Using first channel
                self.buffer_index = (self.buffer_index + 1) % config.BUFFER_SIZE
                return values
        except Exception as e:
            logger.error(f"Error reading BCI data: {e}")
            return None

    def get_buffer(self):
        return np.roll(self.buffer, -self.buffer_index)
