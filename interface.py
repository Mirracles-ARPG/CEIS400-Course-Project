# import tkinter module 

from tkinter import *
import application
  

# creating main tkinter window/toplevel 

root = Tk() 

root.title('Login')  

top = Toplevel() 

  

# this wil create a label widget 

employeeID = Label(top, text = "Employee ID: ") 

password = Label(top, text = "Password: ") 

   

# grid method to arrange labels in respective 

# put label widget on the screen 

employeeID.grid(row = 1, column = 0, sticky = W, pady = 2) 

password.grid(row = 2, column = 0, sticky = W, pady = 2) 

   

# entry widgets, used to take entry from user 

e1 = Entry(top) 

e2 = Entry(top) 

   

# this will arrange input widgets 

e1.grid(row = 1, column = 1, pady = 2) 

e2.grid(row = 2, column = 1, pady = 2) 

  
  

lBtn = Button(top, text = "LOGIN ", command=open) 

# this will arrange the login button 

lBtn.grid(row = 3, column = 0, padx = 50) 

   

#this will create a login button 

#will take the user to the next page on click 

#open function is allow the next window to open when "login" is clicked 

#lbls of all tools to choose from 

  

#toplevel  

top = Toplevel() 

  

#new window function to be called when button pressed 

def new_window(): 

    window = Toplevel(root) 

    canvas = tk.Canvase(window, height=HEIGHT, width=WIDTH) 

    canvas.pack() 

  

    HEIGHT = 400 

    Widget = 300 

    root = tk.Tk() 

    root.title("Equipment Checkout") 

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH) 

    canvas.pack() 

    button = tk.Button(root, text="Checkout", bg='black', fg='#469A00', 

                       command=lambda: new_window()) 

    button.grid() 



def open(): 

   # top = Toplevel() 

    #top.title('Equipment Inventory') 

    ##creates labels for the tool names 

    #toolHacksaw = Label(top, text = "Hacksaw ") 

    #toolHoleSawKit = Label(top, text = "Hole Saw Kit ") 

    #toolHandAuger = Label(top, text = "Hand Auger ") 

    #toolWeldingClamps = Label(top, text = "Welding Clamps") 

    #toolAngleGrinder = Label(top, text = "Angle Grinder") 

    ##grid method to arrange labels in respective 

    ##put label widget on the screen 

    #toolHacksaw.grid(row = 1, column = 0, sticky = W, pady = 2) 

    #toolHoleSawKit.grid(row = 2, column = 0, sticky = W, pady = 2) 

    #toolHandAuger.grid(row = 3, column = 0, sticky = W, pady = 2) 

    #toolWeldingClamps.grid(row = 4, column = 0, sticky = W, pady = 2) 

    #toolAngleGrinder.grid(row= 5, column = 0, sticky = W, pady = 2) 

  

     #check boxes to select tool to checkout 

    var = IntVar() 

    c=Checkbutton(root, text="HackSaw") 

    c=Checkbutton(root, text="Hole Saw Kit") 

    c=Checkbutton(root, text="Hand Auger") 

    c=Checkbutton(root, text="Welding Clamps") 

    c=Checkbutton(root, text="Angle Grinder") 

  

    lBtn = Button(root, text ="LOGIN", command=open) 



# infinite loop which can be terminated by keyboard 

# or mouse interrupt 

mainloop() 