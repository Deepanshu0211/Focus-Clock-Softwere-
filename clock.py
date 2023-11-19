import tkinter as tk
from tkinter import ttk, simpledialog
from time import strftime
import pygame
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt 



class App:
    def __init__(self, root):
        self.root = root
        self.focus_mode_active = False
        self.focus_mode_sessions = []
        self.session_counter = 1
        self.goal_text = None
       
        self.daily_streak = 0
        self.last_focus_date = None
        self.focus_sessions_data = []

        self.streak_label = ttk.Label(root, font=('calibri', 20), background='black', foreground='white')
        self.streak_label.pack()

        self.show_daily_streak()
     

        self.root.title("Productivity App")
        original_image = Image.open("icon.jpg")
        self.background_image = ImageTk.PhotoImage(original_image)

        image = Image.open("start.png")
        image = image.resize((32, 32))
        icon = ImageTk.PhotoImage(image)

       

        self.canvas = tk.Canvas(self.root, width=1000, height=600, borderwidth=0, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        label = ttk.Label(root, text="Hello, Welcome", font=('Broadway', 45), background='black', foreground='grey')
        label.pack(pady=20)
        label = ttk.Label(root, text="This app will help you stay focused", font=('Calm Waters', 20), background='black', foreground='lightgreen')
        label.pack()

        self.focus_mode_start_time = None
        self.focus_mode_sessions = []

        self.clock_label = ttk.Label(root, font=('Franklin Gothic Book', 40, 'bold'), background='black', foreground='lightblue')
        self.clock_label.pack()

        self.timer_label = ttk.Label(root, font=('calibri', 20, 'bold'), background='black', foreground='white')
        self.timer_label.pack()
        self.timer_entry = ttk.Entry(root, font=('calibri', 15, 'bold'))
        self.timer_entry.insert(0, 'enter the time')
        self.timer_entry.pack()
        self.start_timer_button = ttk.Button(root, text='Start Timer', command=self.start_timer,)
        self.start_timer_button.config(image=icon, compound="left")
        self.start_timer_button.pack()
        self.stop_timer_button = ttk.Button(root, text='Stop Timer', command=self.stop_timer, state=tk.DISABLED)
        self.stop_timer_button.pack()
        self.reset_timer_button = ttk.Button(root, text='Reset Timer', command=self.reset_timer)
        self.reset_timer_button.pack()
        self.timer_seconds = 0
        self.timer_running = False

        self.stopwatch_label = ttk.Label(root, font=('calibri', 20, 'bold'), background='black', foreground='white')
        self.stopwatch_label.pack()
        self.stopwatch_label.place(x=20, y=400)

        self.start_stopwatch_button = ttk.Button(root, text='Start Stopwatch', command=self.start_stopwatch)
        self.start_stopwatch_button.pack()
        self.start_stopwatch_button.place(x=20, y=450)

        self.stop_stopwatch_button = ttk.Button(root, text='Stop Stopwatch', command=self.stop_stopwatch, state=tk.DISABLED)
        self.stop_stopwatch_button.pack()
        self.stop_stopwatch_button.place(x=20, y=480)

        self.reset_stopwatch_button = ttk.Button(root, text='Reset Stopwatch', command=self.reset_stopwatch)
        self.reset_stopwatch_button.pack()
        self.reset_stopwatch_button.place(x=20, y=510)
        self.stopwatch_seconds = 0
        self.stopwatch_running = False

     

        self.todo_button = ttk.Button(root, text="To-Do List", command=self.open_todo_window)
        self.todo_button.pack()
        self.todo_button.pack(side=tk.BOTTOM)
        self.todo_button.place(x=453, y=520)
        self.todo_list = []

        self.goal_button = ttk.Button(root, text="Today's Goal", command=self.open_goal_window)
        self.goal_button.pack()
        self.goal_button.place(x=453, y=550)

        self.focus_history_button = tk.Button(
            root,
            background="lightgreen",
            foreground="red",
            highlightthickness=2,
            highlightbackground="yellow",
            highlightcolor="white",
            activebackground="green",
            activeforeground='pink',
            border=0,
            text="View Focus Mode History",
            command=self.open_focus_mode_history_window
        )
        self.focus_history_button.pack()
        self.focus_history_button.place(x=420, y=570)

        self.focus_mode_button = ttk.Button(root, text='Focus Mode', command=self.toggle_focus_mode)
        self.focus_mode_button.pack(padx=20)
        self.focus_mode_button.pack(side=tk.RIGHT)
    

        self.update_clock()


        
    def open_todo_window(self):
        todo_window = tk.Toplevel()
        todo_window.title("To-Do List")
        entry = ttk.Entry(todo_window, font=('calibri', 12))
        entry.grid(row=0, column=0, padx=10, pady=10)
        add_button = ttk.Button(todo_window, text="Add Task", command=lambda: self.add_todo_item(entry, listbox))
        add_button.grid(row=0, column=1, padx=10, pady=10)
        listbox = tk.Listbox(todo_window, font=('calibri', 12))
        listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        complete_button = ttk.Button(todo_window, text="Complete", command=lambda: self.mark_todo_item(listbox))
        complete_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.update_todo_list(listbox)


    def add_todo_item(self, entry, listbox):
        task = entry.get()
        if task:
            self.todo_list.append({'text': task, 'completed': False})
            self.update_todo_list(listbox)
            entry.delete(0, 'end')
            self.save_todo_list()  # Save the tasks after adding

    def mark_todo_item(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.todo_list[index] = {'text': self.todo_list[index]['text'], 'completed': True}
            self.update_todo_list(listbox)
            self.save_todo_list()  # Save the tasks after marking as completed


    def update_todo_list(self, listbox):
        listbox.delete(0, tk.END)
        for i, todo in enumerate(self.todo_list):
            task_text = f"✓ {todo['text']}" if todo['completed'] else f"○ {todo['text']}"
            listbox.insert(tk.END, task_text)

    def open_goal_window(self):
        
        goal_window = tk.Toplevel()
        goal_window.title("Today's Goal")
        goal_window.geometry("200x200+600+250") 
        goal_window.geometry("400x300")  # Adjust the size as needed

        goal_label = ttk.Label(goal_window, text="Write your thoughts or goals for today:", font=('calibri', 12))
        goal_label.pack()

        self.goal_text = tk.Text(goal_window, font=('calibri', 12))
        self.goal_text.pack(fill='both', expand=True)

        
        
        

    
        

        def save_todo_list(self):
            # You can implement saving tasks to a file or database here if needed
            pass

    def save_goal_button(self):
         # You can save the goal text to a file or process it as needed
        goal_text = self.goal_text.get("1.0", "end-1c")
        with open("goal.txt", "w") as file:
                file.write(goal_text)
        print("Saved goal text:", goal_text)

    def update_clock(self):
        current_time = strftime('%H:%M:%S %p')
        self.clock_label['text'] = current_time
        self.root.after(1000, self.update_clock)

    def start_timer(self):
        self.timer_seconds = int(self.timer_entry.get()) * 60
        self.timer_running = True
        self.start_timer_button['state'] = tk.DISABLED
        self.timer_entry['state'] = tk.DISABLED
        self.stop_timer_button['state'] = tk.NORMAL
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        self.start_timer_button['state'] = tk.NORMAL
        self.timer_entry['state'] = tk.NORMAL
        self.stop_timer_button['state'] = tk.DISABLED

    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_entry.delete(0, tk.END)
        self.start_timer_button['state'] = tk.NORMAL
        self.timer_entry['state'] = tk.NORMAL
        self.stop_timer_button['state'] = tk.DISABLED
        self.timer_label['text'] = "Timer: 00:00"

    def update_timer(self):
        if self.timer_running and self.timer_seconds > 0:
            mins, secs = divmod(self.timer_seconds, 60)
            self.timer_label['text'] = f"Timer: {mins:02d}:{secs:02d}"
            self.timer_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_seconds == 0:
            self.play_sound()
            self.timer_running = False
            self.timer_label['text'] = "Timer: 00:00"
            self.start_timer_button['state'] = tk.NORMAL
            self.timer_entry['state'] = tk.NORMAL
            self.stop_timer_button['state'] = tk.DISABLED


    def play_sound(self):
        pygame.mixer.music.load('alarm.mp3')
        pygame.mixer.music.play()

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.start_stopwatch_button['state'] = tk.DISABLED
            self.stop_stopwatch_button['state'] = tk.NORMAL
            self.update_stopwatch()

    def stop_stopwatch(self):
        self.stopwatch_running = False
        self.start_stopwatch_button['state'] = tk.NORMAL
        self.stop_stopwatch_button['state'] = tk.DISABLED

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_seconds = 0
        self.stop_stopwatch_button['state'] = tk.DISABLED
        self.stopwatch_label['text'] = "Stopwatch: 00:00"

    def update_stopwatch(self):
        if self.stopwatch_running:
            mins, secs = divmod(self.stopwatch_seconds, 60)
            self.stopwatch_label['text'] = f"Stopwatch: {mins:02d}:{secs:02d}"
            self.stopwatch_seconds += 1
            self.root.after(1000, self.update_stopwatch)




    def update_daily_streak(self):
        today = datetime.now().date()
        if self.last_focus_date == today:
            return
        if self.last_focus_date is None:
            self.last_focus_date = today
        else:
            if (today - self.last_focus_date).days == 1:
                self.daily_streak += 1
            elif (today - self.last_focus_date).days > 1:
                self.daily_streak = 1
            self.last_focus_date = today



    def show_daily_streak(self):
        self.streak_label['text'] = f'Daily Streak: {self.daily_streak} days'

    
    def toggle_focus_mode(self):
        if self.focus_mode_active:
            self.focus_mode_active = False
            self.focus_mode_window.destroy()
            self.focus_mode_window = None
            end_time = datetime.now()
            duration = (end_time - self.focus_mode_start_time).total_seconds()
            self.focus_mode_sessions.append((self.focus_mode_start_time.strftime('%H:%M:%S'), end_time.strftime('%H:%M:%S'), duration))
            self.reset_stopwatch()
            self.stop_stopwatch()
            self.todo_button['state'] = tk.NORMAL
            self.session_counter +=1  # Increment session counter
            self.update_daily_streak()
            self.show_daily_streak()
        else:
            self.focus_mode_active = True
            self.focus_mode_start_time = datetime.now()
            self.create_focus_mode_window()
            self.start_stopwatch()
            self.todo_button['state'] = tk.DISABLED
            self.update_daily_streak()
            self.show_daily_streak()
 

    def create_focus_mode_window(self):
        self.focus_mode_window = tk.Toplevel()
        self.focus_mode_window.attributes('-fullscreen', True)
        self.focus_mode_window.title("Focus Mode")
        self.focus_mode_window.configure(bg='black')
        self.focus_mode_label = ttk.Label(self.focus_mode_window, font=('Felix Titling', 65, 'bold'),background='black', foreground='white')
        self.focus_mode_label.pack()
        self.focus_mode_label.place(relx=0.2, rely=0.4, anchor='nw')
        self.update_focus_mode_timer(self.focus_mode_label)
        self.exit_focus_mode_button = ttk.Button(self.focus_mode_window, text='Exit Focus Mode', command=self.exit_focus_mode)
        self.exit_focus_mode_button.pack()
        self.exit_focus_mode_button.place(x=1260,y=730)

    def exit_focus_mode(self):
        end_time = datetime.now()
        duration = (end_time - self.focus_mode_start_time).total_seconds()
        self.focus_mode_sessions.append((self.focus_mode_start_time.strftime('%H:%M:%S'), end_time.strftime('%H:%M:%S'), duration))
        self.focus_mode_active = False
        self.focus_mode_window.destroy()
        self.focus_mode_window = None
        self.reset_stopwatch()
        self.stop_stopwatch()
        self.todo_button['state'] = tk.NORMAL

    def update_focus_mode_timer(self, label):
        if self.focus_mode_start_time:
            elapsed_time = datetime.now() - self.focus_mode_start_time
            mins, secs = divmod(int(elapsed_time.total_seconds()), 60)
            label['text'] = f"Focus Mode: {mins:02d}:{secs:02d}"
            label.after(1000, self.update_focus_mode_timer, label)

  
    def open_focus_mode_history_window(self):
        history_window = tk.Toplevel()
        history_window.title("Focus Mode History")

        history_label = ttk.Label(history_window, text='Focus Mode History', font=('calibri', 20, 'bold'))
        history_label.pack()

        history_text = tk.Text(history_window, height=10, width=40, font=('calibri', 12))
        history_text.pack()
        history_text.config(state="normal")
        session_data = self.focus_mode_sessions

        for session in self.focus_mode_sessions:
            start_time, end_time, duration = session
            rounded_duration = int(duration)
            history_text.insert(tk.END, f"Sessions:\nStart: {start_time},\nEnd: {end_time},\nDuration: {rounded_duration} seconds\n, –––––––––––––––\n")

        history_text.config(state="disabled")

        if session_data:
            start_times = [session[0] for session in session_data]
            durations = [session[2] for session in session_data]

          
            plt.bar(start_times, durations, color='green')
            plt.xlabel('Start Time')
            plt.ylabel('Duration (seconds)')
           
            plt.xticks(rotation=0)
            plt.style.use(['dark_background'])
            plt.title('Focus Mode Sessions - Daily Overview')
            plt.ioff

            
            plt.show()

        
    

        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600+200+50")
    root.resizable(True, True)
    root.iconbitmap("yo.ico")
    root.configure(bg="black")
    
   

    app = App(root)
    root.mainloop()
