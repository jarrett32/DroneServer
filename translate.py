def translate_to_mavproxy_command(command_data):
    command_type = command_data['command']
    data = command_data['data']['data']

    if command_type == 'button':
        if data == 'arm':
            return 'arm throttle'
        elif data == 'disarm':
            return 'disarm'
    elif command_type == 'joystick-left':
        # Adjust roll and pitch based on joystick input
        roll = data['message']['position']['x']
        pitch = data['message']['position']['y']
        # convert joystick values to RC values (this is a hypothetical formula, replace with your actual mapping)
        roll_rc = roll * 5 + 1000
        pitch_rc = pitch * 5 + 1000
        return 'rc 1 {0}, rc 2 {1}'.format(roll_rc, pitch_rc)
    elif command_type == 'joystick-right':
        # Adjust throttle and yaw based on joystick input
        throttle = data['message']['position']['y']
        yaw = data['message']['position']['x']
        # convert joystick values to RC values (this is a hypothetical formula, replace with your actual mapping)
        throttle_rc = throttle * 5 + 1000
        yaw_rc = yaw * 5 + 1000
        return 'rc 3 {0}, rc 4 {1}'.format(throttle_rc, yaw_rc)

    # If the command is not recognized, return an empty string
    return command_type
