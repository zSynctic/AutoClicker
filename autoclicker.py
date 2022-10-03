import sys
import os
import pyautogui
import customtkinter
import threading
import spinbox
from PIL import Image, ImageTk
from pynput.keyboard import *
from tkinter import IntVar

autoclick_key = Key.f5
holdm_key = Key.f6

button1 = "left"
clicktype = "Single"
repeattype = 1

pause = False


class App(customtkinter.CTk):

    auto = False
    auto1 = False

    WIDTH = 320
    HEIGHT = 450

    global resource

    def resource(relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    def __init__(self):
        super().__init__()

        self.p1 = ImageTk.PhotoImage(file=resource("Assets/icon.ico"))

        self.iconphoto(False, self.p1)

        self.title("AutoClicker")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(5, weight=1)

        self.title = customtkinter.CTkLabel(
            master=self.frame, text="AutoClicker", text_font=("Roboto Medium", -16))
        self.title.grid(row=1, column=1, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.start_auto_button = customtkinter.CTkButton(master=self.frame, text="Start", fg_color=(
            "black"), text_font=("Roboto Medium", -16), command=self.start_button2)
        self.start_auto_button.place(x=80, y=275)

        self.stop_auto_button = customtkinter.CTkButton(master=self.frame, text="Stop", fg_color=(
            "black"), text_font=("Roboto Medium", -16), state="disabled", command=self.stop_button2)
        self.stop_auto_button.place(x=80, y=310)

        self.buttonmenu_var = customtkinter.StringVar(value="left")

        self.buttonmenu = customtkinter.CTkOptionMenu(master=self.frame, text_font=(
            "Roboto Medium", -14), width=115, fg_color="black", button_color="black", variable=self.buttonmenu_var, command=self.buttonmenu_event, values=["left", "middle", "right"])
        self.buttonmenu.place(x=20, y=90)

        self.mousebuttontxt = customtkinter.CTkLabel(
            master=self.frame, text="Mouse Button:", text_font=("Roboto Medium", -15))
        self.mousebuttontxt.place(x=5, y=60)

        self.clicktype_var = customtkinter.StringVar(value="Single")

        self.clicktypemenu = customtkinter.CTkOptionMenu(master=self.frame, text_font=(
            "Roboto Medium", -14), width=115, fg_color="black", button_color="black", variable=self.clicktype_var, command=self.clicktype_event, values=["Single", "Double", "Triple", "Hold"])
        self.clicktypemenu.place(x=160, y=90)

        self.clicktypetxt = customtkinter.CTkLabel(
            master=self.frame, text="Click Type:", text_font=("Roboto Medium", -15))
        self.clicktypetxt.place(x=145, y=60)

        self.clickinterval_var = customtkinter.StringVar(
            master=self.frame, value=str(0.01))

        self.clickinterval = customtkinter.CTkEntry(master=self.frame, text_font=(
            "Roboto Medium", -14), width=80, textvariable=self.clickinterval_var)
        self.clickinterval.place(x=110, y=380)

        self.clickintervaltxt = customtkinter.CTkLabel(
            master=self.frame, text="Click interval", text_font=("Roboto Medium", -14))
        self.clickintervaltxt.place(x=80, y=350)

        self.secondstxt = customtkinter.CTkLabel(
            master=self.frame, text="secs", text_font=("Roboto Medium", -13), width=10)
        self.secondstxt.place(x=195, y=385)

        self.repeat_var = IntVar()
        self.repeat_var.set(value=1)

        self.repeat = customtkinter.CTkRadioButton(master=self.frame, text="Repeat", value=0, variable=self.repeat_var,
                                                   command=self.repeat_event, text_font=("Roboto Medium", -13), width=20, height=20)
        self.repeat.place(x=20, y=140)

        self.repeatstopped = customtkinter.CTkRadioButton(master=self.frame, text="Repeat until stopped", value=1,
                                                          variable=self.repeat_var, command=self.repeat_event, text_font=("Roboto Medium", -13), width=20, height=20)
        self.repeatstopped.place(x=20, y=170)

        self.repeattimes = spinbox.FloatSpinbox(
            master=self.frame, width=105, height=25, step_size=1)
        self.repeattimes.place(x=160, y=135)

        self.repeattimes.set(1)
        self.repeatstopped.select()

    def buttonmenu_event(self, choice):
        global button1

        if choice == "left":
            button1 = "left"
        if choice == "middle":
            button1 = "middle"
        if choice == "right":
            button1 = "right"

    def clicktype_event(self, choice):
        global clicktype

        if choice == "Single":
            clicktype = "Single"
        if choice == "Double":
            clicktype = "Double"
        if choice == "Triple":
            clicktype = "Triple"
        if choice == "Hold":
            clicktype = "Hold"

    def repeat_event(self):
        global repeattype

        if self.repeat_var.get() == 0:
            repeattype = 0
        if self.repeat_var.get() == 1:
            repeattype = 1

    def start_button2(self):
        if clicktype == "Single" or clicktype == "Double" or clicktype == "Triple":
            threading.Thread(target=self.autoClick).start()
            self.start_auto_button.configure(state="disabled")
            self.stop_auto_button.configure(state="enabled")
        else:
            threading.Thread(target=self.autoHold).start()
            self.start_auto_button.configure(state="disabled")
            self.stop_auto_button.configure(state="enabled")

    def on_press(self, key):
        global pause

        if self.auto1 and key == autoclick_key:
            self.auto1 = False
            pause = True
            self.stop_button2()

        if self.auto and key == holdm_key:
            self.auto = False
            pause = True
            self.stop_button2()

    def autoHold(self):
        self.auto = True
        self.auto1 = False
        pause = False

        lis = Listener(on_press=self.on_press)
        lis.start()

        while self.auto:
            if not pause:
                if button1 == "left":
                    pyautogui.mouseDown(button="left")
                if button1 == "middle":
                    pyautogui.mouseDown(button="middle")
                if button1 == "right":
                    pyautogui.mouseDown(button="right")
            if pause:
                break
        lis.stop()

    def autoClick(self):
        self.auto = False
        self.auto1 = True
        pause = False

        lis = Listener(on_press=self.on_press)
        lis.start()

        self.interval = float(self.clickinterval.get())
        if repeattype == 1:
            while self.auto1:
                if not pause:
                    if button1 == "left" and clicktype == "Single":
                        pyautogui.click(button="left")
                        pyautogui.PAUSE = self.interval
                    if button1 == "middle" and clicktype == "Single":
                        pyautogui.click(button="middle")
                        pyautogui.PAUSE = self.interval
                    if button1 == "right" and clicktype == "Single":
                        pyautogui.click(button="right")
                        pyautogui.PAUSE = self.interval

                    if button1 == "left" and clicktype == "Double":
                        pyautogui.doubleClick(button="left")
                        pyautogui.PAUSE = self.interval
                    if button1 == "middle" and clicktype == "Double":
                        pyautogui.doubleClick(button="middle")
                        pyautogui.PAUSE = self.interval
                    if button1 == "right" and clicktype == "Double":
                        pyautogui.doubleClick(button="right")
                        pyautogui.PAUSE = self.interval

                    if button1 == "left" and clicktype == "Triple":
                        pyautogui.tripleClick(button="left")
                        pyautogui.PAUSE = self.interval
                    if button1 == "middle" and clicktype == "Triple":
                        pyautogui.tripleClick(button="middle")
                        pyautogui.PAUSE = self.interval
                    if button1 == "right" and clicktype == "Triple":
                        pyautogui.tripleClick(button="right")
                        pyautogui.PAUSE = self.interval
                if pause:
                    break
        else:
            for i in range(int(self.repeattimes.get()) + 1):
                if not pause:
                    if button1 == "left" and clicktype == "Single":
                        pyautogui.click(button="left")
                        pyautogui.PAUSE = self.interval
                    if button1 == "middle" and clicktype == "Single":
                        pyautogui.click(button="middle")
                        pyautogui.PAUSE = self.interval
                    if button1 == "right" and clicktype == "Single":
                        pyautogui.click(button="right")
                        pyautogui.PAUSE = self.interval

                    if button1 == "left" and clicktype == "Double":
                        pyautogui.doubleClick(button="left")
                        pyautogui.PAUSE = self.interval
                    if button1 == "middle" and clicktype == "Double":
                        pyautogui.doubleClick(button="middle")
                        pyautogui.PAUSE = self.interval
                    if button1 == "right" and clicktype == "Double":
                        pyautogui.doubleClick(button="right")
                        pyautogui.PAUSE = self.interval

                    if button1 == "left" and clicktype == "Triple":
                        pyautogui.tripleClick(button="left")
                        pyautogui.PAUSE = self.interval
                    if button1 == "middle" and clicktype == "Triple":
                        pyautogui.tripleClick(button="middle")
                        pyautogui.PAUSE = self.interval
                    if button1 == "right" and clicktype == "Triple":
                        pyautogui.tripleClick(button="right")
                        pyautogui.PAUSE = self.interval

                    if i == int(self.repeattimes.get()):
                        pause = True

                if pause:
                    pause = True
                    self.auto1 = False
                    self.stop_button2()
                    break
        lis.stop()

    def stop_button2(self):
        pause = True

        if button1 == "left" and clicktype == "Single":
            self.auto1 = False
            pyautogui.mouseUp(button="left")
        if button1 == "middle" and clicktype == "Single":
            self.auto1 = False
            pyautogui.mouseUp(button="middle")
        if button1 == "right" and clicktype == "Single":
            self.auto1 = False
            pyautogui.mouseUp(button="right")

        if button1 == "left" and clicktype == "Double":
            self.auto1 = False
            pyautogui.mouseUp(button="left")
        if button1 == "middle" and clicktype == "Double":
            self.auto1 = False
            pyautogui.mouseUp(button="middle")
        if button1 == "right" and clicktype == "Double":
            self.auto1 = False
            pyautogui.mouseUp(button="right")

        if button1 == "left" and clicktype == "Triple":
            self.auto1 = False
            pyautogui.mouseUp(button="left")
        if button1 == "middle" and clicktype == "Triple":
            self.auto1 = False
            pyautogui.mouseUp(button="middle")
        if button1 == "right" and clicktype == "Triple":
            self.auto1 = False
            pyautogui.mouseUp(button="right")

        if button1 == "left" and clicktype == "Hold":
            self.auto = False
            pyautogui.mouseUp(button="left")
        if button1 == "middle" and clicktype == "Hold":
            self.auto = False
            pyautogui.mouseUp(button="middle")
        if button1 == "right" and clicktype == "Hold":
            self.auto = False
            pyautogui.mouseUp(button="right")

        self.start_auto_button.configure(state="enabled")
        self.stop_auto_button.configure(state="disabled")

    def on_close(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.attributes("-topmost", True)
    app.resizable(False, False)
    app.update()
    app.start()
