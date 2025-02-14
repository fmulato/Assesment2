import customtkinter as ctk

def say_hello():
    name = name_input.get()
    greeting_label.configure(text=f"Hi, {name}!")

root = ctk.CTk()
root.title("Window in CustomTkinter")
root.geometry("800x600")

name_input = ctk.CTkEntry(root)
name_input.pack(pady=10)

greet_button = ctk.CTkButton(root, text="Say Hello", command=say_hello)
greet_button.pack()

greeting_label = ctk.CTkLabel(root, text="")
greeting_label.pack(pady=10)

root.mainloop()
