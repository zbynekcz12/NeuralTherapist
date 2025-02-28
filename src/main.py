from bci_reader import BCIReader
from signal_processor import SignalProcessor
from robot_controller import RobotController
from safety_monitor import SafetyMonitor
from visualization import Visualizer
from gui import GUI
from logger import logger
import threading

def main():
    try:
        # Initialize components
        bci_reader = BCIReader()
        signal_processor = SignalProcessor()
        robot_controller = RobotController()
        safety_monitor = SafetyMonitor(robot_controller)
        
        # Create visualization in a separate thread
        visualizer = Visualizer()
        viz_thread = threading.Thread(
            target=visualizer.start_visualization,
            args=(bci_reader.get_buffer, signal_processor.extract_features)
        )
        viz_thread.daemon = True
        
        # Create and start GUI
        gui = GUI(bci_reader, robot_controller, safety_monitor)
        
        # Start visualization
        viz_thread.start()
        
        # Main processing loop
        def processing_loop():
            while True:
                if bci_reader.connected and robot_controller.connected:
                    # Read and process BCI data
                    sample = bci_reader.read_sample()
                    if sample:
                        # Process signal
                        buffer = bci_reader.get_buffer()
                        filtered_signal = signal_processor.filter_signal(buffer)
                        features = signal_processor.extract_features(filtered_signal)
                        command = signal_processor.classify_command(features)
                        
                        # Update safety monitor
                        safety_monitor.update_activity()
                        
                        # Execute robot command if not in emergency stop
                        if not safety_monitor.emergency_stop:
                            if command == 'forward':
                                robot_controller.send_command('forward', 0.5)
                            elif command == 'stop':
                                robot_controller.send_command('stop', 0.0)
        
        # Start processing in separate thread
        process_thread = threading.Thread(target=processing_loop)
        process_thread.daemon = True
        process_thread.start()
        
        # Start GUI (main thread)
        gui.run()
        
    except Exception as e:
        logger.critical(f"System error: {e}")
        raise
    finally:
        # Cleanup
        safety_monitor.stop_monitoring()
        bci_reader.disconnect()
        robot_controller.disconnect()
        logger.info("System shutdown complete")

if __name__ == "__main__":
    main()
