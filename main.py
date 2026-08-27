from finance_app_gui import App
import tkinter as tk


def main():
    # Create the GUI's main window object here
    root = tk.Tk()
    # Instantiates an App object - pass the main window as the parent
    app = App(root)
    # Begin Tkinter's event loop
    root.mainloop()
    

if __name__ == "__main__":
    main()