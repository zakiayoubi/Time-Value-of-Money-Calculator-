######################################################################
# Author: Zaki Ayoubi
# Purpose: This program is designed to calculate the present value of money, future value of money,
# interest rate, number of periods and payment.
####################################################################################
import tkinter as tk
from tkinter import *
import math
from tkinter import messagebox

class TVM_calculator:

    def __init__(self):
        # Create the main window for the TVM calculator
        self.window = tk.Tk()
        self.window.title("Time Value of Money Calculator")
        self.window.geometry("320x380")

        self.input_frame = LabelFrame(self.window, borderwidth=3)
        # Create radio buttons for the input type
        VALUES = [
            ("Present value ", 1),
            ("future value ", 2),
            ("interest rate", 3),
            ("payment", 4),
            ("period", 5)]
        self.tvm = IntVar()
        self.tvm.set(1)

        for i, (text, mode) in enumerate(VALUES):
            Radiobutton(self.input_frame, text=text, variable=self.tvm, value=mode, padx=20,
                        pady=2).grid(row=i, column=0, sticky=W)
        self.input_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W + E)

        self.entry_frame = LabelFrame(self.window, borderwidth=3)
        # Creating the entry fields for the input

        self.pv_label = tk.Label(self.entry_frame, text="Present value")
        self.pv_label.grid(row=5, column=0, padx=3)
        self.pv_entry = tk.Entry(self.entry_frame, width=25, borderwidth=3)
        self.pv_entry.grid(row=5, column=1, columnspan=2)

        # creating the entry for future value

        self.fv_label = tk.Label(self.entry_frame, text="Future value")
        self.fv_label.grid(row=6, column=0, padx=3)
        self.fv_entry = tk.Entry(self.entry_frame, width=25, borderwidth=3)
        self.fv_entry.grid(row=6, column=1, columnspan=2)

        # creating the entry for interest rate

        self.r_label = tk.Label(self.entry_frame, text="Interest rate (%)")
        self.r_label.grid(row=7, column=0, padx=3)
        self.r_entry = tk.Entry(self.entry_frame, width=25, borderwidth=3)
        self.r_entry.grid(row=7, column=1, columnspan=2)

        # creating the entry for repeating payment

        self.pmt_label = tk.Label(self.entry_frame, text="Repeating Payment")
        self.pmt_label.grid(row=8, column=0, padx=3)
        self.pmt_entry = tk.Entry(self.entry_frame, width=25, borderwidth=3)
        self.pmt_entry.grid(row=8, column=1, columnspan=2)

        # creating the entry for period

        self.n_label = tk.Label(self.entry_frame, text="Period")
        self.n_label.grid(row=9, column=0, padx=3)
        self.n_entry = tk.Entry(self.entry_frame, width=25, borderwidth=3)
        self.n_entry.grid(row=9, column=1, columnspan=2)
        self.entry_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=W + E)

        # create the Calculate button

        self.cal_button_frame = LabelFrame(self.window, borderwidth=3)
        self.button_cal = tk.Button(self.cal_button_frame, text="                                     Calculate                                   ", command=self.calculate)
        self.button_cal.grid(row=2, column=0, columnspan=2)
        self.cal_button_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=W + E)

    def cal_present_value(self):
        """
        Calculate the present value of an investment using the provided inputs
        """
        self.future_value = float(self.fv_entry.get())
        self.interest = float(self.r_entry.get())
        self.payment = float(self.pmt_entry.get())
        self.period = float(self.n_entry.get())

        if self.future_value < 0 or self.interest < 0 or self.payment < 0 or self.period < 0:
            messagebox.showerror("Error", "Amounts cannot be negative")
            return

        self.pv = self.future_value * ((1 + self.interest/100) ** -self.period) + self.payment * (1 - (1 + self.interest / 100) ** -self.period) / (self.interest/100)
        return round(self.pv, 2)

    def cal_future_value(self):
        """
        Calculate the future value of an investment using the provided inputs
        """
        self.present_value = float(self.pv_entry.get())
        self.interest = float(self.r_entry.get())
        self.payment = float(self.pmt_entry.get())
        self.period = float(self.n_entry.get())
        if self.present_value < 0 or self.interest < 0 or self.payment < 0 or self.period < 0:
            messagebox.showerror("Error", "Amounts cannot be negative")
            return

        self.fv = self.present_value * ((1 + self.interest/100) ** self.period) + self.payment * ((1 + self.interest/100) ** self.period -1)/(self.interest/100)
        return self.fv

    def cal_interest_rate(self):
        """
        Calculate the interest rate of an investment using the provided inputs
        """
        # Retrieve input values
        self.present_value = float(self.pv_entry.get())
        self.future_value = float(self.fv_entry.get())
        self.payment = float(self.pmt_entry.get())
        self.period = float(self.n_entry.get())

        # Check input values for errors
        if self.future_value < self.present_value or self.payment > self.future_value or self.period == 0:
            messagebox.showerror("Error", "Invalid input values")
            return

        # Set a reasonable initial guess
        if self.payment == 0:
            self.guess = (self.future_value / self.present_value) ** (1 / self.period) - 1
        else:
            self.guess = 0.05  # set initial guess to a reasonable value
            while abs((self.present_value * (
                    (1 + self.guess) ** self.period - 1) / self.guess) - self.payment) > 0.01 * self.payment:
                self.guess -= 0.001
                break
        # Set a tolerance value for convergence
        self.tolerance = 0.0001

        # Use the Newton-Raphson method to iteratively update the guess value
        while True:
            # Calculate the future value and difference from the provided future value
            self.fv = self.present_value * ((1 + self.guess) ** self.period) + self.payment * (
                    (1 + self.guess) ** self.period - 1) / self.guess
            self.diff = self.fv - self.future_value

            # Check for convergence
            if abs(self.diff) < self.tolerance:
                break

            # Calculate the derivative of the future value function
            self.derivative = (
                        self.present_value * self.period * (1 + self.guess) ** (self.period - 1) + self.payment * (
                        (1 + self.guess) ** self.period - self.period * self.guess - 1) / (self.guess ** 2))

            # Update the guess value
            self.guess = self.guess - self.diff / self.derivative

        # Return the calculated interest rate
        return self.guess

    def cal_payment(self):
        """
        Calculate the repeating payment of an investment using the provided inputs
        """
        self.present_value = float(self.pv_entry.get())
        self.future_value = float(self.fv_entry.get())
        self.interest = float(self.r_entry.get())
        self.period = float(self.n_entry.get())
        if self.future_value < 0 or self.present_value < 0 or self.interest < 0 or self.period < 0:
            messagebox.showerror("Error", "Amounts cannot be negative")
            return
        self.payment = (self.future_value - self.present_value * (1 + self.interest/100) ** self.period) / (((1 + self.interest/100) ** self.period - 1) / (self.interest/100))
        return self.payment
    def cal_period(self):
        """
        Calculate the period of an investment using the provided inputs
        """
        self.present_value = float(self.pv_entry.get())
        self.future_value = float(self.fv_entry.get())
        self.interest = float(self.r_entry.get())
        self.payment = float(self.pmt_entry.get())
        if self.future_value < 0 or self.present_value < 0 or self.interest < 0 or self.payment < 0:
            messagebox.showerror("Error", "Amounts cannot be negative")
            return
        if self.payment == 0:
            self.period = math.log(self.future_value / self.present_value) / math.log(1 + self.interest / 100)
        else:
            try:
                self.period = -math.log(1 - (self.present_value * self.interest/100)/self.payment) / math.log(1 + self.interest/100)
            except Exception:
                messagebox.showerror("Error", "This functionanlity is not available right now.")
        return self.period

    def calculate(self):
        """Calculate the result of a TVM calculation based on user input.

        This function reads user input from the entry widgets and determines which TVM formula
        to use based on the value of the tvm radio button. It then calls the appropriate TVM
        function to calculate the result and displays the result in a label widget.

        If the user has not entered all required input, an error message is displayed.

        """
        # Check if an input type has been selected
        if not self.tvm.get():
            messagebox.showerror("Error!", "Please select an input type.")
            return
        # Check if all fields are filled in
        if not all(
                (self.pv_entry.get(), self.fv_entry.get(), self.r_entry.get(), self.n_entry.get(),
                 self.pmt_entry.get())):
            messagebox.showerror("Error!", "Please fill in all the fields.")
            return
        # check if all entries are numbers and not strings
        if not all(map(lambda entry: entry.get().isdigit() or entry.get().replace('.', '', 1).isdigit(),
                       [self.pv_entry, self.fv_entry, self.r_entry, self.pmt_entry, self.n_entry])):
            messagebox.showerror("Error", "Please enter numbers only.")
            return

        # Determine the input type and calculate the result
        self.value = self.tvm.get()
        if self.value == 1:
            self.result = round(self.cal_present_value(), 2)
            self.pv_entry.delete(0, END)
            self.fv_entry.delete(0, END)
            self.r_entry.delete(0, END)
            self.n_entry.delete(0, END)
            self.pmt_entry.delete(0, END)

        if self.value == 2:
            self.result = round(self.cal_future_value(), 2)
            self.pv_entry.delete(0, END)
            self.fv_entry.delete(0, END)
            self.r_entry.delete(0, END)
            self.n_entry.delete(0, END)
            self.pmt_entry.delete(0, END)
        if self.value == 3:
            self.result = round(self.cal_interest_rate() * 100, 2)
            self.result = str(self.result) + "%"
            self.pv_entry.delete(0, END)
            self.fv_entry.delete(0, END)
            self.r_entry.delete(0, END)
            self.n_entry.delete(0, END)
            self.pmt_entry.delete(0, END)
        if self.value == 4:
            self.result = round(self.cal_payment(), 2)
            self.pv_entry.delete(0, END)
            self.fv_entry.delete(0, END)
            self.r_entry.delete(0, END)
            self.n_entry.delete(0, END)
            self.pmt_entry.delete(0, END)
        if self.value == 5:
            self.result = round(self.cal_period(), 2)
            self.pv_entry.delete(0, END)
            self.fv_entry.delete(0, END)
            self.r_entry.delete(0, END)
            self.n_entry.delete(0, END)
            self.pmt_entry.delete(0, END)

        # displays the result of the calculation in a inside a frame within a label
        self.cal_result_frame = LabelFrame(self.window, borderwidth=3)
        self.result_label = Label(self.cal_result_frame, text=self.result)
        self.result_label.pack()
        self.cal_result_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=W + E)

tvm_calc = TVM_calculator()
tvm_calc.window.mainloop()
