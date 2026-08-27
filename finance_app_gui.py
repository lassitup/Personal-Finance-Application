import tkinter as tk
import data_manage as dm
import Database.database_manage as dbm

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Application")

        self.header_lbl = tk.Label(self.root, text="Personal Finance App", width=100, height=2)
        self.header_lbl.pack()

        # Establish 'main' frame within the window that will house all of the other screen frames
        self.parent_frame = tk.Frame(self.root, borderwidth=5)
        self.parent_frame.pack(fill=tk.BOTH,expand=True)

        self.parent_frame.columnconfigure(0, weight=1)
        self.parent_frame.rowconfigure(0, weight=1)

        # I'm creating a sub frame to house each type of screen the app will have - this will allow me to 
        # cycle through different screens as directed by the user
        # I'm passing 'self' in here so that we can access the methods defined within the main App
        self.welcome_screen = Welcome(self.parent_frame, self)

        self.transaction_screen = Transactions(self.parent_frame, self)

        # All of the various screens need to be assigned to the same area of the screen so I can 
        # cycle through the screens and all will occupy the same area of the screen
        self.welcome_screen.grid(row=0, column=0, sticky="nsew")
        self.transaction_screen.grid(row=0, column=0, sticky="nsew")

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.welcome_screen.tkraise()

    def show_transaction_screen(self):
        self.transaction_screen.tkraise()




class Welcome(tk.Frame):
    # The parent needs to be passed in so that the new screen object is affiliated with the parent frame
    def __init__(self, parent, main_app):
        super().__init__(parent)

        self.main_app = main_app

        self.welcome_lbl = tk.Label(self, text="Welcome to Personal Finance", width=100, height=20, bg="blue")
        self.welcome_lbl.pack()

        self.transaction_btn = tk.Button(self, text="see transactions", bg="orange", command=self.main_app.show_transaction_screen)
        self.transaction_btn.pack()


class Transactions(tk.Frame):
    # Parent Frame gets passed in
    def __init__(self, parent, main_app):
        super().__init__(parent)

        self.main_app = main_app

        # This section of code creates a canvas widget and a scrollbar that will allow the user to scroll through the transactions listing if it exceeds the size of the window
        self.canvas = tk.Canvas(self)

        # Instantiate the scrollbar objects for each direction
        self.scrollbary = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollbarx = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.content_frame = tk.Frame(self.canvas)

        self.content_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.content_window = self.canvas.create_window((0, 0), window=self.content_frame,anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbary.set)
        self.canvas.configure(xscrollcommand=self.scrollbarx.set)

        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfigure(self.content_window, width=event.width))

        self.canvas.grid(row=0, column=0, sticky="nsew")

        current_cols, current_rows = self.grid_size()

        self.scrollbary.grid(row=0, column=1, sticky="ns")
        self.scrollbarx.grid(row=current_rows, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)



        transaction_lbl = tk.Label(self.content_frame, text="Transactions", width=100, height=5)
        transaction_lbl.grid(row=0, column=0)

        self.menu_btn = tk.Button(self.content_frame, text="Main Menu", bg="orange", command=self.main_app.show_welcome_screen)
        self.menu_btn.grid(row=1, column=0)

        self.transaction_btn = tk.Button(self.content_frame, text="Query Transactions", bg="orange", command=self.query_transactions)
        self.transaction_btn.grid(row=2, column=0)

      
    def query_transactions(self):
        transactions = dbm.get_transactions() 






        # Display the Transactions
        for row_i in range(3, 3+len(transactions)):
            # self.rowconfigure(row_i, weight=1)
            for column_i in range(7):
                # self.columnconfigure(column_i, weight=1)

                frame = tk.Frame(self.content_frame)
                frame.grid(row=row_i, column=column_i)
                label = tk.Label(frame, text=f"Row {row_i}, Column {column_i}")
                label.grid(row=0, column=0)

