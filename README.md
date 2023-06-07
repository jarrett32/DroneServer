# Drone Server Documentation

This project comprises of a server that facilitates the remote control of a drone using Dronekit (MAVLink) commands over a network. It provides an interface to communicate with the drone via HTTP.

## Key Components

1. `server.py`: This is the main server file. It sets up a Flask server, which listens to HTTP POST requests at the `/send-data` endpoint. The data sent in these requests is expected to be in a specific format that can be translated to a MAVLink command.

2. `drone_control.py`: This file defines a `DroneControl` class, which is used to interface with the drone itself. The `DroneControl` object maintains a queue of commands to be executed and processes them one by one. It can connect to the drone, execute commands on the drone, and handle the drone's response.

## Server Usage Guidelines

1. Ensure your phone's hotspot is enabled.

2. Start or reboot the Raspberry Pi.

3. SSH into your Pi with `ssh pi@raspberrypi.local`.

4. Use `hostname -I` to retrieve the IP address of the Pi.

5. Run the server using `python server.py`.

6. Use the companion app, connect to the server using the IP from step 4, and start sending commands. It's recommended to use testing mode first, which can be enabled in the config file (`config.yaml`).

## Initial Setup Guidelines

1. Start the Raspberry Pi with a monitor, keyboard, and mouse connected.

2. Enable your phone's hotspot and connect to it on the Pi's monitor.

3. Edit the `wpa_supplicant.conf` file (this is the configuration file for the Wi-Fi) located at `/etc/wpa_supplicant/wpa_supplicant.conf`. Add `priority=1` to the configuration block for your hotspot. This will make the Pi connect to your hotspot by default upon startup. 

```bash
network={
    ssid="Your_Hotspot_Name"
    psk="Your_Hotspot_Password"
    priority=1
}
```

4. Change the mDNS (Multicast DNS) hostname of your Raspberry Pi to `raspberrypi.local`. You can do this by editing the `hostname` file (`sudo nano /etc/hostname`) and `hosts` file (`sudo nano /etc/hosts`), replacing the existing name with `raspberrypi.local`.

5. Connect your serial cable from the Raspberry Pi to the Pixhawk. A detailed tutorial on this will be provided in the future.

6. Continue to the usage instructions above.

## Recording Feature
If the `record_video` configuration is set to `True` in `config.yaml`, the server will start recording a video from the Pi Camera as soon as the drone is connected. The recording will be saved as `output.h264`. This feature requires a Pi Camera module to be connected to the Raspberry Pi.