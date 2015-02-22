#!/usr/bin/env python

from Tkinter import *
import tkMessageBox

from Adafruit_Thermal import *

import serial, sys

import datetime

class ThermalPrinterApp:

  def __init__(self, parent):
    """
    Initialization of instance
    """
    #constants for buttons
    button_width = 6
    button_padx = "2m"
    button_pady = "1m"
    buttons_frame_padx = "3m"
    buttons_frame_pady = "2m"
    buttons_frame_ipadx = "3m"
    buttons_frame_ipady = "1m"
    #end of buttons constant

    #Layout Managment Start
    self.myParent = parent
    self.myParent.title("ESN Receipt Printer")
    self.myParent.report_callback_exception = self.show_error
    self.myParent.geometry("320x200")

    self.myContainer1 = Frame(parent)
    self.myContainer1.pack(expand=YES, fill=BOTH) 
    #self.myContainer1.pack()

    self.buttons_frame = Frame(self.myContainer1,
                               borderwidth=5,
                               relief=RIDGE,
                               background="white")
    self.buttons_frame.pack(
        side=TOP,
        fill=X,
        expand=NO,
        )

    self.bottom_frame = Frame(self.myContainer1,
                              borderwidth=5,
                              relief=RIDGE,
                              background="snow4")
    self.bottom_frame.pack(
        side=TOP,
        fill=BOTH,
        expand=YES) 
    
    self.print_button = Button(self.buttons_frame,
                          command =self.print_receipt_click)
    self.print_button.configure(text="Print", background="forest green")
    self.print_button.focus_force()
    self.print_button.configure(
        padx=button_padx,
        pady=button_pady)
    self.print_button.pack(side=LEFT,fill=X,expand=YES)    
    

    self.quit_button = Button(self.buttons_frame, command=self.cancel_button_click)
    self.quit_button.configure(text="Quit", background="orange red")  
    self.quit_button.configure( 
        padx=button_padx, 
        pady=button_pady)
    self.quit_button.pack(side=RIGHT,fill=X,expand=YES) 

    self.name_row_frame = Frame(self.bottom_frame)
    self.name_label = Label(self.name_row_frame, 
                            text="Receiver Name", 
                            width=15,
                            anchor = 'w',
                            bg="light steel blue") 
    self.name_entry = Entry(self.name_row_frame)

    self.name_row_frame.pack(side=TOP, padx=5, pady=5, fill=X)
    self.name_label.pack(side=LEFT)
    self.name_entry.pack(side=RIGHT,
                         expand=YES,
                         fill=X)

    self.transaction_row_frame = Frame(self.bottom_frame)
    self.transaction_label = Label(self.transaction_row_frame, 
                                   text="Event Name", 
                                   width = 15,
                                   anchor = 'w',
                                   bg="light steel blue") 
    self.transaction_entry = Entry(self.transaction_row_frame)

    self.transaction_row_frame.pack(side=TOP, padx=5, pady=5, fill=X)
    self.transaction_label.pack(side=LEFT)
    self.transaction_entry.pack(side=RIGHT,
                                expand=YES,
                                fill=X)

    self.amount_row_frame = Frame(self.bottom_frame)
    self.amount_label = Label(self.amount_row_frame, 
                                   text="Amount", 
                                   width = 15,
                                   anchor = 'w',
                                   bg="chartreuse") 
    self.amount_entry = Entry(self.amount_row_frame)

    self.amount_row_frame.pack(side=TOP, padx=5, pady=5, fill=X)
    self.amount_label.pack(side=LEFT)
    self.amount_entry.pack(side=RIGHT,
                                expand=YES,
                                fill=X)
    #Layout Managment End

    self.entries = {} #Dictionary for Storing Entries in the Widgets
    try:
      self.printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
    except serial.SerialException,e:
      self.show_error(e)

  def fetch_entries(self):
    self.entries['receiver'] = self.name_entry.get()
    self.entries['trans_name'] = self.transaction_entry.get()
    self.entries['amount'] = self.amount_entry.get()
    print self.entries

  def print_ESN_constants(self):
    self.printer.feed(1)
    self.printer.justify('C')
    self.printer.boldOn()
    self.printer.println("ESN OULU ry")
    self.printer.boldOff()
    self.printer.println("http://web.esnoulu.org")
    self.printer.println("Reg No(Y-tunnus): 2660271-2")
    now = datetime.datetime.now()
    self.printer.println(now.ctime())
    self.printer.feed(1)

  def print_receipt_click(self):
    self.fetch_entries()
    if tkMessageBox.askyesno("Print", "Print Receipt?"):
      print "printing "
      self.print_ESN_constants()
      self.printer.justify('L')

      dotNo = self.printer.maxColumn - len('Name -') - len(self.entries['receiver'])
      self.printer.println("Name -" + "."*dotNo + self.entries['receiver'])

      dotNo = self.printer.maxColumn - len('Event -') - len(self.entries['trans_name'])
      self.printer.println("Event -" + "."*dotNo + self.entries['trans_name'])

      dotNo = self.printer.maxColumn - len('Amount -') - len(self.entries['amount']) - len("Eur ")
      self.printer.println("Amount -" + "."*dotNo + "Eur " + self.entries['amount'])

      self.printer.println("-"*30)
      self.printer.println("Thank You")
      self.printer.feed(2)


  def cancel_button_click(self):
    if tkMessageBox.askyesno("Quit Program", "Quit?"):
      self.myParent.destroy()

  def show_error(self, *args):
    #err = traceback.format_exception(*args)
    tkMessageBox.showerror('Error', "Printer Not Found")
    sys.exit(0)
   


root = Tk()
esn_printer = ThermalPrinterApp(root)
root.mainloop()
