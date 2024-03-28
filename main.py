import time
import customtkinter
import pyautogui

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto Clicker")
        self.geometry("500x300")

        self.label_input_clicks = customtkinter.CTkLabel(self, text="Enter amount of clicks:")
        self.label_input_clicks.grid(row=0, column=0, padx=5, pady=5)
        self.input_clicks = customtkinter.CTkEntry(self, placeholder_text="0")
        self.input_clicks.grid(row=0, column=1, padx=5, pady=5)

        self.label_input_delay = customtkinter.CTkLabel(self, text="Enter amount of delay between clicks:")
        self.label_input_delay.grid(row=1, column=0, padx=5, pady=5)
        self.input_delay = customtkinter.CTkEntry(self, placeholder_text="0")
        self.input_delay.grid(row=1, column=1, padx=5, pady=5)

        self.label_countdown = customtkinter.CTkLabel(self, text="")
        self.label_countdown.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

        self.label_countdown_info = customtkinter.CTkLabel(self, text="after starting the program you have 3 seconds "
                                                                      "to place the mouse")
        self.label_countdown_info.grid(row=4, column=0, padx=5, pady=5, columnspan=2)
        self.start_button = customtkinter.CTkButton(self, text="Start", command=self.countdown)
        self.start_button.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    def countdown(self, count=3) -> None:
        if count > 0:
            self.label_countdown.configure(text=f"{count}...")
            self.after(1000, self.countdown, count - 1)
        else:
            self.start_clicker()

    def start_clicker(self) -> None:
        i = 0
        clicks = int(self.input_clicks.get())
        delay = float(self.input_delay.get())
        while i < clicks:
            pyautogui.click()
            print("clicked")
            i = i + 1
            time.sleep(delay)


if __name__ == '__main__':
    app = App()
    app.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
