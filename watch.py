import tkinter as tk
from tkinter import messagebox
import datetime
import time
import winsound

class MultiFunctionClock:
    def __init__(self, master):
        self.master = master
        self.master.title("Multi-Function Clock")
        self.master.configure(background='black')

        self.create_widgets()
        self.update_current_time()

    def create_widgets(self):
        self.tab_buttons_frame = tk.Frame(self.master, background='black')
        self.tab_buttons_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.tab_frames = {}

        button_width = 15
        for tab_name in ["Time", "Alarm Clock", "Stopwatch", "Countdown"]:
            button = tk.Button(self.tab_buttons_frame, text=tab_name, font=("ds-digital", 18), background="black", foreground="cyan", width=button_width, command=lambda name=tab_name: self.show_tab(name))
            button.pack(side=tk.LEFT, padx=10, pady=10)

            frame = tk.Frame(self.master, background='black')
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.tab_frames[tab_name] = frame

        self.create_current_time_tab()
        self.create_alarm_clock_tab()
        self.create_stopwatch_tab()
        self.create_countdown_timer_tab()

        self.show_tab("Time")

    def show_tab(self, tab_name):
        for frame in self.tab_frames.values():
            frame.pack_forget()
        self.tab_frames[tab_name].pack(fill=tk.BOTH, expand=True)

    def create_current_time_tab(self):
        frame = self.tab_frames["Time"]
        self.current_time_label = tk.Label(frame, font=("ds-digital", 80), background="black", foreground="cyan")
        self.current_time_label.pack(anchor='center', pady=50)

    def update_current_time(self):
        current_time = datetime.datetime.now().strftime('%H:%M:%S %p')
        self.current_time_label.config(text=current_time)
        self.master.after(1000, self.update_current_time)

    def create_alarm_clock_tab(self):
        frame = self.tab_frames["Alarm Clock"]

        tk.Label(frame, text="Enter alarm time (HH:MM):", font=("ds-digital", 18), background='black', foreground='cyan').pack(pady=10)
        self.alarm_time = tk.StringVar()
        self.alarm_entry = tk.Entry(frame, textvariable=self.alarm_time, font=("ds-digital", 18), background="cyan", foreground="black", justify='center')
        self.alarm_entry.pack(pady=10)

        tk.Button(frame, text="Set Alarm", font=("ds-digital", 18), background="black", foreground="cyan", width=20, command=self.set_alarm).pack(pady=20)

    def set_alarm(self):
        alarm_time_str = self.alarm_time.get()
        try:
            alarm_time_obj = datetime.datetime.strptime(alarm_time_str, "%H:%M")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid time format! Use HH:MM")
            return
        
        current_time = datetime.datetime.now()
        alarm_time_today = alarm_time_obj.replace(year=current_time.year, month=current_time.month, day=current_time.day)
        
        if alarm_time_today < current_time:
            alarm_time_today += datetime.timedelta(days=1)
        
        time_diff = (alarm_time_today - current_time).total_seconds()
        self.master.after(int(time_diff * 1000), self.trigger_alarm)

    def trigger_alarm(self):
        tk.messagebox.showinfo("Alarm", "It's time to wake up!")
        winsound.Beep(440, 1000)

    def create_stopwatch_tab(self):
        frame = self.tab_frames["Stopwatch"]

        self.stopwatch_time_label = tk.Label(frame, font=("ds-digital", 80), background="black", foreground="cyan")
        self.stopwatch_time_label.pack(anchor='center', pady=50)

        button_frame = tk.Frame(frame, background='black')
        button_frame.pack(pady=20)

        self.stopwatch_running = False
        self.stopwatch_start_time = None
        self.stopwatch_elapsed_time = 0

        button_width = 15

        tk.Button(button_frame, text="Start", font=("ds-digital", 18), background="black", foreground="cyan", width=button_width, command=self.start_stopwatch).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Stop", font=("ds-digital", 18), background="black", foreground="cyan", width=button_width, command=self.stop_stopwatch).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Reset", font=("ds-digital", 18), background="black", foreground="cyan", width=button_width, command=self.reset_stopwatch).pack(side=tk.LEFT, padx=10)

        self.update_stopwatch()

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_elapsed_time = time.time() - self.stopwatch_start_time
        elapsed_time_str = self.format_time(self.stopwatch_elapsed_time)
        self.stopwatch_time_label.config(text=elapsed_time_str)
        self.master.after(100, self.update_stopwatch)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed_time
            self.stopwatch_running = True

    def stop_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_elapsed_time = time.time() - self.stopwatch_start_time
            self.stopwatch_running = False

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_start_time = None
        self.stopwatch_elapsed_time = 0
        self.stopwatch_time_label.config(text="00:00:00")

    def create_countdown_timer_tab(self):
        frame = self.tab_frames["Countdown"]

        self.countdown_time_left = tk.IntVar(value=60)
        self.countdown_running = False

        self.countdown_time_label = tk.Label(frame, font=("ds-digital", 80), background="black", foreground="cyan")
        self.countdown_time_label.pack(anchor='center', pady=50)

        entry_frame = tk.Frame(frame, background='black')
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Set time (seconds):", font=("ds-digital", 18), background='black', foreground='cyan').pack(side=tk.LEFT, padx=10)
        self.countdown_entry = tk.Entry(entry_frame, textvariable=self.countdown_time_left, font=("ds-digital", 18), background="cyan", foreground="black", justify='center')
        self.countdown_entry.pack(side=tk.LEFT, padx=10)

        button_frame = tk.Frame(frame, background='black')
        button_frame.pack(pady=20)

        button_width = 15

        tk.Button(button_frame, text="Start", font=("ds-digital", 18), background="black", foreground="cyan", width=button_width, command=self.start_countdown).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Stop", font=("ds-digital", 18), background="black", foreground="cyan", width=button_width, command=self.stop_countdown).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Reset", font=("ds-digital", 18), background="black", foreground="cyan", width=button_width, command=self.reset_countdown).pack(side=tk.LEFT, padx=10)

        self.update_countdown_timer()

    def update_countdown_timer(self):
        if self.countdown_running and self.countdown_time_left.get() > 0:
            self.countdown_time_left.set(self.countdown_time_left.get() - 1)
        if self.countdown_time_left.get() <= 0 and self.countdown_running:
            self.countdown_running = False
            self.time_up()
        self.countdown_time_label.config(text=self.format_time(self.countdown_time_left.get()))
        self.master.after(1000, self.update_countdown_timer)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{int(hours):02}:{int(mins):02}:{int(secs):02}"

    def start_countdown(self):
        if not self.countdown_running:
            self.countdown_running = True

    def stop_countdown(self):
        if self.countdown_running:
            self.countdown_running = False

    def reset_countdown(self):
        self.countdown_running = False
        self.countdown_time_left.set(60)
        self.countdown_time_label.config(text="00:01:00")

    def time_up(self):
        tk.messagebox.showinfo("Time's up!", "The countdown has finished.")

def main():
    root = tk.Tk()
    root.geometry("800x600") 
    app = MultiFunctionClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()