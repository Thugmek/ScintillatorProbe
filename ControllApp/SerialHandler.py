import serial
import threading

class SerialCallback:
    def __init__(self, command, callback):
        self.command = command
        self.callback = callback

class _SerialHandler:
    def __init__(self):
        self.device = "/dev/pts/7"
        self.callbacks = []
        self.work_thread = threading.Thread(target=self.work_loop)
        self.serial = serial.Serial(port=self.device)

    def set_device(self, device):
        self.device = device

    def add_callback(self, callback: SerialCallback):
        self.callbacks.append(callback)

    def remove_callback(self, callback: SerialCallback):
        self.callbacks.remove(callback)

    def send_command(self, command:str):
        self.serial.write(command.encode())

    def start_handler(self):
        self.work_thread.start()

    def work_loop(self):
        while True:
            line = self.serial.readline()
            for cb in self.callbacks:
                if line.startswith(cb.command):
                    cb.callback(line, self.serial)
                    break

SerialHandler = _SerialHandler()