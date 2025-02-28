import time
import threading
from config import config
from logger import logger

class SafetyMonitor:
    def __init__(self, robot_controller):
        self.robot_controller = robot_controller
        self.last_activity = time.time()
        self.emergency_stop = False
        self.monitoring = False
        self.monitor_thread = None

    def start_monitoring(self):
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("Safety monitoring started")

    def stop_monitoring(self):
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("Safety monitoring stopped")

    def _monitor_loop(self):
        while self.monitoring:
            if self.emergency_stop:
                self.robot_controller.stop()
                logger.warning("Emergency stop activated")
            elif time.time() - self.last_activity > config.SAFETY_TIMEOUT:
                self.robot_controller.stop()
                logger.warning("Safety timeout - stopping robot")
            time.sleep(0.1)

    def update_activity(self):
        self.last_activity = time.time()

    def trigger_emergency_stop(self):
        self.emergency_stop = True
        self.robot_controller.stop()
        logger.critical("Emergency stop triggered")

    def reset_emergency_stop(self):
        self.emergency_stop = False
        logger.info("Emergency stop reset")
