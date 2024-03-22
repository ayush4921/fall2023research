import tkinter as tk
from tkinter import PhotoImage
import threading
import sounddevice as sd
import soundfile as sf
import queue
from pydub import AudioSegment
import os
import numpy as np
import logging
import gym
from minerl.herobraine.env_specs.human_survival_specs import HumanSurvival

import coloredlogs

coloredlogs.install(logging.DEBUG)
env_commands = queue.Queue()


def environment_manager():
    global env_running
    env = gym.make("MineRLObtainDiamondShovel-v0")
    env.reset()

    while True:
        command = env_commands.get()  # Wait for the next command
        if command == "start":
            env_running = True
            for _ in range(100):  # Example interaction loop
                if not env_running:
                    break  # Stop the loop if env_running is set to False
                ac = env.action_space.noop()
                ac["camera"] = [0.0, 360 / 100]
                env.step(ac)
                env.render()
            env.reset()
        elif command == "stop":
            env_running = False
        elif command == "exit":
            env.close()
            break


class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        self.filename = None
        self.recording_number = 0

    def start_recording(self):
        self.filename = f"recording_{self.recording_number}.wav"
        self.is_recording = True
        self.stream = sd.InputStream(callback=self.audio_callback)
        self.stream.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.stream:
                self.stream.stop()
                self.stream = None
                self.save_recording()

    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.audio_queue.put(indata.copy())

    def save_recording(self):
        audio_data = []
        while not self.audio_queue.empty():
            audio_data.append(self.audio_queue.get())

        if audio_data:
            audio_data = np.concatenate(audio_data, axis=0)
            sf.write(self.filename, audio_data, samplerate=44100)
            self.convert_to_mp3()

    def convert_to_mp3(self):
        audio = AudioSegment.from_wav(self.filename)
        mp3_filename = self.filename.replace(".wav", ".mp3")
        audio.export(mp3_filename, format="mp3")
        os.remove(self.filename)

    def reset_recording(self):
        self.recording_number += 1
        self.filename = None
        while not self.audio_queue.empty():
            self.audio_queue.get()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_widgets()
        self.recorder = AudioRecorder()
        self.status = "Stop"  # Start, Stop, Reset
        self.update_colors()

    def create_widgets(self):
        self.start_button = tk.Button(
            self, text="Start", command=self.start, width=20, height=2
        )
        self.start_button.pack(side="top", pady=10)

        self.stop_button = tk.Button(
            self, text="Stop", command=self.stop, width=20, height=2
        )
        self.stop_button.pack(side="top", pady=10)

        self.reset_button = tk.Button(
            self, text="Reset", command=self.reset, width=20, height=2
        )
        self.reset_button.pack(side="top", pady=10)

    def start(self):
        self.status = "Start"
        self.update_colors()
        self.recorder.start_recording()

    def stop(self):
        self.status = "Stop"
        self.update_colors()
        self.recorder.stop_recording()

    def reset(self):
        self.status = "Reset"
        self.update_colors()
        self.recorder.reset_recording()

    def update_colors(self):
        if self.status == "Start":
            self.configure(bg="green")
        elif self.status == "Stop":
            self.configure(bg="red")
        elif self.status == "Reset":
            self.configure(bg="yellow")

    def on_closing(self):
        if self.recorder.is_recording:
            self.recorder.stop_recording()
        self.master.destroy()


def status_monitor(app, stop_event):
    while not stop_event.is_set():
        if app.status == "Start" and not env_running:
            env_commands.put("start")
        elif app.status == "Stop":
            env_commands.put("stop")
    env_commands.put("exit")


root = tk.Tk()
root.title("Audio Recorder")
app = Application(master=root)
app.master.geometry("400x300")


env_thread = threading.Thread(target=environment_manager, daemon=True)
env_thread.start()

root = tk.Tk()
root.title("Audio Recorder")
app = Application(master=root)
app.master.geometry("400x300")
stop_event = threading.Event()
thread = threading.Thread(target=status_monitor, args=(app, stop_event), daemon=True)
thread.start()
root.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()

# After mainloop ends
stop_event.set()
env_commands.put("exit")  # Ensure the environment manager thread exits
env_thread.join()
