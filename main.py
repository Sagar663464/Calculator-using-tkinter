import tkinter as tk

# Defining few variables for font style and background colour
label_frame_bg = '#ffffff'
label_bg = '#dbe5ee'
small_font_style = ('Digital-7 Monoitalic', 30)
large_font_style = ('Digital-7 Monoitalic', 60)


# Creating a class

class Calculator:

    # Initiation

    def __init__(self):

        # For the root window
        self.root = tk.Tk()
        self.root.geometry('300x600')
        self.root.resizable(0, 0)
        self.root.title('Calculator')

        # Calling two frames
        self.label_frame = self.create_label_frame()
        self.button_frame = self.create_button_frame()

        # Creating two empty expressions which will be placed in the labels
        self.current_expression = ''
        self.total_expression = ''

        # Stretching all the rows of buttons to the both ends
        for i in range(0, 4):
            self.button_frame.rowconfigure(i,  weight=1)
            self.button_frame.columnconfigure(i, weight=1)

        # Calling two labels which will be in the label frame
        self.display_label = self.view_label()
        self.small_display_label = self.view_label_small()

        # Labelling and positioning digits from a dict
        self.digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2),
            0: (4, 1), '.': (4, 0)

        }
        self.create_digits()

        # Providing the labels and the symbols for the operators with a dict
        self.operators = {'/': "\u00f7", '*': '*', '+': '+', '-': '-'}  # \u00f7 is the unicode for division symbol.
        self.create_operators()

        # Calling to bind keyboard keys to work with the interface
        self.bind_keys()

        # Calling to create special symbols like equal, clear, sqrt and square
        self.create_special_symbols()

    # Creating two frames

    def create_label_frame(self):

        frame = tk.Frame(self.root, background=label_frame_bg, height=221)
        frame.pack(expand=True, fill='both')
        return frame

    def create_button_frame(self):

        frame = tk.Frame(self.root, highlightbackground='#333333', relief='ridge')
        frame.pack(expand=True, fill='both')
        return frame

    # Creating main view label through which we can view the current expression

    def view_label(self):
        # Label for the large display

        display_label = tk.Label(self.label_frame, text=self.current_expression,
                                 padx=24, anchor=tk.E, background=label_bg, font=large_font_style)
        display_label.pack(expand=True, fill='both')

        return display_label

    # Creating small view label which consists of the total expression

    def view_label_small(self):

        # Label for the small display on the top

        small_display_label = tk.Label(self.label_frame, text=self.total_expression,
                                 padx=24, anchor=tk.E, background=label_bg, font=small_font_style)
        small_display_label.pack(expand=True, fill='both')

        return small_display_label

    # Binding keyboard keys to the root window

    def bind_keys(self):
        self.root.bind('<Return>', lambda event: self.eval())
        self.root.bind('<Escape>', lambda event: self.clear_function())

        for key in self.digits:
            self.root.bind(str(key), lambda event, digit=key: self.update_expression(digit))

        for key in self.operators:
            self.root.bind(str(key), lambda event, op=key: self.append_operator(op))

    # Clearing the both display labels and expressions

    def clear_function(self):
        self.current_expression = ''
        self.total_expression = ''
        self.display_label.config(text='')
        self.small_display_label.config(text='')
        return

    # Calculating the expressions using eval method
    def eval(self):
        self.total_expression += self.current_expression
        self.update_small_display_labels()
        try:
            self.current_expression = str(round(eval(self.total_expression), 5))

        except ZeroDivisionError as e:
            self.current_expression = "Error"
        except Exception as E:
            self.current_expression = 'Error'

        finally:
            self.update_display_labels()
            self.update_small_display_labels()

    # Square

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression} ** 2"))
        self.update_display_labels()

    # Square Root

    def sqrt(self):
        self.current_expression = str(round(eval(f"{self.current_expression} ** 0.5"), 6))
        self.update_display_labels()

# Creating operators, special symbols and digits

    def create_special_symbols(self):

        # Equal button
        btn_equal = tk.Button(self.button_frame, text='=', font=['Arial', 24, 'bold'], borderwidth=0,  background='#3B8471',
                              foreground='white',
                              command=lambda: self.eval())
        btn_equal.grid(row=4, column=2, columnspan=3, sticky=tk.NSEW)

        # Clear button
        btn_clear = tk.Button(self.button_frame, text='AC', font=['Arial', 24, 'bold'], borderwidth=0, foreground='#FC1501',
                              command=lambda: self.clear_function())
        btn_clear.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW)

        # Square button
        btn_square = tk.Button(self.button_frame, text='x\u00b2', font=['Arial', 24, 'bold'], borderwidth=0,
                               foreground='#3B8471',
                               command=lambda: self.square())
        btn_square.grid(row=0, column=1, sticky=tk.NSEW)

        # Square root button
        btn_sqrt = tk.Button(self.button_frame, text='\u221ax', font=['Arial', 24, 'bold'], borderwidth=0,
                             foreground='#3B8471',
                             command=lambda: self.sqrt())
        btn_sqrt.grid(row=0, column=2, sticky=tk.NSEW)

        return btn_clear, btn_equal, btn_square

    # Creating operators using dictionaries at the init section

    def create_operators(self):

        i = 0
        for operator, symbol in self.operators.items():
            operator_btn = tk.Button(self.button_frame, text=symbol, borderwidth=0, font=['Arial', 24, 'bold'],
                                     foreground='#3B8471',
                                     command=lambda x=operator: self.append_operator(x))
            operator_btn.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1
        return

    # Appending the operator to the expressions

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression

        self.current_expression = ''

        self.update_small_display_labels()
        self.update_display_labels()

    # Function to update the current expression

    def update_expression(self, value):
        self.current_expression = self.current_expression + str(value)
        self.update_display_labels()

    # Creating the digits using loops

    def create_digits(self):
        for digit, grid_value in self.digits.items():
            btn = tk.Button(self.button_frame, text=digit, font=['Arial', 24], borderwidth=0,
                            foreground='#333333',
                            command=lambda x=digit: self.update_expression(x))
            btn.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
        return

    # Updating display labels

    def update_display_labels(self):
        self.display_label.config(text=self.current_expression[:8])

    def update_small_display_labels(self):
        self.small_display_label.config(text=self.total_expression)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    calc = Calculator()
    calc.run()
