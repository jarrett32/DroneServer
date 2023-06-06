def translate_to_mavproxy_command(command_data):
    # Check the source of the command
    if command_data['source'] != 'app':
        print("Invalid source")
        return None

    # Define the command lookup table
    command_lookup = {
        'connect-app': 'connect-app',
        'disconnect-app': 'disconnect-app',
        'arm': 'arm throttle',
        'disarm': 'disarm',
        'land': 'mode land'
    }

    # Get the command and data from the input data
    command = command_data['command']
    data = command_data['data']

    # Check the command type
    if command_lookup[command]:
        return command_lookup[command]

    else:
        print(f"Invalid command type: {command}")
        return None
