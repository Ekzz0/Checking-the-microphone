import time
import wx
import serial
import threading
from pynput import keyboard
from elevate import elevate
from firebox import serialPorts

BUTTON_CLEAR = wx.NewIdRef()


class MessegesForArsuino:
    def __init__(self, parent):
        self.serialcomm = serial.Serial(serialPorts()[0], 9600)
        # print(self.serialcomm)
        self.serialcomm.timeout = 0.1
        self.check = True
        self.parent = parent

    def send_command(self):
        if self.check:
            self.serialcomm.write('1'.encode())
            print('red')
            self.parent.console_control('red')

            self.check = False
        else:
            self.serialcomm.write('2'.encode())
            print('green')
            self.parent.console_control('green')
            self.check = True

    def exit_f(self):
        self.serialcomm.write('0'.encode())
        self.parent.console_control('off')
        print('off')


# Основной класс для создания приложения
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, title=title, size=(400, 400))
        self.control_messege = 0

        # Запуск отслеживания нажатия горячих клавиш в отдельном потоке
        thr = threading.Thread(target=self.threading_create_hotkey)
        thr.start()

        # Создание иконки
        ico = wx.Icon('mic.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        # Тут начинается проектирование основного окна
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#270736')
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Создание 1й свехру части: консоли
        st5 = wx.StaticText(self.panel, label="Консоль:")
        vbox.Add(st5, flag=wx.EXPAND | wx.LEFT, border=20)
        self.console = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.console.SetBackgroundColour('#e1def1')
        vbox.Add(self.console, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=20, proportion=1)
        self.btn_clear = wx.Button(self.panel, BUTTON_CLEAR, label='Нажми перед выходом', size=(150, 30))
        self.btn_clear.SetBackgroundColour('#e1def1')
        vbox.Add(self.btn_clear, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=30)
        self.panel.SetSizer(vbox)

        # Установка биндов для всех кнопок
        self.Bind(wx.EVT_BUTTON, self.clear_console, id=BUTTON_CLEAR)

    def threading_create_hotkey(self):
        self.control_messege = MessegesForArsuino(self)
        with keyboard.GlobalHotKeys({
            '<shift>+t': self.control_messege.send_command,
            '<shift>+y': self.control_messege.exit_f}) as h:
            h.join()

    # Функция для очищения консоли
    def clear_console(self, event):
        # pass
        self.control_messege.exit_f()
        self.console.SetValue('')

    def console_control(self, message):
        self.console.WriteText(f"{time.asctime()[11:19]} - {message}\n")


if __name__ == "__main__":
    elevate()
    app = wx.App()
    frame = MyFrame(None, title='Microphone Checker')
    frame.Center()
    frame.Show()
    app.MainLoop()



