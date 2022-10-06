import serial
from pynput import keyboard
from elevate import elevate
from firebox import serialPorts


class MessegesForArsuino:
    def __init__(self):
        print(serialPorts())
        self.serialcomm = serial.Serial(serialPorts()[0], 9600)

        self.serialcomm.timeout = 0.1
        print("Подключение")
        self.check = True

    def send_command(self):
        print("ss")
        if self.check:
            self.serialcomm.write('1'.encode())
            print('red')

            self.check = False
        else:
            self.serialcomm.write('2'.encode())
            print('green')
            self.check = True

    def exit_f(self):
        self.serialcomm.write('0'.encode())
        print('off')
def test_func():
    print(1)


if __name__ == "__main__":
    # elevate()
    msg = MessegesForArsuino()
    # print(serialPorts())
    with keyboard.GlobalHotKeys({
        '<shift>+t': msg.send_command,
        '<shift>+y': msg.exit_f}) as h:
        h.join()



    #

