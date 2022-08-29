import os
from PIL import Image, ImageTk
from pynput.keyboard import *
import pyautogui
import customtkinter
import threading
import pydirectinput

customtkinter.set_appearance_mode("black")
customtkinter.set_default_color_theme("blue")

autoclick_key = Key.f5
holdm_key = Key.f6

pause = False


class App(customtkinter.CTk):

    auto = False
    auto1 = False

    WIDTH = 300
    HEIGHT = 500

    def __init__(self):
        super().__init__()

        p1 = ImageTk.PhotoImage(Image.open(os.path.abspath("mouse.ico")))

        self.iconphoto(False, p1)

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

        self.hold_down_text = customtkinter.CTkLabel(
            master=self.frame, text="Mouse hold down", text_font=("Roboto Medium", -16))
        self.hold_down_text.grid(row=2, column=1, pady=10)

        self.start_hold_button = customtkinter.CTkButton(master=self.frame, text="Start", fg_color=(
            "black"), text_font=("Roboto Medium", -16), command=self.start_button1)
        self.start_hold_button.grid(row=3, column=1, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.stop_hold_button = customtkinter.CTkButton(master=self.frame, text="Stop", fg_color=(
            "black"), text_font=("Roboto Medium", -16), command=self.stop_button1)
        self.stop_hold_button.grid(row=4, column=1, pady=10)

        self.auto_clicker = customtkinter.CTkLabel(
            master=self.frame, text="AutoClick", text_font=("Roboto Medium", -16))
        self.auto_clicker.grid(row=5, column=1, pady=10)

        self.start_auto_button = customtkinter.CTkButton(master=self.frame, text="Start", fg_color=(
            "black"), text_font=("Roboto Medium", -16), command=self.start_button2)
        self.start_auto_button.grid(row=6, column=1, pady=10)

        self.stop_auto_button = customtkinter.CTkButton(master=self.frame, text="Stop", fg_color=(
            "black"), text_font=("Roboto Medium", -16), command=self.stop_button2)
        self.stop_auto_button.grid(row=7, column=1, pady=10)

    def start_button1(self):
        threading.Thread(target=self.autoHold).start()
        self.start_hold_button.configure(state="disabled")

    def start_button2(self):
        threading.Thread(target=self.autoClick).start()
        self.start_auto_button.configure(state="disabled")

    def on_press(self, key):
        global pause

        if self.auto1 and key == autoclick_key:
            self.auto1 = False
            pause = True
            self.stop_button2()

        if self.auto and key == holdm_key:
            self.auto = False
            pause = True
            self.stop_button1()

    def autoHold(self):
        self.auto = True
        self.auto1 = False
        pause = False

        lis = Listener(on_press=self.on_press)
        lis.start()

        while self.auto:
            if not pause:
                pyautogui.mouseDown()
            if pause:
                break
        lis.stop()

    def autoClick(self):
        self.auto = False
        self.auto1 = True
        pause = False

        lis = Listener(on_press=self.on_press)
        lis.start()

        while self.auto1:
            if not pause:
                pyautogui.click()
                pydirectinput.press('x')
            if pause:
                break
        lis.stop()

    def stop_button1(self):
        pause = True
        self.auto = False
        pyautogui.mouseUp()
        self.start_hold_button.configure(state="enabled")

    def stop_button2(self):
        pause = True
        self.auto1 = False
        pyautogui.mouseUp()
        self.start_auto_button.configure(state="enabled")

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
