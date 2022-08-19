import os
from pynput.keyboard import Controller
from PIL import Image, ImageTk
import pyautogui
import customtkinter
import keyboard as keyboard1
import threading
import pydirectinput

customtkinter.set_appearance_mode("black")
customtkinter.set_default_color_theme("blue")


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

    def autoHold(self):
        auto = True

        keyboard = Controller()

        while auto:
            pyautogui.mouseDown()
            if keyboard1.is_pressed('f6'):
                auto = False
                pyautogui.mouseUp()
                self.start_hold_button.configure(state="enabled")
                break

    def autoClick(self):
        auto1 = True

        while auto1:
            pyautogui.click()
            pydirectinput.press('x')
            if keyboard1.is_pressed('f5'):
                auto1 = False
                pyautogui.mouseUp()
                self.start_auto_button.configure(state="enabled")
                break

    def stop_button1(self):
        auto = False
        self.start_hold_button.configure(state="enabled")

    def stop_button2(self):
        auto1 = False
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
