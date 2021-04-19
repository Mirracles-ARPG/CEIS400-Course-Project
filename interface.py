import tkinter as tk
from tkinter import messagebox, scrolledtext
import application



CURRENTLY_LOGGED_IN = None

root = tk.Tk() #creating main tkinter window
root.title('Equipment Depot Software')
root.geometry('480x360')
root.minsize(480, 360)
tk.Grid.rowconfigure(root, 0, weight = 1)
tk.Grid.columnconfigure(root, 1, weight = 1)

rootMenuFrame = tk.LabelFrame(root, text = "Menu", width = 90)
rootMenuFrame.grid_propagate(0)
tk.Grid.columnconfigure(rootMenuFrame, 0, weight = 1)
rootConsole = scrolledtext.ScrolledText(root)

rootMenuFrame.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "NSW")
rootConsole.grid(row = 0, column = 1, sticky = "NSEW")

def loadDefaultMenu():
    unloadCurrentMenu()
    displayInRootConsole("Sign in to use the Equipment Depot Inventory Management Assistant.\n\nThere will always be a root user with the ID number of 0.\n\nAll passwords default to 'Password' until changed on first login.")

    btnLogin = tk.Button(rootMenuFrame, text = "LOGIN", command = lambda: loginWindow())
    btnLogin.grid(row = 0, column = 0, sticky = "EW")

def loadEmployeeMenu():
    unloadCurrentMenu()
    displayInRootConsole("Currently signed in: " + application.getUserNameplate(CURRENTLY_LOGGED_IN) + "\n\nYour Current Checkouts:\n" + application.getEmployeeCheckouts(CURRENTLY_LOGGED_IN))

    btnCheckout = tk.Button(rootMenuFrame, text = "CHECKOUT", command = lambda: checkoutWindow())
    btnReturn = tk.Button(rootMenuFrame, text = "RETURN", command = lambda: returnWindow())
    btnLogout = tk.Button(rootMenuFrame, text = "LOGOUT", command = lambda: logout())

    btnCheckout.grid(row = 0, column = 0, sticky = "EW")
    btnReturn.grid(row = 1, column = 0, sticky = "EW")
    btnLogout.grid(row = 2, column = 0, sticky = "EW")

def loadManagerMenu():
    global CURRENTLY_LOGGED_IN
    unloadCurrentMenu()
    displayInRootConsole("Currently signed in: " + application.getUserNameplate(CURRENTLY_LOGGED_IN) + "\n\nEnter a submenu to perform an action.")

    btnMngUser = tk.Button(rootMenuFrame, text = "MANAGE\nUSERS", command = lambda: loadUsersSubMenu())
    btnMngEquip = tk.Button(rootMenuFrame, text = "MANAGE\nEQUIPMENT", command = lambda: loadEquipSubMenu())
    btnGenReport = tk.Button(rootMenuFrame, text = "GENERATE\nREPORTS", command = lambda: loadReportsSubMenu())
    btnLogout = tk.Button(rootMenuFrame, text = "LOGOUT", command = lambda: logout())

    btnMngUser.grid(row = 0, column = 0, sticky = "EW")
    btnMngEquip.grid(row = 1, column = 0, sticky = "EW")
    btnGenReport.grid(row = 2, column = 0, sticky = "EW")
    btnLogout.grid(row = 3, column = 0, sticky = "EW")

    #if CURRENTLY_LOGGED_IN == "0":
        #btnReset = tk.Button(rootMenuFrame, text = "RESET", command = lambda: reset())
        #btnReset.grid(row = 4, column = 0, sticky = "EW", pady = 30)
        #def reset():
            #application.db_conn.reset()
            #logout()

def loadUsersSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("All Users:\n" + application.getAllUsers())

    btnAddUser = tk.Button(rootMenuFrame, text = "ADD NEW\nUSER", command = lambda: addUserWindow())
    btnRemoveUser = tk.Button(rootMenuFrame, text = "REMOVE\nA USER", command = lambda: removeUserWindow())
    btnModifyUser = tk.Button(rootMenuFrame, text = "MODIFY\nA USER", command = lambda: modifyUserWindow())
    btnBack = tk.Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

    btnAddUser.grid(row = 0, column = 0, sticky = "EW")
    btnRemoveUser.grid(row = 1, column = 0, sticky = "EW")
    btnModifyUser.grid(row = 2, column = 0, sticky = "EW")
    btnBack.grid(row = 3, column = 0, sticky = "EW")

def loadEquipSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("All Equipment:\n" + application.getAllEquipment())

    btnAddEquip = tk.Button(rootMenuFrame, text = "ADD NEW\nEQUIPMENT", command = lambda: addEquipWindow())
    btnRemoveEquip = tk.Button(rootMenuFrame, text = "REMOVE\nEQUIPMENT", command = lambda: removeEquipWindow())
    btnModifyEquip = tk.Button(rootMenuFrame, text = "MODIFY\nEQUIPMENT", command = lambda: modifyEquipWindow())
    btnBack = tk.Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

    btnAddEquip.grid(row = 0, column = 0, sticky = "EW")
    btnRemoveEquip.grid(row = 1, column = 0, sticky = "EW")
    btnModifyEquip.grid(row = 2, column = 0, sticky = "EW")
    btnBack.grid(row = 3, column = 0, sticky = "EW")

def loadReportsSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("Choose a report type to generate.")

    btnRepCheckouts = tk.Button(rootMenuFrame, text = "VIEW ALL\nCHECKOUTS",
        command = lambda: displayInRootConsole("All Active Checkouts:\n" + application.getAllCheckouts()))
    btnRepReturns = tk.Button(rootMenuFrame, text = "VIEW ALL\nRETURN LOGS",
        command = lambda: displayInRootConsole("Full Return Logs:\n" + application.getAllReturns()))
    btnRepUserAll = tk.Button(rootMenuFrame, text = "VIEW ALL\nFROM A\nSELECT USER", command = lambda: reportSpecificUserWindow())
    btnRepEquipAll = tk.Button(rootMenuFrame, text = "VIEW ALL\nFOR SELECT\nEQUIPMENT", command = lambda: reportSpecificEquipWindow())
    btnBack = tk.Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

    btnRepCheckouts.grid(row = 0, column = 0, sticky = "EW")
    btnRepReturns.grid(row = 1, column = 0, sticky = "EW")
    btnRepUserAll.grid(row = 2, column = 0, sticky = "EW")
    btnRepEquipAll.grid(row = 3, column = 0, sticky = "EW")
    btnBack.grid(row = 4, column = 0, sticky = "EW")

def logout():
    global CURRENTLY_LOGGED_IN
    CURRENTLY_LOGGED_IN = None
    loadDefaultMenu()

def unloadCurrentMenu(): 
    for widget in rootMenuFrame.winfo_children(): widget.destroy()

def displayInRootConsole(text):
    rootConsole.configure(state = 'normal')
    rootConsole.delete(1.0, tk.END)
    rootConsole.insert(index = 1.0, chars = text)
    rootConsole.configure(state = 'disabled')



def loginWindow():
    top = tk.Toplevel()
    top.title('Login')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmLoginContent = tk.Frame(top)
    
    lblID = tk.Label(frmLoginContent, text = "User ID#: ") #this wil create a label widget
    lblPass = tk.Label(frmLoginContent, text = "Password: ")
    entID = tk.Entry(frmLoginContent) #entry widgets, used to take entry from user 
    entID.focus_set()
    entPass = tk.Entry(frmLoginContent, show = "*")
    
    lblID.grid(row = 0, column = 0, sticky = "W", pady = 2) #put label widget on the screen 
    lblPass.grid(row = 1, column = 0, sticky = "W", pady = 2) 
    entID.grid(row = 0, column = 1, pady = 2) #this will arrange input widgets 
    entPass.grid(row = 1, column = 1, pady = 2)
    
    btnLogin = tk.Button(top, text = "LOGIN", command = lambda: login()) #this will create a login button
    top.bind('<Return>', lambda event: login())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    # grid method to arrange labels in respective 
    frmLoginContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnLogin.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5) #this will arrange the login button 
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def login():
        global CURRENTLY_LOGGED_IN
        userID = entID.get()
        authenticated = application.login(userID, entPass.get())
        if authenticated == 0 or authenticated == 1: 
            messagebox.showerror(message = "Incorrect ID/Password Combination!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif authenticated == 2:
            firstLoginWindow(userID)
            top.destroy()
        elif authenticated == 3:
            CURRENTLY_LOGGED_IN = userID
            loadEmployeeMenu()
            top.destroy()
        elif authenticated == 4:
            CURRENTLY_LOGGED_IN = userID
            loadManagerMenu()
            top.destroy()
        elif authenticated == 5:
            messagebox.showerror(message = "Fields can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif authenticated == 6:
            messagebox.showerror(message = "User ID must be a number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def firstLoginWindow(userID):
    top = tk.Toplevel()
    top.title('Change Password')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmFirstLoginContent = tk.Frame(top)

    lblInfo = tk.Label(frmFirstLoginContent, text = "This is your first time logging in.\nYou need to change your password.")
    lblPass = tk.Label(frmFirstLoginContent, text = "New Password: ")
    lblVerify = tk.Label(frmFirstLoginContent, text = "Confirm New Password: ")
    entPass = tk.Entry(frmFirstLoginContent, show = "*")
    entPass.focus_set()
    entVerify = tk.Entry(frmFirstLoginContent, show = "*")
    
    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblPass.grid(row = 1, column = 0, sticky = "W", pady = 2)
    lblVerify.grid(row = 2, column = 0, sticky = "W", pady = 2) 
    entPass.grid(row = 1, column = 1, pady = 2)
    entVerify.grid(row = 2, column = 1, pady = 2)

    btnSubmit = tk.Button(top, text = "SUBMIT", command = lambda: firstLogin())
    top.bind('<Return>', lambda event: firstLogin())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmFirstLoginContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnSubmit.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def firstLogin():
        result = application.firstLoginPasswordChange(userID, entPass.get(), entVerify.get())
        if result == 0:
            messagebox.showinfo(message = "Password changed successfully.\nPlease login with your new password.")
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "Passwords do not match!")
            entPass.focus_set()
            entPass.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "Password is too short!\nYour password must be at least 6 characters")
            entPass.focus_set()
            entPass.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "Unexpected error!")
            entPass.focus_set()
            entPass.selection_adjust(tk.END)



def checkoutWindow():
    top = tk.Toplevel()
    top.title('Checkout')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmCheckoutContent = tk.Frame(top)
    
    lblID = tk.Label(frmCheckoutContent, text = "Enter ID number of\nequipment to check out")
    entID = tk.Entry(frmCheckoutContent)
    entID.focus_set()
    
    lblID.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)
    
    btnCheckout = tk.Button(top, text = "CHECKOUT", command = lambda: checkout())
    top.bind('<Return>', lambda event: checkout())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmCheckoutContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnCheckout.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def checkout():
        result = application.checkout(CURRENTLY_LOGGED_IN, entID.get())
        if result == 0:
            messagebox.showinfo(message = "Equipment checked out successfully.")
            displayInRootConsole("Currently signed in: " + application.getUserNameplate(CURRENTLY_LOGGED_IN) + "\n\nYour Current Checkouts:\n" + application.getEmployeeCheckouts(CURRENTLY_LOGGED_IN))
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "You do not have the skills set for this equipment!\nFor safety reasons you may not check it out.")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "No equipment exists with the given ID number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "Equipment is already checked out by another user!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "You already have this equipment checked out!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 5:
            messagebox.showerror(message = "Fields can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 6:
            messagebox.showerror(message = "Equipment ID must be a number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 7:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def returnWindow():
    top = tk.Toplevel()
    top.title('Return')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmReturnContent = tk.Frame(top)
    
    lblID = tk.Label(frmReturnContent, text = "Enter ID number of\nequipment to return")
    entID = tk.Entry(frmReturnContent)
    entID.focus_set()
    
    lblID.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)
    
    btnReturn = tk.Button(top, text = "RETURN", command = lambda: returns())
    top.bind('<Return>', lambda event: returns())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmReturnContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnReturn.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def returns():
        result = application.returns(CURRENTLY_LOGGED_IN, entID.get())
        if result == 0:
            messagebox.showinfo(message = "Equipment returned successfully.")
            displayInRootConsole("Currently signed in: " + application.getUserNameplate(CURRENTLY_LOGGED_IN) + "\n\nYour Current Checkouts:\n" + application.getEmployeeCheckouts(CURRENTLY_LOGGED_IN))
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "No equipment exists with the given ID number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "No users have this equipment checked out!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "You do not have this equipment checked out!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "Fields can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 5:
            messagebox.showerror(message = "Equipment ID must be a number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 6:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def addUserWindow():
    top = tk.Toplevel()
    top.title('Add New User')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter data for new user.")
    lblID = tk.Label(frmContent, text = "ID Number:")
    lblNameF = tk.Label(frmContent, text = "First Name:")
    lblNameL = tk.Label(frmContent, text = "Last Name:")
    lblSkills = tk.Label(frmContent, text = "Skills:")
    lblPermission = tk.Label(frmContent, text = "Permission:")
    entID = tk.Entry(frmContent)
    entID.focus_set()
    entNameF = tk.Entry(frmContent)
    entNameL = tk.Entry(frmContent)
    entSkills = tk.Entry(frmContent)
    entPermission = tk.Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = "W", pady = 2)
    lblNameF.grid(row = 2, column = 0, sticky = "W", pady = 2)
    lblNameL.grid(row = 3, column = 0, sticky = "W", pady = 2)
    lblSkills.grid(row = 4, column = 0, sticky = "W", pady = 2)
    lblPermission.grid(row = 5, column = 0, sticky = "W", pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entNameF.grid(row = 2, column = 1, pady = 2)
    entNameL.grid(row = 3, column = 1, pady = 2)
    entSkills.grid(row = 4, column = 1, pady = 2)
    entPermission.grid(row = 5, column = 1, pady = 2)

    btnAdd = tk.Button(top, text = "ADD", command = lambda: addUser())
    top.bind('<Return>', lambda event: addUser())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnAdd.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def addUser():
        result = application.addUser(CURRENTLY_LOGGED_IN, entID.get(), entNameF.get(), entNameL.get(), entSkills.get(), entPermission.get())
        if result == 0:
            messagebox.showinfo(message = "User added successfully.")
            displayInRootConsole("All Users:\n" + application.getAllUsers())
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "A user already exists with this ID!\nIDs must be unique for each user.")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "You do not have permission to do this!\nThe permission of users you add must be less than yours.")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "Fields can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "User ID, skills, and permission must be numbers!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 5:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def removeUserWindow():
    top = tk.Toplevel()
    top.title('Remove a User')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter ID of user to remove.")
    entID = tk.Entry(frmContent)
    entID.focus_set()

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = tk.Button(top, text = "REMOVE", command = lambda: removeUser())
    top.bind('<Return>', lambda event: removeUser())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def removeUser():
        result = application.removeUser(CURRENTLY_LOGGED_IN, entID.get())
        if result == 0:
            messagebox.showinfo(message = "User removed successfully.")
            displayInRootConsole("All Users:\n" + application.getAllUsers())
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "No users exist with this ID!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "You do not have permission to do this!\nYou can only remove users with lower permission than you.")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "Fields can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "User ID must be a number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 5:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def modifyUserWindow():
    top = tk.Toplevel()
    top.title('Modify a User')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter ID of user to change.\nEnter any fields you want to\nupdate with the new data.\nLeave fields blank if you\ndo not want them changed.")
    lblID = tk.Label(frmContent, text = "ID Number:")
    lblNameF = tk.Label(frmContent, text = "First Name:")
    lblNameL = tk.Label(frmContent, text = "Last Name:")
    chkVar = tk.IntVar()
    chkPassword = tk.Checkbutton(frmContent, text = "Reset Password", variable = chkVar, onvalue = 1, offvalue = 0)
    lblSkills = tk.Label(frmContent, text = "Skills:")
    lblPermission = tk.Label(frmContent, text = "Permission:")
    entID = tk.Entry(frmContent)
    entID.focus_set()
    entNameF = tk.Entry(frmContent)
    entNameL = tk.Entry(frmContent)
    entSkills = tk.Entry(frmContent)
    entPermission = tk.Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = "W", pady = 2)
    lblNameF.grid(row = 2, column = 0, sticky = "W", pady = 2)
    lblNameL.grid(row = 3, column = 0, sticky = "W", pady = 2)
    chkPassword.grid(row = 4, column = 0, columnspan = 2, pady = 2)
    lblSkills.grid(row = 5, column = 0, sticky = "W", pady = 2)
    lblPermission.grid(row = 6, column = 0, sticky = "W", pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entNameF.grid(row = 2, column = 1, pady = 2)
    entNameL.grid(row = 3, column = 1, pady = 2)
    entSkills.grid(row = 5, column = 1, pady = 2)
    entPermission.grid(row = 6, column = 1, pady = 2)

    btnApply = tk.Button(top, text = "APPLY", command = lambda: modifyUser())
    top.bind('<Return>', lambda event: modifyUser())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnApply.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def modifyUser():
        result = application.updateUser(CURRENTLY_LOGGED_IN, entID.get(), entNameF.get(), entNameL.get(), chkVar.get(), entSkills.get(), entPermission.get())
        if result == 0:
            messagebox.showinfo(message = "User modified successfully.")
            displayInRootConsole("All Users:\n" + application.getAllUsers())
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "No users exist with this ID!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "You do not have permission to do this!\nYou can only modify users with lower permission than you.")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "You do not have permission to do this!\nYou can only modify a users permission to be less than yours.")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "User ID can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 5:
            messagebox.showerror(message = "User ID, skills, and permission must be numbers!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 6:
            messagebox.showerror(message = "You can not modify the root user!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 7:
            messagebox.showerror(message = "You can not modify yourself!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 8:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def addEquipWindow():
    top = tk.Toplevel()
    top.title('Add New Equipment')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter data for new equipment.")
    lblID = tk.Label(frmContent, text = "ID Number:")
    lblDesc = tk.Label(frmContent, text = "Description:")
    lblSkills = tk.Label(frmContent, text = "Skills:")
    entID = tk.Entry(frmContent)
    entID.focus_set()
    entDesc = tk.Entry(frmContent)
    entSkills = tk.Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = "W", pady = 2)
    lblDesc.grid(row = 2, column = 0, sticky = "W", pady = 2)
    lblSkills.grid(row = 3, column = 0, sticky = "W", pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entDesc.grid(row = 2, column = 1, pady = 2)
    entSkills.grid(row = 3, column = 1, pady = 2)

    btnAdd = tk.Button(top, text = "ADD", command = lambda: addEquip())
    top.bind('<Return>', lambda event: addEquip())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnAdd.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def addEquip():
        result = application.addEquipment(entID.get(), entDesc.get(), entSkills.get())
        if result == 0:
            messagebox.showinfo(message = "Equipment added successfully.")
            displayInRootConsole("All Equipment:\n" + application.getAllEquipment())
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "Equipment already exists with this ID!\nIDs must be unique for all equipment.")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "Fields can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "Equipment ID and skills must be numbers!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def removeEquipWindow():
    top = tk.Toplevel()
    top.title('Remove Equipment')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter ID of equipment to remove.")
    entID = tk.Entry(frmContent)
    entID.focus_set()

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = tk.Button(top, text = "REMOVE", command = lambda: removeEquip())
    top.bind('<Return>', lambda event: removeEquip())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def removeEquip():
        result = application.removeEquipment(entID.get())
        if result == 0:
            messagebox.showinfo(message = "Equipment removed successfully.")
            displayInRootConsole("All Equipment:\n" + application.getAllEquipment())
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "No equipment exists with this ID!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "Fields can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "Equipment ID must be a number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def modifyEquipWindow():
    top = tk.Toplevel()
    top.title('Modify Equipment')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter ID of equipment to change.\nEnter any fields you want to\nupdate with the new data.\nLeave fields blank if you\ndo not want them changed.")
    lblID = tk.Label(frmContent, text = "ID Number:")
    lblDesc = tk.Label(frmContent, text = "Description:")
    lblSkills = tk.Label(frmContent, text = "Skills:")
    entID = tk.Entry(frmContent)
    entID.focus_set()
    entDesc = tk.Entry(frmContent)
    entSkills = tk.Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = "W", pady = 2)
    lblDesc.grid(row = 2, column = 0, sticky = "W", pady = 2)
    lblSkills.grid(row = 3, column = 0, sticky = "W", pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entDesc.grid(row = 2, column = 1, pady = 2)
    entSkills.grid(row = 3, column = 1, pady = 2)

    btnApply = tk.Button(top, text = "APPLY", command = lambda: modifyEquip())
    top.bind('<Return>', lambda event: modifyEquip())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnApply.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def modifyEquip():
        result = application.updateEquipment(entID.get(), entDesc.get(), entSkills.get())
        if result == 0:
            messagebox.showinfo(message = "Equipment modified successfully.")
            displayInRootConsole("All Equipment:\n" + application.getAllEquipment())
            top.destroy()
        elif result == 1:
            messagebox.showerror(message = "No equipment exists with this ID!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 2:
            messagebox.showerror(message = "Equipment ID can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 3:
            messagebox.showerror(message = "Equipment ID and skills must be numbers!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == 4:
            messagebox.showerror(message = "Unexpected error!")
            entID.focus_set()
            entID.selection_adjust(tk.END)



def reportSpecificUserWindow():
    top = tk.Toplevel()
    top.title('Generate User Report')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter ID of user to generate a report of.")
    entID = tk.Entry(frmContent)
    entID.focus_set()

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = tk.Button(top, text = "SUBMIT", command = lambda: generateReport())
    top.bind('<Return>', lambda event: generateReport())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def generateReport():
        userID = entID.get()
        result = application.getEmployeeAll(userID)
        if result == "x":
            messagebox.showerror(message = "No user exists with this ID!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == "y":
            messagebox.showerror(message = "User ID can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == "z":
            messagebox.showerror(message = "User ID must be a number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        else:
            displayInRootConsole("All Activity From User " + application.getUserNameplate(userID) + ":\n" + result)
            top.destroy()



def reportSpecificEquipWindow():
    top = tk.Toplevel()
    top.title('Generate Equipment Report')
    top.geometry("+%d+%d" % (root.winfo_x() + 90, root.winfo_y() + 50))
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)
    top.grab_set()

    frmContent = tk.Frame(top)

    lblInfo = tk.Label(frmContent, text = "Enter ID of equipment to generate a report of.")
    entID = tk.Entry(frmContent)
    entID.focus_set()

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = tk.Button(top, text = "SUBMIT", command = lambda: generateReport())
    top.bind('<Return>', lambda event: generateReport())
    btnCancel = tk.Button(top, text = "CANCEL", command = top.destroy)
    btnCancel.bind('<Return>', lambda event: top.destroy())

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = "E", padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = "W", padx = 5, pady = 5)

    def generateReport():
        equipID = entID.get()
        result = application.getEquipmentAll(equipID)
        if result == "x":
            messagebox.showerror(message = "No equipment exists with this ID!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == "y":
            messagebox.showerror(message = "Equipment ID can not be blank!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        elif result == "z":
            messagebox.showerror(message = "Equipment ID must be a number!")
            entID.focus_set()
            entID.selection_adjust(tk.END)
        else:
            displayInRootConsole("All Activity For Equipment " + application.getEquipNameplate(equipID) + ":\n" + result)
            top.destroy()



if __name__ == "__main__":
    application.db_conn.initialize()
    loadDefaultMenu()
    root.mainloop() #infinite loop which can be terminated by keyboard or mouse interrupt 