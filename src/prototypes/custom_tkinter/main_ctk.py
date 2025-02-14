import gui_ctk

def app():
    root = gui_ctk.ctk.CTk()
    gui_ctk.Gui(root)
    root.mainloop()

if __name__ == "__main__":
    app()
