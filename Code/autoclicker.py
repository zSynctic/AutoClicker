# Author: Synctic
# License: GPL-3.0 | Copyright (c) 2022 Synctic
# Version: 1.1.0

from PIL import Image, ImageTk
from CTkToolTip import *
from pynput.keyboard import *
from pynput.keyboard import Key, Listener
from pynput import keyboard
import time
import webbrowser
import pydirectinput
import sys
import os
import pydirectinput
import customtkinter
import threading
import json
import queue
import re
import urllib.request
import spinbox as spinbox

APP_VERSION = "1.1.0"
UPDATE_INFO_URL = "https://zclicker.com/api/zclicker-free/latest"
UPDATE_CHECK_INTERVAL_SECONDS = 72 * 60 * 60

autoclick_key = Key.f5

button1 = "Left"
clicktype = "Single"
repeattype = 1


class App(customtkinter.CTk):
    auto = False
    auto1 = False

    WIDTH = 315
    HEIGHT = 500

    global resource

    def resource(relative_path):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        return os.path.join(base_path, relative_path)

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    def __init__(self):
        super().__init__()

        self.title("ZClicker")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.p1 = ImageTk.PhotoImage(file=resource("Assets/icon.ico"))
        
        self.wm_iconbitmap()
        self.iconphoto(False, self.p1)
        
        self.pause = False
        self.update_result_queue = queue.Queue()
        self.update_check_thread = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(5, weight=1)

        self.titlel = customtkinter.CTkLabel(
            master=self.frame,
            text="ZClicker",
            font=("Roboto Medium", -16),
            cursor="hand2",
        )
        self.titlel.grid(row=1, column=1, pady=10)
        
        self.tooltip = CTkToolTip(
            self.titlel,
            message="Open ZClicker Website",
            delay=0,
        )

        self.titlel.bind(
            "<Button-1>",
            lambda event: webbrowser.open_new_tab(
                "https://ZClicker.com"
            ),
        )

        self.copyright = customtkinter.CTkButton(
            master=self.frame,
            text="""Copyright (C) 2022 - ZClicker
By zSynctic""",
            text_color="#686F7A",
            bg_color="transparent",
            fg_color="transparent",
            hover_color="#2B2B2B",
            cursor="hand2",
            font=("Roboto Medium", -9),
        )
        self.copyright.place(x=75, y=32)

        self.copyright.bind(
            "<Button-1>",
            lambda event: webbrowser.open_new_tab(
                "https://github.com/zSynctic/AutoClicker"
            ),
        )

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        def show_premium_popup(feature_name):
            feature_benefits = {
                "Background Window Clicker": (
                    "Keep clicking a selected window while you work elsewhere."
                ),
                "Click Position": (
                    "Choose an exact screen position for every automated click."
                ),
                "Settings": (
                    "Customize your hotkey, appearance, and always-on-top behavior."
                ),
                "CPS Test": (
                    "Measure your clicking speed and track your clicks per second."
                ),
                "Macro Recorder": (
                    "Record, edit, save, and replay complete mouse and keyboard workflows."
                ),
                "Presets": (
                    "Save multiple clicking setups and macros as reusable presets."
                ),
            }

            if (
                hasattr(self, "premium_popup")
                and self.premium_popup.winfo_exists()
            ):
                self.premium_popup.focus_force()
                return

            self.premium_popup = customtkinter.CTkToplevel(self)
            self.premium_popup.title("Premium Feature")
            self.premium_popup.geometry("420x360")
            self.premium_popup.resizable(False, False)
            self.premium_popup.configure(fg_color="#242424")
            self.premium_popup.transient(self)
            self.premium_popup.grab_set()
            self.premium_popup.after(
                200,
                lambda: self.premium_popup.iconbitmap(
                    resource("Assets/icon.ico")
                ),
            )

            self.premium_popup.update_idletasks()
            popup_x = (self.premium_popup.winfo_screenwidth() - 420) // 2
            popup_y = (self.premium_popup.winfo_screenheight() - 360) // 2
            self.premium_popup.geometry(f"+{popup_x}+{popup_y}")

            premium_card = customtkinter.CTkFrame(
                master=self.premium_popup,
                fg_color="#2B2B2B",
                corner_radius=10,
            )
            premium_card.pack(fill="both", expand=True, padx=18, pady=18)

            premium_title = customtkinter.CTkLabel(
                master=premium_card,
                text="🔒 Premium Feature",
                font=("Roboto Medium", -20, "bold"),
                text_color="white",
            )
            premium_title.pack(pady=(18, 8))

            premium_message = customtkinter.CTkLabel(
                master=premium_card,
                text=(
                    f"{feature_benefits[feature_name]}\n\n"
                    "Available in ZClicker Pro with a simple\n"
                    "one-time payment."
                ),
                font=("Roboto Medium", -14),
                text_color="#B9B9B9",
                justify="center",
                wraplength=340,
            )
            premium_message.pack(pady=(0, 12))

            support_message = customtkinter.CTkLabel(
                master=premium_card,
                text="Purchases help support continued updates and website hosting.",
                font=("Roboto Medium", -11),
                text_color="#858585",
                justify="center",
                wraplength=340,
            )
            support_message.pack(pady=(0, 14))

            def open_zclicker_pro():
                webbrowser.open("https://zclicker.com")
                self.premium_popup.destroy()

            premium_upgrade_button = customtkinter.CTkButton(
                master=premium_card,
                text="🚀 Get ZClicker Pro",
                width=310,
                height=42,
                fg_color="#1F6AA5",
                hover_color="#144870",
                corner_radius=6,
                font=("Roboto Medium", -15, "bold"),
                cursor="hand2",
                command=open_zclicker_pro,
            )
            premium_upgrade_button.pack(pady=(0, 10))

            maybe_later_button = customtkinter.CTkButton(
                master=premium_card,
                text="Maybe Later",
                width=310,
                height=42,
                fg_color="#242424",
                hover_color="#2B2B2B",
                border_width=1,
                border_color="#949A9F",
                text_color="white",
                corner_radius=6,
                command=self.premium_popup.destroy,
            )
            maybe_later_button.pack(pady=(0, 18))

            self.premium_popup.protocol(
                "WM_DELETE_WINDOW", self.premium_popup.destroy
            )
            self.premium_popup.focus_force()

        self.settings_image = customtkinter.CTkImage(
            dark_image=Image.open(resource("Assets/darksettings.png")),
            light_image=Image.open(resource("Assets/lightsettings.png")),
            size=(20, 20),
        )

        self.cps_image = customtkinter.CTkImage(
            dark_image=Image.open(resource("Assets/darkclick.png")),
            light_image=Image.open(resource("Assets/lightclick.png")),
            size=(20, 20),
        )

        self.start_auto_button = customtkinter.CTkButton(
            master=self.frame,
            text="Start",
            width=123,
            height=36,
            fg_color="#1F6AA5",
            hover_color="#2878B5",
            text_color="white",
            font=("Roboto Medium", -16),
            command=self.start_button,
        )
        self.start_auto_button.place(x=20, y=328)

        self.stop_auto_button = customtkinter.CTkButton(
            master=self.frame,
            text="Stop",
            width=123,
            height=36,
            fg_color="#242424",
            hover_color="#2B2B2B",
            border_color="#949A9F",
            border_width=1,
            text_color="white",
            font=("Roboto Medium", -15),
            state="disabled",
            command=self.stop_button,
        )
        self.stop_auto_button.place(x=152, y=328)

        self.click_position_button = customtkinter.CTkButton(
            master=self.frame,
            text="Click Position 🔒",
            width=255,
            height=32,
            fg_color="#242424",
            border_color="#949A9F",
            border_width=1,
            font=("Roboto Medium", -14),
            cursor="hand2",
            command=lambda: show_premium_popup("Click Position"),
        )
        self.click_position_button.place(x=20, y=200)

        self.background_click_button = customtkinter.CTkButton(
            master=self.frame,
            text="Background Window Clicker 🔒",
            width=255,
            height=32,
            fg_color="#242424",
            border_color="#949A9F",
            border_width=1,
            font=("Roboto Medium", -14),
            cursor="hand2",
            command=lambda: show_premium_popup("Background Window Clicker"),
        )
        self.background_click_button.place(x=20, y=240)

        self.macro_recorder_button = customtkinter.CTkButton(
            master=self.frame,
            text="Macro Recorder 🔒",
            width=123,
            height=32,
            fg_color="#242424",
            border_color="#949A9F",
            border_width=1,
            font=("Roboto Medium", -12),
            cursor="hand2",
            command=lambda: show_premium_popup("Macro Recorder"),
        )
        self.macro_recorder_button.place(x=20, y=280)

        self.profiles_button = customtkinter.CTkButton(
            master=self.frame,
            text="Presets 🔒",
            width=123,
            height=32,
            fg_color="#242424",
            border_color="#949A9F",
            border_width=1,
            font=("Roboto Medium", -13),
            cursor="hand2",
            command=lambda: show_premium_popup("Presets"),
        )
        self.profiles_button.place(x=152, y=280)

        self.buttonmenu_var = customtkinter.StringVar(value="Left")

        self.buttonmenu = customtkinter.CTkComboBox(
            master=self.frame,
            font=("Roboto Medium", -14),
            width=115,
            fg_color="black",
            button_color="black",
            variable=self.buttonmenu_var,
            command=self.buttonmenu_event,
            values=["Left", "Middle", "Right"],
        )
        self.buttonmenu.place(x=20, y=90)

        self.buttonmenu.bind("<Return>", lambda e: self.custombutton())

        self.buttontxt = customtkinter.CTkLabel(
            master=self.frame, text="Button:", font=("Roboto Medium", -15)
        )
        self.buttontxt.place(x=46, y=60)

        self.clicktype_var = customtkinter.StringVar(value="Single")

        self.clicktypemenu = customtkinter.CTkOptionMenu(
            master=self.frame,
            font=("Roboto Medium", -14),
            width=115,
            fg_color="black",
            button_color="black",
            variable=self.clicktype_var,
            command=self.clicktype_event,
            values=["Single", "Double", "Triple", "Hold"],
        )
        self.clicktypemenu.place(x=160, y=90)

        self.clicktypetxt = customtkinter.CTkLabel(
            master=self.frame, text="Click Type:", font=("Roboto Medium", -15)
        )
        self.clicktypetxt.place(x=180, y=60)

        self.clickinterval_var = customtkinter.StringVar(
            master=self.frame, value=str(0.01)
        )

        self.clickinterval = customtkinter.CTkEntry(
            master=self.frame,
            font=("Roboto Medium", -14),
            width=80,
            textvariable=self.clickinterval_var,
        )
        self.clickinterval.place(x=110, y=411)

        self.clickintervaltxt = customtkinter.CTkLabel(
            master=self.frame, text="Click interval", font=("Roboto Medium", -14)
        )
        self.clickintervaltxt.place(x=108, y=382)

        self.secondstxt = customtkinter.CTkLabel(
            master=self.frame, text="secs", font=("Roboto Medium", -13), width=10
        )
        self.secondstxt.place(x=195, y=416)

        self.upgrade_btn = customtkinter.CTkButton(
            master=self.frame,
            text="Upgrade to Pro",
            width=160,
            height=25,
            fg_color="transparent",
            bg_color="transparent",
            hover_color="#2B2B2B",
            text_color="#1F6AA5",
            font=("Roboto Condensed", -13, "underline"),
            cursor="hand2",
            command=lambda: webbrowser.open_new_tab("https://zclicker.com"),
        )
        self.upgrade_btn.place(x=68, y=448)

        self.settings_button = customtkinter.CTkButton(
            master=self.frame,
            text="",
            image=self.settings_image,
            width=20,
            height=20,
            bg_color="transparent",
            fg_color="transparent",
            hover_color="#2B2B2B",
            cursor="hand2",
            command=lambda: show_premium_popup("Settings"),
        )
        self.settings_button.place(x=0, y=447)

        self.settings_tooltip = CTkToolTip(
            widget=self.settings_button,
            message="Settings 🔒",
            delay=0,
        )

        self.cps_test_button = customtkinter.CTkButton(
            master=self.frame,
            text="",
            image=self.cps_image,
            width=20,
            height=20,
            bg_color="transparent",
            fg_color="transparent",
            hover_color="#2B2B2B",
            cursor="hand2",
            command=lambda: show_premium_popup("CPS Test"),
        )
        self.cps_test_button.place(x=258, y=445)

        self.cps_tooltip = CTkToolTip(
            widget=self.cps_test_button,
            message="CPS Test 🔒",
            delay=0,
        )

        self.repeat_var = customtkinter.IntVar()
        self.repeat_var.set(value=1)

        self.repeat = customtkinter.CTkRadioButton(
            master=self.frame,
            text="Repeat",
            value=0,
            variable=self.repeat_var,
            command=self.repeat_event,
            font=("Roboto Medium", -13),
            width=20,
            height=20,
        )
        self.repeat.place(x=20, y=140)

        self.repeatstopped = customtkinter.CTkRadioButton(
            master=self.frame,
            text="Repeat until stopped",
            value=1,
            variable=self.repeat_var,
            command=self.repeat_event,
            font=("Roboto Medium", -13),
            width=20,
            height=20,
        )
        self.repeatstopped.place(x=20, y=170)

        self.repeattimes = spinbox.FloatSpinbox(
            master=self.frame, width=105, height=25, step_size=1
        )
        self.repeattimes.place(x=160, y=135)

        self.lis2 = keyboard.Listener(on_press=self.on_press1)
        self.lis2.start()

        self.repeattimes.set(1)
        self.repeatstopped.select()
        self.after(1500, self.check_for_updates)

    def buttonmenu_event(self, choice5):
        global button1
        self.choice5 = choice5

        if self.choice5 == "Left":
            button1 = "Left"
        elif self.choice5 == "Middle":
            button1 = "Middle"
        elif self.choice5 == "Right":
            button1 = "Right"

    def custombutton(self):
        global button1
        button1 = self.buttonmenu_var.get()
        self.frame.focus_set()

    def clicktype_event(self, choice):
        global clicktype

        if choice == "Single":
            clicktype = "Single"
        elif choice == "Double":
            clicktype = "Double"
        elif choice == "Triple":
            clicktype = "Triple"
        elif choice == "Hold":
            clicktype = "Hold"

    def repeat_event(self):
        global repeattype

        if self.repeat_var.get() == 0:
            repeattype = 0
        if self.repeat_var.get() == 1:
            repeattype = 1

    def start_button(self):
        if clicktype in ["Single", "Double", "Triple", "Hold"] and not self.pause:
            self.lis2.stop()
            self.pause = False

            self.autoclc = threading.Thread(target=self.autoClick)
            self.autoclc.start()

            self.buttonmenu.configure(state="normal")
            self.buttonmenu.configure(state="disabled")
            self.start_auto_button.configure(state="disabled")
            self.stop_auto_button.configure(state="enabled")

    def on_press1(self, key):
        if not self.auto1 and key == autoclick_key:
            self.pause = False
            self.auto1 = True
            self.lis2.stop()
            self.start_button()
    
    def on_press(self, key):
        if self.auto1 and key == autoclick_key:
            self.pause = True
            self.auto1 = False
            self.stop_button()
            self.lis2 = keyboard.Listener(on_press=self.on_press1)
            self.lis2.start()

    def autoClick(self):
        self.auto = False
        self.auto1 = True
        self.pause = False

        lis1 = Listener(on_press=self.on_press)
        lis1.start()
        try:
            try:
                self.interval = float(self.clickinterval.get())
            except ValueError:
                self.interval = 0.01
                
            if repeattype == 1:
                while self.auto1:
                    if not self.pause:
                        if clicktype == "Single":
                            if self.buttonmenu.get() == "Left":
                                pydirectinput.click(button="left")
                                pydirectinput.PAUSE = self.interval
                            elif self.buttonmenu.get() == "Middle":
                                pydirectinput.click(button="middle")
                                pydirectinput.PAUSE = self.interval
                            elif self.buttonmenu.get() == "Right":
                                pydirectinput.click(button="right")
                                pydirectinput.PAUSE = self.interval
                            else:
                                pydirectinput.press(
                                    key=button1.lower())
                                pydirectinput.PAUSE = self.interval

                        if clicktype == "Double":
                            if button1 == "Left":
                                pydirectinput.doubleClick(button="left")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Middle":
                                pydirectinput.doubleClick(button="middle")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Right":
                                pydirectinput.doubleClick(button="right")
                                pydirectinput.PAUSE = self.interval
                            else:
                                pydirectinput.press(
                                    key=button1.lower())
                                pydirectinput.PAUSE = self.interval

                        if clicktype == "Triple":
                            if button1 == "Left":
                                pydirectinput.tripleClick(button="left")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Middle":
                                pydirectinput.tripleClick(button="middle")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Right":
                                pydirectinput.tripleClick(button="right")
                                pydirectinput.PAUSE = self.interval
                            else:
                                pydirectinput.press(
                                    key=button1.lower())
                                pydirectinput.PAUSE = self.interval
                        
                        if clicktype == "Hold":
                            if button1 == "Left":
                                pydirectinput.mouseDown(button="left")
                            elif button1 == "Middle":
                                pydirectinput.mouseDown(button="middle")
                            elif button1 == "Right":
                                pydirectinput.mouseDown(button="right")
                            else:
                                pydirectinput.keyDown(key=button1.lower())
                                            
                            while self.auto1 and not self.pause:
                                time.sleep(0.05)
                                            
                            break
                    if self.pause:
                        break
            else:
                for i in range(int(self.repeattimes.get()) + 1):
                    if not self.pause:
                        if clicktype == "Single":
                            if self.buttonmenu.get() == "Left":
                                pydirectinput.click(button="left")
                                pydirectinput.PAUSE = self.interval
                            elif self.buttonmenu.get() == "Middle":
                                pydirectinput.click(button="middle")
                                pydirectinput.PAUSE = self.interval
                            elif self.buttonmenu.get() == "Right":
                                pydirectinput.click(button="right")
                                pydirectinput.PAUSE = self.interval
                            else:
                                pydirectinput.press(key=button1.lower())
                                pydirectinput.PAUSE = self.interval

                        if clicktype == "Double":
                            if button1 == "Left":
                                pydirectinput.doubleClick(button="left")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Middle":
                                pydirectinput.doubleClick(button="middle")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Right":
                                pydirectinput.doubleClick(button="right")
                                pydirectinput.PAUSE = self.interval
                            else:
                                pydirectinput.press(
                                    key=button1.lower())
                                pydirectinput.PAUSE = self.interval

                        if clicktype == "Triple":
                            if button1 == "Left":
                                pydirectinput.tripleClick(button="left")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Middle":
                                pydirectinput.tripleClick(button="middle")
                                pydirectinput.PAUSE = self.interval
                            elif button1 == "Right":
                                pydirectinput.tripleClick(button="right")
                                pydirectinput.PAUSE = self.interval
                            else:
                                pydirectinput.press(
                                    key=button1.lower())
                                pydirectinput.PAUSE = self.interval
                            
                        if clicktype == "Hold":
                            if button1 == "Left":
                                pydirectinput.mouseDown(button="left")
                            elif button1 == "Middle":
                                pydirectinput.mouseDown(button="middle")
                            elif button1 == "Right":
                                pydirectinput.mouseDown(button="right")
                            else:
                                pydirectinput.keyDown(key=button1.lower())
                                            
                            while self.auto1 and not self.pause:
                                time.sleep(0.05)
                                            
                            break

                        if i == int(self.repeattimes.get()):
                            self.pause = True

                    if self.pause:
                        self.auto1 = False
                        self.stop_button()
                        break
                
        finally:
            try:
                lis1.stop()
            except:
                pass

    def stop_button(self):
        self.pause = True

        if clicktype == "Single":
            if button1 == "Left":
                self.auto1 = False
                pydirectinput.mouseUp(button="left")
            elif button1 == "Middle":
                self.auto1 = False
                pydirectinput.mouseUp(button="middle")
            elif button1 == "Right":
                self.auto1 = False
                pydirectinput.mouseUp(button="right")

        if clicktype == "Double":
            if button1 == "Left":
                self.auto1 = False
                pydirectinput.mouseUp(button="left")
            elif button1 == "Middle":
                self.auto1 = False
                pydirectinput.mouseUp(button="middle")
            elif button1 == "Right":
                self.auto1 = False
                pydirectinput.mouseUp(button="right")

        if clicktype == "Triple":
            if button1 == "Left":
                self.auto1 = False
                pydirectinput.mouseUp(button="left")
            elif button1 == "Middle":
                self.auto1 = False
                pydirectinput.mouseUp(button="middle")
            elif button1 == "Right":
                self.auto1 = False
                pydirectinput.mouseUp(button="right")
        
        if clicktype == "Hold":
            if button1 == "Left":
                self.auto1 = False
                pydirectinput.mouseUp(button="left")
            elif button1 == "Middle":
                self.auto1 = False
                pydirectinput.mouseUp(button="middle")
            elif button1 == "Right":
                self.auto1 = False
                pydirectinput.mouseUp(button="right")
            else:
                self.auto1 = False
                pydirectinput.keyUp(key=self.buttonmenu.get().lower())

        self.buttonmenu.configure(state="normal")
        self.start_auto_button.configure(state="enabled")
        self.stop_auto_button.configure(state="disabled")

    @staticmethod
    def version_parts(version):
        numbers = [int(part) for part in re.findall(r"\d+", str(version))[:4]]
        return tuple(numbers + [0] * (4 - len(numbers)))

    @staticmethod
    def update_state_path():
        base_path = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
        return os.path.join(base_path, "ZClicker", "Free", "update_state.json")

    def update_check_due(self):
        try:
            with open(self.update_state_path(), "r", encoding="utf-8") as state_file:
                last_check = float(json.load(state_file).get("last_update_check", 0))
        except (OSError, ValueError, TypeError, AttributeError):
            last_check = 0

        return time.time() - last_check >= UPDATE_CHECK_INTERVAL_SECONDS

    def record_update_check(self):
        try:
            state_path = self.update_state_path()
            os.makedirs(os.path.dirname(state_path), exist_ok=True)
            with open(state_path, "w", encoding="utf-8") as state_file:
                json.dump({"last_update_check": int(time.time())}, state_file)
        except OSError:
            pass

    def check_for_updates(self):
        if not self.update_check_due():
            return

        # Record the attempt first so an offline computer does not retry on every launch.
        self.record_update_check()
        self.update_check_thread = threading.Thread(
            target=self.fetch_update_information,
            daemon=True,
        )
        self.update_check_thread.start()
        self.after(150, self.poll_update_result)

    def fetch_update_information(self):
        try:
            request = urllib.request.Request(
                UPDATE_INFO_URL,
                headers={"User-Agent": f"ZClicker-Free/{APP_VERSION}"},
            )
            with urllib.request.urlopen(request, timeout=4) as response:
                update_info = json.loads(response.read().decode("utf-8"))

            latest_version = str(update_info.get("version", "")).strip()
            if not latest_version or (
                self.version_parts(latest_version) <= self.version_parts(APP_VERSION)
            ):
                return

            release_notes = update_info.get("release_notes", [])
            if not isinstance(release_notes, list):
                release_notes = []
            release_notes = [str(note) for note in release_notes[:6]]
            download_url = str(update_info.get("download_url", "")).strip()
            if not download_url.startswith(("https://", "http://")):
                return

            self.update_result_queue.put(
                (latest_version, release_notes, download_url)
            )
        except (OSError, ValueError, TypeError):
            # Update checks must never delay or prevent the clicker from opening.
            return

    def poll_update_result(self):
        try:
            update_result = self.update_result_queue.get_nowait()
        except queue.Empty:
            if self.update_check_thread and self.update_check_thread.is_alive():
                self.after(150, self.poll_update_result)
            return

        self.show_update_available(*update_result)

    def show_update_available(self, latest_version, release_notes, download_url):
        if hasattr(self, "update_window") and self.update_window.winfo_exists():
            self.update_window.focus_force()
            return

        self.update_window = customtkinter.CTkToplevel(self)
        self.update_window.title("ZClicker Update")
        self.update_window.geometry("420x390")
        self.update_window.resizable(False, False)
        self.update_window.configure(fg_color="#242424")
        self.update_window.transient(self)
        self.update_window.grab_set()
        self.update_window.after(
            200,
            lambda: self.update_window.iconbitmap(resource("Assets/icon.ico")),
        )

        update_card = customtkinter.CTkFrame(
            self.update_window,
            fg_color="#2B2B2B",
            corner_radius=10,
        )
        update_card.pack(fill="both", expand=True, padx=18, pady=18)

        customtkinter.CTkLabel(
            update_card,
            text="Update Available",
            font=("Roboto Medium", -21, "bold"),
        ).pack(pady=(20, 5))

        customtkinter.CTkLabel(
            update_card,
            text=f"ZClicker {latest_version} is ready  •  Installed {APP_VERSION}",
            font=("Roboto Medium", -13),
            text_color="#B9B9B9",
        ).pack(pady=(0, 14))

        notes_text = "\n".join(f"• {note}" for note in release_notes)
        if not notes_text:
            notes_text = "A newer version of ZClicker is available."
        customtkinter.CTkLabel(
            update_card,
            text=notes_text,
            justify="left",
            anchor="w",
            wraplength=330,
            font=("Roboto Medium", -12),
            text_color="#D0D0D0",
        ).pack(fill="x", padx=26, pady=(0, 16))

        def download_update():
            webbrowser.open(download_url)
            self.update_window.destroy()

        customtkinter.CTkButton(
            update_card,
            text="Download Update",
            width=310,
            height=42,
            fg_color="#1F6AA5",
            hover_color="#144870",
            font=("Roboto Medium", -14, "bold"),
            cursor="hand2",
            command=download_update,
        ).pack(pady=(0, 10))

        customtkinter.CTkButton(
            update_card,
            text="Maybe Later",
            width=310,
            height=42,
            fg_color="#242424",
            hover_color="#333333",
            border_width=1,
            border_color="#949A9F",
            command=self.update_window.destroy,
        ).pack(pady=(0, 18))

        self.update_window.focus_force()

    def on_close(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.update()
    app.start()
