from flask import Flask, jsonify, request, render_template
from bci_reader import BCIReader
from signal_processor import SignalProcessor
from robot_controller import RobotController
from safety_monitor import SafetyMonitor
from logger import logger
import threading

app = Flask(__name__)
# Globální proměnné pro přístup k komponentám
bci_reader = None
signal_processor = None
robot_controller = None
safety_monitor = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bci/data', methods=['GET'])
def get_bci_data():
    if not bci_reader or not bci_reader.connected:
        return jsonify({'error': 'BCI není připojeno'}), 400

    buffer = bci_reader.get_buffer()
    features = signal_processor.extract_features(buffer)
    return jsonify({
        'raw_data': buffer.tolist(),
        'features': features
    })

@app.route('/connect/bci', methods=['POST'])
def connect_bci():
    if bci_reader:
        bci_reader.connect()
        if bci_reader.connected:
            return jsonify({'message': 'BCI úspěšně připojeno'})
    return jsonify({'error': 'Nelze připojit BCI'}), 400

@app.route('/connect/robot', methods=['POST'])
def connect_robot():
    if robot_controller:
        robot_controller.connect()
        if robot_controller.connected:
            return jsonify({'message': 'Robot úspěšně připojen'})
    return jsonify({'error': 'Nelze připojit robot'}), 400

@app.route('/robot/command', methods=['POST'])
def send_robot_command():
    if not robot_controller or not robot_controller.connected:
        return jsonify({'error': 'Robot není připojen'}), 400

    data = request.json
    command = data.get('command')
    speed = data.get('speed', 0.0)

    if not safety_monitor.emergency_stop:
        success = robot_controller.send_command(command, speed)
        if success:
            return jsonify({'status': 'success'})

    return jsonify({'error': 'Příkaz se nepodařilo odeslat'}), 400

@app.route('/system/status', methods=['GET'])
def get_system_status():
    return jsonify({
        'bci_connected': bci_reader.connected if bci_reader else False,
        'robot_connected': robot_controller.connected if robot_controller else False,
        'emergency_stop': safety_monitor.emergency_stop if safety_monitor else True
    })

@app.route('/system/start', methods=['POST'])
def start_system():
    if not (bci_reader and robot_controller and 
            bci_reader.connected and robot_controller.connected):
        return jsonify({'error': 'Nejprve připojte BCI a robot'}), 400

    safety_monitor.start_monitoring()
    return jsonify({'message': 'Systém spuštěn'})

@app.route('/system/emergency_stop', methods=['POST'])
def trigger_emergency_stop():
    if safety_monitor:
        safety_monitor.trigger_emergency_stop()
        return jsonify({'message': 'Nouzové zastavení aktivováno'})
    return jsonify({'error': 'Safety monitor není inicializován'}), 500

def processing_loop():
    while True:
        if bci_reader and robot_controller and bci_reader.connected and robot_controller.connected:
            # Čtení a zpracování BCI dat
            sample = bci_reader.read_sample()
            if sample:
                # Zpracování signálu
                buffer = bci_reader.get_buffer()
                filtered_signal = signal_processor.filter_signal(buffer)
                features = signal_processor.extract_features(filtered_signal)
                command = signal_processor.classify_command(features)

                # Aktualizace monitoru bezpečnosti
                safety_monitor.update_activity()

                # Provedení příkazu robota, pokud není aktivní nouzové zastavení
                if not safety_monitor.emergency_stop:
                    if command == 'forward':
                        robot_controller.send_command('forward', 0.5)
                    elif command == 'stop':
                        robot_controller.send_command('stop', 0.0)

def main():
    global bci_reader, signal_processor, robot_controller, safety_monitor

    try:
        # Inicializace komponent
        bci_reader = BCIReader()
        signal_processor = SignalProcessor()
        robot_controller = RobotController()
        safety_monitor = SafetyMonitor(robot_controller)

        # Spuštění zpracování v samostatném vlákně
        process_thread = threading.Thread(target=processing_loop)
        process_thread.daemon = True
        process_thread.start()

        # Spuštění webového serveru
        logger.info("Spouštím webové rozhraní...")
        app.run(host='0.0.0.0', port=5000)

    except Exception as e:
        logger.critical(f"Chyba systému: {e}")
        raise
    finally:
        # Úklid
        if safety_monitor:
            safety_monitor.stop_monitoring()
        if bci_reader:
            bci_reader.disconnect()
        if robot_controller:
            robot_controller.disconnect()
        logger.info("Systém byl vypnut")

if __name__ == "__main__":
    main()