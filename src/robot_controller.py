import serial
import time
from config import config
from logger import logger

class RobotController:
    def __init__(self):
        self.port = None
        self.connected = False
        self.current_speed = 0.0
        self.last_command_time = time.time()

    def connect(self):
        try:
            self.port = serial.Serial(
                config.ROBOT_SERIAL_PORT,
                config.ROBOT_BAUD_RATE,
                timeout=1
            )
            self.connected = True
            logger.info(f"Connected to robot on {config.ROBOT_SERIAL_PORT}")
        except serial.SerialException as e:
            logger.error(f"Failed to connect to robot: {e}")
            self.connected = False

    def disconnect(self):
        if self.port and self.port.is_open:
            self.stop()
            self.port.close()
            self.connected = False
            logger.info("Disconnected from robot")

    def send_command(self, command, speed=0.0):
        if not self.connected:
            return False

        try:
            # Limit acceleration
            current_time = time.time()
            dt = current_time - self.last_command_time
            max_speed_change = config.MAX_ACCELERATION * dt
            
            target_speed = min(speed, config.MAX_SPEED)
            speed_change = target_speed - self.current_speed
            speed_change = np.clip(speed_change, 
                                 -max_speed_change,
                                 max_speed_change)
            
            self.current_speed += speed_change
            
            # Format: <command>,<speed>\n
            command_str = f"{command},{self.current_speed:.2f}\n"
            self.port.write(command_str.encode())
            
            self.last_command_time = current_time
            logger.info(f"Sent robot command: {command_str.strip()}")
            return True
        except Exception as e:
            logger.error(f"Error sending robot command: {e}")
            return False

    def stop(self):
        self.send_command('stop', 0.0)
        self.current_speed = 0.0
