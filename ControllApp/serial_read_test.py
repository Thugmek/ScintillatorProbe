import serial

ser = serial.Serial(port="/dev/ttyACM0")

while True:
    line = ser.readline()
    if line.startswith(b"Temperature Report, data size"):
        temperatures_bin = ser.read(200)
        pwms_bin = ser.read(200)
        temperatures = []
        pwms = []
        for i in range(100):
            b = temperatures_bin[0:2]
            temperatures_bin = temperatures_bin[2:]
            p = pwms_bin[0:2]
            pwms_bin = pwms_bin[2:]

            temperatures.append(int.from_bytes(b, "little"))
            pwms.append(int.from_bytes(p, "little"))
        print(f"Voltages: {len(temperatures)} {temperatures}, pwms: {pwms}")
