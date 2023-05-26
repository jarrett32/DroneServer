from flask import Flask, request
from translate import translate_to_mavproxy_command
from dronekit import connect, VehicleMode
import atexit
import time

# Connect to the vehicle
vehicle = connect('/dev/ttyAMA0', wait_ready=False, baud=57600)

app = Flask(__name__)
testing = False

def close_vehicle():
    """
    Close vehicle connection when exiting the script
    """
    print("Close vehicle connection")
    vehicle.close()

atexit.register(close_vehicle)

@app.route('/send-data', methods=['POST'])
def send_command():
    data = request.get_json()
    print(data)
    mavproxy_command = translate_to_mavproxy_command(data)

    if mavproxy_command and not testing:
        # Parse the mavproxy command to dronekit methods and parameters
        cmd, *params = mavproxy_command.split()
        if cmd == 'arm':
            if params[0] == 'throttle':
                vehicle.mode = VehicleMode("GUIDED")
                vehicle.armed = True
        elif cmd == 'disarm':
            vehicle.armed = False
        elif cmd == 'rc':
            channel = int(params[0])
            pwm = int(params[1])
            vehicle.channels.overrides[channel] = pwm
        return {"status": "success"}
    else:
        print(['mavproxy.py', '--master=/dev/ttyAMA0', '--baudrate', '57600', '--aircraft', 'MyCopter', mavproxy_command])

if __name__ == '__main__':
    # Wait until vehicle is ready before starting Flask server
    while not vehicle.is_armable:
        print("Waiting for vehicle connection...")
        time.sleep(1)
    
    print("Connected to drone!")
    app.run(host='0.0.0.0', port=5000)

