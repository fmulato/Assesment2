import tkinter as tk

def say_hello():
    name = name_input.get()
    greeting_label.config(text=f"Hi, {name}!")

root = tk.Tk()
root.title("Window in Tkinter")
root.geometry("300x150")

name_input = tk.Entry(root)
name_input.pack(pady=10)

greet_button = tk.Button(root, text="Say Hello", command=say_hello)
greet_button.pack()

greeting_label = tk.Label(root, text="")
greeting_label.pack(pady=10)

root.mainloop()