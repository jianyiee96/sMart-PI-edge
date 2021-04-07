import serial, pprint
if __name__ == '__main__':

    ser = serial.Serial(port='COM11', baudrate=115200, timeout=1)
    print("PI-EDGE is running.. Listening on serial port.")
    while True:
        
        response = ser.readline()
        response = response.decode('utf-8').strip()
        if(response != '' and response[0] == '>'):
            response_comp = response[1:].split("=")

            device = response_comp[0]
            command = response_comp[1]
            rdif = response_comp[2]
            print()
            print(f"Command: {command}")
            print(f"Device: {device}")
            print(f"RFID: {rdif}")
