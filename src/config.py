import os
from dataclasses import dataclass

@dataclass
class BCIConfig:
    # Serial port configuration
    SERIAL_PORT: str = os.getenv('BCI_SERIAL_PORT', '/dev/ttyUSB0')
    BAUD_RATE: int = int(os.getenv('BCI_BAUD_RATE', '9600'))
    
    # Signal processing parameters
    SAMPLING_RATE: int = 250  # Hz
    FILTER_LOW_CUTOFF: float = 0.5  # Hz
    FILTER_HIGH_CUTOFF: float = 50.0  # Hz
    BUFFER_SIZE: int = 1000  # samples
    
    # Robot control parameters
    ROBOT_SERIAL_PORT: str = os.getenv('ROBOT_SERIAL_PORT', '/dev/ttyUSB1')
    ROBOT_BAUD_RATE: int = int(os.getenv('ROBOT_BAUD_RATE', '115200'))
    MAX_SPEED: float = 0.5  # normalized units
    
    # Safety parameters
    SAFETY_TIMEOUT: float = 0.5  # seconds
    MAX_ACCELERATION: float = 0.2  # units/s^2
    
    # Logging
    LOG_FILE: str = "bci_system.log"
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')

config = BCIConfig()
