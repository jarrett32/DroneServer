import threading
from dronekit import connect, VehicleMode
import time
from queue import Queue
import picamera

class DroneControl:
    def __init__(self, config):
        self.vehicle = None
        self.config = config
        self.force_disarm_timer = config["force_disarm_timer"]
        self.commands = Queue()
        self.force_land = {'value': False}
        self.thread = threading.Thread(target=self._process_commands)

        if self.config['record_video']:
            self.camera = picamera.PiCamera()

    def connect(self):
        # Connect to the vehicle
        self.vehicle = connect('/dev/ttyAMA0', baud=57600)
        while not self.vehicle.is_armable:
            print("Waiting for vehicle connection...")
            time.sleep(1)

        print("Connected to drone via Serial Cable!")
        if self.config['record_video']:
            self.camera.start_recording('output.h264')
            print("Started Recording...")
        self.thread.start()

    def close_vehicle(self):
        self.vehicle.close()
        if self.config['record_video']:
            if self.camera.recording:
                self.camera.stop_recording()
                self.camera.close()
                print("Stopped Recording...")

    def execute(self, mavproxy_command):
        self.commands.put(mavproxy_command)

    def _process_commands(self):
        while True:
            command = self.commands.get()
            self._execute_command(command)

    def _execute_command(self, command):
        cmd, *params = command.split()

        if cmd == 'arm':
            if params[0] == 'throttle':
                self.force_land['value'] = False
                self.vehicle.mode = VehicleMode("GUIDED")
                while not self.vehicle.is_armable:
                    print("Waiting for vehicle to become armable.")
                    time.sleep(1)

                self.vehicle.armed = True

                disarm_timer = threading.Timer(self.force_disarm_timer, self.force_disarm)
                disarm_timer.start()

                while not self.vehicle.armed:
                    print("Waiting for vehicle to arm.")
                    time.sleep(1)

                # After vehicle is armed, check if it's not disarmed already
                if self.vehicle.armed:
                    print("Taking off!")
                    target_altitude = .2
                    increment = 0.01  # Further decreased increment for even slower takeoff
                    current_altitude = self.vehicle.location.global_relative_frame.alt
                    max_tilt = 15  # Maximum tilt angle in degrees

                    while current_altitude < target_altitude and not self.force_land['value']:
                        current_altitude += increment
                        self.vehicle.simple_takeoff(current_altitude)  # Take off to current altitude
                        time.sleep(5)  # Further increased sleep time for even slower ascent

                        # Check roll and pitch, if they exceed max_tilt, force landing
                        attitude = self.vehicle.attitude
                        if abs(attitude.roll) > max_tilt or abs(attitude.pitch) > max_tilt:
                            print("Tilt exceeded, initiating forced landing...")
                            self.force_land['value'] = True

                        # Check altitude, if it's decreasing, force landing
                        if self.vehicle.location.global_relative_frame.alt < current_altitude:
                            print("Unexpected altitude decrease, initiating forced landing...")
                            self.force_land['value'] = True

                if self.force_land['value']:
                    self.vehicle.mode = VehicleMode("LAND")
                    while self.vehicle.armed:
                        print("Disarming vehicle")
                        self.vehicle.armed = False
                        time.sleep(1)

        elif cmd == 'disarm':
            self.force_land['value'] = True  # Stop the waiting thread
            self.vehicle.mode = VehicleMode("LAND")
            while self.vehicle.armed:
                print("Disarming vehicle")
                self.vehicle.armed = False
                time.sleep(1)

        elif cmd == 'land':
            self.force_land['value'] = True
            self.vehicle.mode = VehicleMode("LAND") 

    def force_disarm(self):
        self.force_land['value'] = True
        self.vehicle.mode = VehicleMode("LAND")
        while self.vehicle.armed:
            print("Disarming vehicle")
            self.vehicle.armed = False
            time.sleep(1)
