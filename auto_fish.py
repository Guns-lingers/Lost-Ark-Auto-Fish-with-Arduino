import tkinter as tk
from tkinter import ttk
from threading import Thread
import queue
import time
import yaml
import serial
import pyautogui
import cv2
import win32com.client
import pygetwindow as gw
from time import gmtime, strftime
import random
import numpy
import serial.tools.list_ports


class FishingBotGUI:
    ENERGY_DECREASE_AMOUNT = 60
    DURABILITY_DECREASE_AMOUNT = 1

    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Bot")
        self.in_main_thread = True

        self.create_UI()

        with open("resources/keybindings.yaml", "r") as yamlfile:
            self.keybindings = yaml.safe_load(yamlfile)

        self.screenWidth, self.screenHeight= pyautogui.size()
        self.flag = "pulled"

        self.template = cv2.imread(f"resources/{self.screenHeight}/template.png", 0)
        self.poplavok = cv2.imread(f"resources/{self.screenHeight}/poplavok.png", 0)

        self.shell = win32com.client.Dispatch("WScript.Shell")

        self.queue = queue.Queue()
        self.worker_thread = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_UI(self):
        # Добавляем метку и выпадающий список для выбора COM-порта
        self.port_label = ttk.Label(root, text="Выберите COM-порт:")
        self.port_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.port_var = tk.StringVar()
        self.port_dropdown = ttk.Combobox(root, textvariable=self.port_var, state="readonly")
        self.port_dropdown.grid(row=0, column=1, padx=10, pady=5)

        self.energy_label = ttk.Label(root, text="Текущее количество энергии:")
        self.energy_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.energy_entry = ttk.Entry(root)
        self.energy_entry.grid(row=1, column=1, padx=10, pady=5)

        self.durability_label = ttk.Label(root, text="Текущая прочность инструмента:")
        self.durability_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.durability_entry = ttk.Entry(root)
        self.durability_entry.grid(row=2, column=1, padx=10, pady=5)

        self.start_button = ttk.Button(root, text="Начать", command=self.start_bot)
        self.start_button.grid(row=3, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(root, text="Остановить", state=tk.DISABLED, command=self.stop_bot)
        self.stop_button.grid(row=3, column=1, padx=10, pady=10)

        self.status_label = ttk.Label(root, text="Статус: Не запущено", font=("Helvetica", 10))
        self.status_label.grid(row=4, column=0, pady=10)

        self.status_square = tk.Label(root, width=2, height=1, bg="red")
        self.status_square.grid(row=4, column=1, padx=5, pady=10)

        self.log_text = tk.Text(root, height=20, width=50, wrap=tk.WORD)
        self.log_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.populate_ports_dropdown()

    def populate_ports_dropdown(self, prev_ports=None):
        # Получаем список доступных COM портов
        ports = [port.device for port in serial.tools.list_ports.comports()]

        # Если предыдущий список портов не передан, используем текущий
        prev_ports = prev_ports or self.port_dropdown['values']

        # Если списки отличаются, производим обновление
        if ports != prev_ports:
            if ports:
                self.port_dropdown['values'] = ports
                self.port_dropdown.current(0)  # Выбираем первый порт по умолчанию

                # Если есть порты, делаем кнопку "Начать" активной
                self.start_button['state'] = tk.NORMAL
            else:
                self.port_dropdown['values'] = ["Не обнаружено"]
                self.port_dropdown.current(0)  # Выбираем "Не обнаружено"

                # Если нет портов, делаем кнопку "Начать" неактивной
                self.start_button['state'] = tk.DISABLED

        # Запускаем повторяющееся событие через 1000 миллисекунд (1 секунда)
        self.root.after(1000, self.populate_ports_dropdown, ports)

    def change_status_square_color(self, color):
        self.status_square.config(bg=color)

    def move_servo(self,angle):
        # Отправляем угол поворота мотора на Arduino
        command = f'servo:{angle}\n'
        self.ser.write(command.encode('utf-8'))
        time.sleep(0.1)  # Даем мотору время на выполнение команды

    def cast_fishing_rod(self):
        time.sleep(random.uniform(0.75, 1.5))
        self.move_servo(30)
        time.sleep(random.uniform(0.3, 0.8))
        self.move_servo(0)
        print(strftime("%H:%M:%S", gmtime()), f"Бросок удочки.")
        log_text = strftime("%H:%M:%S", gmtime()) + f" Бросок удочки.\n"
        self.log_text.insert(tk.END, log_text)
        self.log_text.see(tk.END)
        time.sleep(random.uniform(4.5, 6.5))

    def start_bot(self):
        energy = self.energy_entry.get()
        durability = self.durability_entry.get()

        self.ser = serial.Serial(self.port_dropdown.get(), 9600)

        if energy.isdigit() and durability.isdigit():
            self.log_text.delete(1.0, tk.END)  # Clear previous logs
            self.status_label.config(text="Статус: Запущено")
            self.change_status_square_color("green")

            # Reset state before starting the bot
            self.flag = "pulled"
            self.stop_event = False

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            self.worker_thread = Thread(target=self.run_bot)
            self.worker_thread.start()
        else:
            self.log_text.insert(tk.END, "Ошибка: Введите числовые значения для энергии и прочности.\n")
            self.log_text.see(tk.END)

    def stop_bot(self):
        if self.worker_thread and self.worker_thread.is_alive():
            self.status_label.config(text="Статус: Остановка...")
            self.change_status_square_color("orange")
            self.root.update()
            self.stop_event = True
            if self.in_main_thread:
                self.worker_thread.join()
            else:
                self.worker_thread.join(timeout=0)

            if hasattr(self, 'ser') and self.ser.is_open:
                self.ser.close()

            # Reset state after stopping the bot
            self.status_label.config(text="Статус: Не запущено")
            self.change_status_square_color("red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.log_text.insert(tk.END, "Программа остановлена.\n")
            self.log_text.see(tk.END)

            # Reset state for restartability
            self.flag = "pulled"

    def run_bot(self):
        self.in_main_thread = False
        print(strftime("%H:%M:%S", gmtime()), "Запуск бота через 5 секунд.")
        log_text = strftime("%H:%M:%S", gmtime()) + " Запуск бота через 5 секунд.\n"
        self.log_text.insert(tk.END, log_text)
        self.log_text.see(tk.END)
        time.sleep(5)
        
        while not self.stop_event:  # Проверяем флаг для завершения цикла

            energy = self.energy_entry.get()
            durability = self.durability_entry.get()

            # screenshot creation
            self.image = pyautogui.screenshot(region=(self.screenWidth/2 - 100, self.screenHeight/2 - 150, 200, 200))
            self.image = cv2.cvtColor(numpy.array(self.image), 0)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # search pattern on screen for exclamation point
            self.template_coordinates = cv2.matchTemplate(self.image, self.template, cv2.TM_CCOEFF_NORMED)
            self.loc = numpy.where(self.template_coordinates >= 0.7)

            if len(self.loc[0]) > 0 and self.flag == "thrown":
                time.sleep( random.uniform(0.04, 0.085))

                # keyboard.press(keybindings['fishing'])
                self.move_servo(30)
                time.sleep( random.uniform(0.3, 0.8))
                # keyboard.release(keybindings['fishing'])
                self.move_servo(0)

                # pyautogui.press(keybindings['fishing'])
                
                self.flag = "pulled"
                
                energy = int(energy) - 60
                self.energy_entry.delete(0, tk.END)
                self.energy_entry.insert(0, str(energy))

                durability = int(durability) - 1
                self.durability_entry.delete(0, tk.END)
                self.durability_entry.insert(0, str(durability))

                print(strftime("%H:%M:%S", gmtime()), "Найдена рыба.")
                log_te = strftime("%H:%M:%S", gmtime()) + " Найдена рыба.\n"
                self.log_text.insert(tk.END, log_te)
                self.log_text.see(tk.END)
                time.sleep(random.uniform(5.5, 7.5))

            # search pattern on screen for buoy
            self.poplavok_coordinates = cv2.matchTemplate(self.image, self.poplavok, cv2.TM_CCOEFF_NORMED)
            self.poplavok_loc = numpy.where(self.poplavok_coordinates >= 0.7)
            
            if len(self.poplavok_loc[0]) == 0 and self.flag == "pulled":
                if int(energy) < self.ENERGY_DECREASE_AMOUNT or int(durability) < self.DURABILITY_DECREASE_AMOUNT:
                    self.status_label.config(text="Статус: Остановка...")
                    self.change_status_square_color("orange")
                    self.root.update()
                    self.stop_event = True
                    
                    if hasattr(self, 'ser') and self.ser.is_open:
                        self.ser.close()

                    # Reset state after stopping the bot
                    self.status_label.config(text="Статус: Не запущено")
                    self.change_status_square_color("red")
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.log_text.insert(tk.END, "Программа остановлена.\n")
                    self.log_text.see(tk.END)

                    # Reset state for restartability
                    self.flag = "pulled"
                    break

                self.cast_fishing_rod()
                self.flag = "thrown"

    def on_close(self):
        if self.worker_thread and self.worker_thread.is_alive():
            self.stop_bot()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FishingBotGUI(root)
    root.mainloop()