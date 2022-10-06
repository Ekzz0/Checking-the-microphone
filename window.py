
import wx
import time

BUTTON_CLEAR = wx.NewIdRef()

# Основной класс для создания приложения
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, title=title, size=(400, 400))
        """НУЖНО ЗАПРЕТИТЬ ИЗМЕНЕНИЕ РАЗМЕРОВ ОКНА"""
        self.path_name = 0

        # Создание иконки
        ico = wx.Icon('mic.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        # Тут начинается проектирование основного окна
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#f8a05f')
        vbox = wx.BoxSizer(wx.VERTICAL)


        # Создание 1й свехру части: консоли
        st5 = wx.StaticText(self.panel, label="Консоль:")
        vbox.Add(st5, flag=wx.EXPAND | wx.LEFT, border=20)
        self.console = wx.TextCtrl(self.panel, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.console.SetBackgroundColour('#f4f4f4')
        vbox.Add(self.console, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=20, proportion=1)
        self.btn_clear = wx.Button(self.panel, BUTTON_CLEAR, label='Очистить консоль', size=(150, 30))
        self.btn_clear.SetBackgroundColour('#f6f6f6')
        vbox.Add(self.btn_clear, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=30)
        self.panel.SetSizer(vbox)

        # Установка биндов для всех кнопок
        self.Bind(wx.EVT_BUTTON, self.clear_console, id=BUTTON_CLEAR)


    # Функция для очищения консоли
    def clear_console(self, event):
        self.console.SetValue('')

    def console_control(self, message):
        self.console.WriteText(f"{time.asctime()[11:19]} - {message}\n")


# Основная функция, с которой происходит запуск программы
if __name__ == "__main__":
    #elevate()
    app = wx.App()
    frame = MyFrame(None, title='Microphone Checker')
    frame.Center()
    frame.Show()
    app.MainLoop()
