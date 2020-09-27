import os
import time
import pickle

import tkinter as tk
import tkinter.font as tk_font
import threading
from pygame import mixer


class StopWatch:
    def __init__(self):
        self.prev_path = '../prev.pickle'
        self.sound_path = '../sound/se_maoudamashii_jingle01.mp3'

        self.time_value = self.load_pickle(self.prev_path)
        if self.time_value is None:
            self.time_value = 0
        self.starting_time_value = self.time_value

        w0 = 40
        y0 = 60
        y02 = y0 -20

        w1 = 80
        h1 = 40
        wspace = 10

        w2 = w1 * 3 + wspace * 2
        h2 = 50

        x1 = 40
        x2 = x1 + w1 + wspace
        x3 = x2 + w1 + wspace
        x0 = x3 + 60

        y1 = 10
        y2 = 95
        y3 = 140

        size1 = 56
        bg1 = '#ffffee'
        bg2 = '#ffffaa'
        bg0 = '#ffccff'
        bg02 = '#ffaaff'

        self.root = tk.Tk()
        self.enable_count_down = False

        self.root.title("Python GUI")
        self.root.geometry("340x215")

        self.time_text = tk.StringVar()
        self.time_label = tk.Label(self.root, textvariable=self.time_text, font=tk_font.Font(size=size1))
        self.time_label.place(x=x1, y=y1)

        button_up_1_hour = tk.Button(text="時", command=self.plus_1_hour, font=tk.font.Font(size=14), bg=bg1)
        button_up_1_hour.place(x=x1, y=y2, width=w1, height=h1)

        button_up_1_min = tk.Button(text="分", command=self.plus_1_min, font=tk.font.Font(size=14), bg=bg1)
        button_up_1_min.place(x=x2, y=y2, width=w1, height=h1)

        button_up_1_sec = tk.Button(text="秒", command=self.plus_1_sec, font=tk.font.Font(size=14), bg=bg1)
        button_up_1_sec.place(x=x3, y=y2, width=w1, height=h1)

        button_start = tk.Button(text="START/STOP", command=self.start_stop, font=tk.font.Font(size=14), bg=bg2)
        button_start.place(x=x1, y=y3, width=w2, height=h2)

        button_reset = tk.Button(text="RESET", command=self.reset, font=tk.font.Font(size=8), bg=bg0)
        button_reset.place(x=x0, y=y0, width=w0)

        button_again = tk.Button(text="AGAIN", command=self.again, font=tk.font.Font(size=8), bg=bg02)
        button_again.place(x=x0, y=y02, width=w0)

        thread = threading.Thread(target=self.count_down)
        thread.start()

        self.update()
        self.root.mainloop()

    def plus_1_hour(self):
        self.time_value += 60 * 60
        self.update()

    def plus_1_min(self):
        self.time_value += 60
        self.update()

    def plus_1_sec(self):
        self.time_value += 1
        self.update()

    def reset(self):
        self.time_value = 0
        self.enable_count_down = False
        self.update()

    def again(self):
        self.time_value = self.starting_time_value
        self.enable_count_down = False
        self.update()

    def sound(self):
        mixer.init()
        mixer.music.load(self.sound_path)
        mixer.music.play(1)

    def count_down(self):
        while True:
            if self.time_value > 0 and self.enable_count_down:
                self.time_value -= 1
                self.update()
            if self.time_value <= 0 and self.enable_count_down:
                self.time_value = 0
                self.enable_count_down = False
                self.update()
                self.sound()
            time.sleep(1)

    def start_stop(self):
        self.starting_time_value = self.time_value
        self.enable_count_down = not self.enable_count_down

    @staticmethod
    def sec_to_hms(sec):
        minutes, sec = divmod(sec, 60)
        hour, minutes = divmod(minutes, 60)
        return '{}:{:0>2}:{:0>2}'.format(hour, minutes, sec)

    def update(self):
        hms = self.sec_to_hms(self.time_value)
        self.time_text.set(hms)
        self.save_pickle(self.time_value, self.prev_path)

    @staticmethod
    def save_pickle(model, model_path, protocol=4):
        with open(model_path, mode='wb') as f:
            if protocol is None:
                pickle.dump(model, f)
            else:
                pickle.dump(model, f, protocol=protocol)

    @staticmethod
    def load_pickle(path):
        if os.path.exists(path):
            try:
                with open(path, mode='rb') as f:
                    obj = pickle.load(f)
                return obj
            except EOFError as e:
                print('load_pickle():', e)
                return None
        else:
            print('NOT FOUND load_pickle():', path)
            return None


if __name__ == '__main__':
    StopWatch()

