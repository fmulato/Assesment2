import gui_ctk as gui

def app():
    root = gui.ctk.CTk()
    gui.Gui(root)
    root.mainloop()

if __name__ == "__main__":
    app()