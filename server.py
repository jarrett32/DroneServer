from flask import Flask, request
from config import load_config
from translate import translate_to_mavproxy_command
from drone_control import DroneControl
import atexit

app = Flask(__name__)
config = load_config("config.yaml")
drone_control = DroneControl(config)

def close_vehicle():
    print("Close vehicle connection")
    drone_control.close_vehicle()

if drone_control.vehicle:
    atexit.register(close_vehicle)

@app.route('/send-data', methods=['POST'])
def send_command():
    data = request.get_json()
    mavproxy_command = translate_to_mavproxy_command(data)
    print(data, mavproxy_command)

    if mavproxy_command:
        if not config["testing"]:
            drone_control.execute(mavproxy_command)
        else:
            print(['mavproxy.py', '--master=/dev/ttyAMA0', '--baudrate', '57600', '--aircraft', 'MyCopter', mavproxy_command])

        return {"status": "success"}, 200
    else:
        return {"status": "error", "message": "Invalid command"}, 400


if __name__ == '__main__':
    print("Starting server...")
    if config["testing"]:
        print("Testing: ENABLED")
    else:
        print("Testing: DISABLED")
        drone_control.connect() # Recieve heartbeat from Drone via serial cable
    app.run(host='0.0.0.0', port=5000)

