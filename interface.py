from tkinter import *
from tkinter import messagebox, scrolledtext
import application

CURRENTLY_LOGGED_IN = None

root = Tk() #creating main tkinter window
root.title('Equipment Depot Software')
root.geometry('480x360')
root.minsize(480, 360)
Grid.rowconfigure(root, 0, weight = 1)
Grid.columnconfigure(root, 1, weight = 1)

rootMenuFrame = LabelFrame(root, text = "Menu", width = 90)
rootMenuFrame.grid_propagate(0)
Grid.columnconfigure(rootMenuFrame, 0, weight = 1)
rootConsole = scrolledtext.ScrolledText(root)

rootMenuFrame.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "NSW")
rootConsole.grid(row = 0, column = 1, sticky = "NSEW")



def loadDefaultMenu():
    unloadCurrentMenu()
    displayInRootConsole("Sign in to use the Equipment Depot Inventory Management Assistant.\n\nThere will always be a root user with the ID number of 0.\n\nAll passwords default to 'Password' until changed on first login.")

    btnLogin = Button(rootMenuFrame, text = "LOGIN", command = lambda: loginWindow())
    btnLogin.grid(row = 0, column = 0, sticky = "EW")

def loadEmployeeMenu():
    unloadCurrentMenu()
    displayInRootConsole("Your Current Checkouts:\n" + application.getEmployeeCheckouts(CURRENTLY_LOGGED_IN))

    btnCheckout = Button(rootMenuFrame, text = "CHECKOUT", command = lambda: checkoutWindow())
    btnReturn = Button(rootMenuFrame, text = "RETURN", command = lambda: returnWindow())
    btnLogout = Button(rootMenuFrame, text = "LOGOUT", command = lambda: logout())

    btnCheckout.grid(row = 0, column = 0, sticky = "EW")
    btnReturn.grid(row = 1, column = 0, sticky = "EW")
    btnLogout.grid(row = 2, column = 0, sticky = "EW")

def loadManagerMenu():
    unloadCurrentMenu()
    displayInRootConsole("Enter a submenu to perform an action.")

    btnMngUser = Button(rootMenuFrame, text = "MANAGE\nUSERS", command = lambda: loadUsersSubMenu())
    btnMngEquip = Button(rootMenuFrame, text = "MANAGE\nEQUIPMENT", command = lambda: loadEquipSubMenu())
    btnGenReport = Button(rootMenuFrame, text = "GENERATE\nREPORTS", command = lambda: loadReportsSubMenu())
    btnLogout = Button(rootMenuFrame, text = "LOGOUT", command = lambda: logout())

    btnMngUser.grid(row = 0, column = 0, sticky = "EW")
    btnMngEquip.grid(row = 1, column = 0, sticky = "EW")
    btnGenReport.grid(row = 2, column = 0, sticky = "EW")
    btnLogout.grid(row = 3, column = 0, sticky = "EW")

def loadUsersSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("All Users:\n" + application.getAllUsers())

    btnAddUser = Button(rootMenuFrame, text = "ADD NEW\nUSER", command = lambda: addUserWindow())
    btnRemoveUser = Button(rootMenuFrame, text = "REMOVE\nA USER", command = lambda: removeUserWindow())
    btnModifyUser = Button(rootMenuFrame, text = "MODIFY\nA USER", command = lambda: modifyUserWindow())
    btnBack = Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

    btnAddUser.grid(row = 0, column = 0, sticky = "EW")
    btnRemoveUser.grid(row = 1, column = 0, sticky = "EW")
    btnModifyUser.grid(row = 2, column = 0, sticky = "EW")
    btnBack.grid(row = 3, column = 0, sticky = "EW")

def loadEquipSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("All Equipment:\n" + application.getAllEquipment())

    btnAddEquip = Button(rootMenuFrame, text = "ADD NEW\nEQUIPMENT", command = lambda: addEquipWindow())
    btnRemoveEquip = Button(rootMenuFrame, text = "REMOVE\nEQUIPMENT", command = lambda: removeEquipWindow())
    btnModifyEquip = Button(rootMenuFrame, text = "MODIFY\nEQUIPMENT", command = lambda: modifyEquipWindow())
    btnBack = Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

    btnAddEquip.grid(row = 0, column = 0, sticky = "EW")
    btnRemoveEquip.grid(row = 1, column = 0, sticky = "EW")
    btnModifyEquip.grid(row = 2, column = 0, sticky = "EW")
    btnBack.grid(row = 3, column = 0, sticky = "EW")

def loadReportsSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("Choose a report type to generate.")

    btnRepCheckouts = Button(rootMenuFrame, text = "VIEW ALL\nCHECKOUTS",
        command = lambda: displayInRootConsole("All Active Checkouts:\n" + application.getAllCheckouts()))
    btnRepReturns = Button(rootMenuFrame, text = "VIEW ALL\nRETURN LOGS",
        command = lambda: displayInRootConsole("Full Return Logs:\n" + application.getAllReturns()))
    btnRepUserAll = Button(rootMenuFrame, text = "VIEW ALL\nFROM A\nSELECT USER", command = lambda: reportSpecificUserWindow())
    btnRepEquipAll = Button(rootMenuFrame, text = "VIEW ALL\nFOR SELECT\nEQUIPMENT", command = lambda: reportSpecificEquipWindow())
    btnBack = Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

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
    rootConsole.delete(1.0, END)
    rootConsole.insert(index = 1.0, chars = text)
    rootConsole.configure(state = 'disabled')



def loginWindow():
    top = Toplevel()
    top.title('Login')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmLoginContent = Frame(top)
    
    lblID = Label(frmLoginContent, text = "User ID#: ") #this wil create a label widget
    lblPass = Label(frmLoginContent, text = "Password: ")
    entID = Entry(frmLoginContent) #entry widgets, used to take entry from user 
    entPass = Entry(frmLoginContent, show = "*")
    
    lblID.grid(row = 0, column = 0, sticky = W, pady = 2) #put label widget on the screen 
    lblPass.grid(row = 1, column = 0, sticky = W, pady = 2) 
    entID.grid(row = 0, column = 1, pady = 2) #this will arrange input widgets 
    entPass.grid(row = 1, column = 1, pady = 2)
    
    btnLogin = Button(top, text = "LOGIN",
        command = lambda: login(entID.get(), entPass.get())) #this will create a login button 
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    # grid method to arrange labels in respective 
    frmLoginContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnLogin.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5) #this will arrange the login button 
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def login(userID, password):
        global CURRENTLY_LOGGED_IN
        authenticated = application.login(userID, password)
        if authenticated == 0 or authenticated == 1: messagebox.showerror(message = "Incorrect ID/Password Combination!")
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
        elif authenticated == 5: messagebox.showerror(message = "Fields can not be blank!")
        elif authenticated == 6: messagebox.showerror(message = "User ID must be a number!")



def firstLoginWindow(userID):
    top = Toplevel()
    top.title('Change Password')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmFirstLoginContent = Frame(top)

    lblInfo = Label(frmFirstLoginContent, text = "This is your first time logging in.\nYou need to change your password.")
    lblPass = Label(frmFirstLoginContent, text = "New Password: ")
    lblVerify = Label(frmFirstLoginContent, text = "Confirm New Password: ")
    entPass = Entry(frmFirstLoginContent, show = "*")
    entVerify = Entry(frmFirstLoginContent, show = "*")
    
    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblPass.grid(row = 1, column = 0, sticky = W, pady = 2)
    lblVerify.grid(row = 2, column = 0, sticky = W, pady = 2) 
    entPass.grid(row = 1, column = 1, pady = 2)
    entVerify.grid(row = 2, column = 1, pady = 2)

    btnSubmit = Button(top, text = "SUBMIT",
        command = lambda: firstLogin(entPass.get(), entVerify.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmFirstLoginContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnSubmit.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def firstLogin(password, verify):
        result = application.firstLoginPasswordChange(userID, password, verify)
        if result == 0:
            messagebox.showinfo(message = "Password changed successfully.\nPlease login with your new password.")
            top.destroy()
        elif result == 1: messagebox.showerror(message = "Passwords do not match!")
        elif result == 2: messagebox.showerror(message = "Password is too short!\nYour password must be at least 6 characters")
        elif result == 3: messagebox.showerror(message = "Unexpected error!")



def checkoutWindow():
    top = Toplevel()
    top.title('Checkout')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmCheckoutContent = Frame(top)
    
    lblID = Label(frmCheckoutContent, text = "Enter ID number of\nequipment to check out")
    entID = Entry(frmCheckoutContent)
    
    lblID.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)
    
    btnCheckout = Button(top, text = "CHECKOUT",
        command = lambda: checkout(entID.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmCheckoutContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnCheckout.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def checkout(equipID):
        result = application.checkout(CURRENTLY_LOGGED_IN, equipID)
        if result == 0:
            messagebox.showinfo(message = "Equipment checked out successfully.")
            displayInRootConsole("Your Current Checkouts:\n" + application.getEmployeeCheckouts(CURRENTLY_LOGGED_IN))
            top.destroy()
        elif result == 1: messagebox.showerror(message = "You do not have the skills set for this equipment!\nFor safety reasons you may not check it out.")
        elif result == 2: messagebox.showerror(message = "No equipment exists with the given ID number!")
        elif result == 3: messagebox.showerror(message = "Equipment is already checked out by another user!")
        elif result == 4: messagebox.showerror(message = "You already have this equipment checked out!")
        elif result == 5: messagebox.showerror(message = "Fields can not be blank!")
        elif result == 6: messagebox.showerror(message = "Equipment ID must be a number!")
        elif result == 7: messagebox.showerror(message = "Unexpected error!")



def returnWindow():
    top = Toplevel()
    top.title('Return')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmReturnContent = Frame(top)
    
    lblID = Label(frmReturnContent, text = "Enter ID number of\nequipment to return")
    entID = Entry(frmReturnContent)
    
    lblID.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)
    
    btnReturn = Button(top, text = "RETURN",
        command = lambda: returns(entID.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmReturnContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnReturn.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def returns(equipID):
        result = application.returns(CURRENTLY_LOGGED_IN, equipID)
        if result == 0:
            messagebox.showinfo(message = "Equipment returned successfully.")
            displayInRootConsole("Your Current Checkouts:\n" + application.getEmployeeCheckouts(CURRENTLY_LOGGED_IN))
            top.destroy()
        elif result == 1: messagebox.showerror(message = "No equipment exists with the given ID number!")
        elif result == 2: messagebox.showerror(message = "No users have this equipment checked out!")
        elif result == 3: messagebox.showerror(message = "You do not have this equipment checked out!")
        elif result == 4: messagebox.showerror(message = "Fields can not be blank!")
        elif result == 5: messagebox.showerror(message = "Equipment ID must be a number!")
        elif result == 6: messagebox.showerror(message = "Unexpected error!")



def addUserWindow():
    top = Toplevel()
    top.title('Add New User')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter data for new user.")
    lblID = Label(frmContent, text = "ID Number:")
    lblNameF = Label(frmContent, text = "First Name:")
    lblNameL = Label(frmContent, text = "Last Name:")
    lblSkills = Label(frmContent, text = "Skills:")
    lblPermission = Label(frmContent, text = "Permission:")
    entID = Entry(frmContent)
    entNameF = Entry(frmContent)
    entNameL = Entry(frmContent)
    entSkills = Entry(frmContent)
    entPermission = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = W, pady = 2)
    lblNameF.grid(row = 2, column = 0, sticky = W, pady = 2)
    lblNameL.grid(row = 3, column = 0, sticky = W, pady = 2)
    lblSkills.grid(row = 4, column = 0, sticky = W, pady = 2)
    lblPermission.grid(row = 5, column = 0, sticky = W, pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entNameF.grid(row = 2, column = 1, pady = 2)
    entNameL.grid(row = 3, column = 1, pady = 2)
    entSkills.grid(row = 4, column = 1, pady = 2)
    entPermission.grid(row = 5, column = 1, pady = 2)

    btnAdd = Button(top, text = "ADD",
        command = lambda: addUser(entID.get(), entNameF.get(), entNameL.get(), entSkills.get(), entPermission.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnAdd.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def addUser(userID, nameF, nameL, skills, permission):
        result = application.addUser(CURRENTLY_LOGGED_IN, userID, nameF, nameL, skills, permission)
        if result == 0:
            messagebox.showinfo(message = "User added successfully.")
            displayInRootConsole("All Users:\n" + application.getAllUsers())
            top.destroy()
        elif result == 1: messagebox.showerror(message = "A user already exists with this ID!\nIDs must be unique for each user.")
        elif result == 2: messagebox.showerror(message = "You do not have permission to do this!\nThe permission of users you add must be less than yours.")
        elif result == 3: messagebox.showerror(message = "Fields can not be blank!")
        elif result == 4: messagebox.showerror(message = "User ID, skills, and permission must be numbers!")
        elif result == 5: messagebox.showerror(message = "Unexpected error!")



def removeUserWindow():
    top = Toplevel()
    top.title('Remove a User')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter ID of user to remove.")
    entID = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = Button(top, text = "REMOVE",
        command = lambda: removeUser(entID.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def removeUser(userID):
        result = application.removeUser(CURRENTLY_LOGGED_IN, userID)
        if result == 0:
            messagebox.showinfo(message = "User removed successfully.")
            displayInRootConsole("All Users:\n" + application.getAllUsers())
            top.destroy()
        elif result == 1: messagebox.showerror(message = "No users exist with this ID!")
        elif result == 2: messagebox.showerror(message = "You do not have permission to do this!\nYou can only remove users with lower permission than you.")
        elif result == 3: messagebox.showerror(message = "Fields can not be blank!")
        elif result == 4: messagebox.showerror(message = "User ID must be a number!")
        elif result == 5: messagebox.showerror(message = "Unexpected error!")



def modifyUserWindow():
    top = Toplevel()
    top.title('Modify a User')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter ID of user to change.\nEnter any fields you want to\nupdate with the new data.\nLeave fields blank if you\ndo not want them changed.")
    lblID = Label(frmContent, text = "ID Number:")
    lblNameF = Label(frmContent, text = "First Name:")
    lblNameL = Label(frmContent, text = "Last Name:")
    chkVar = IntVar()
    chkPassword = Checkbutton(frmContent, text = "Reset Password", variable = chkVar, onvalue = 1, offvalue = 0)
    lblSkills = Label(frmContent, text = "Skills:")
    lblPermission = Label(frmContent, text = "Permission:")
    entID = Entry(frmContent)
    entNameF = Entry(frmContent)
    entNameL = Entry(frmContent)
    entSkills = Entry(frmContent)
    entPermission = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = W, pady = 2)
    lblNameF.grid(row = 2, column = 0, sticky = W, pady = 2)
    lblNameL.grid(row = 3, column = 0, sticky = W, pady = 2)
    chkPassword.grid(row = 4, column = 0, columnspan = 2, pady = 2)
    lblSkills.grid(row = 5, column = 0, sticky = W, pady = 2)
    lblPermission.grid(row = 6, column = 0, sticky = W, pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entNameF.grid(row = 2, column = 1, pady = 2)
    entNameL.grid(row = 3, column = 1, pady = 2)
    entSkills.grid(row = 5, column = 1, pady = 2)
    entPermission.grid(row = 6, column = 1, pady = 2)

    btnApply = Button(top, text = "APPLY",
        command = lambda: modifyUser(entID.get(), entNameF.get(), entNameL.get(), chkVar, entSkills.get(), entPermission.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnApply.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def modifyUser(userID, nameF, nameL, password, skills, permission):
        reset = True if password == 1 else False
        result = application.updateUser(CURRENTLY_LOGGED_IN, userID, nameF, nameL, reset, skills, permission)
        if result == 0:
            messagebox.showinfo(message = "User modified successfully.")
            displayInRootConsole("All Users:\n" + application.getAllUsers())
            top.destroy()
        elif result == 1: messagebox.showerror(message = "No users exist with this ID!")
        elif result == 2: messagebox.showerror(message = "You do not have permission to do this!\nYou can only modify users with lower permission than you.")
        elif result == 3: messagebox.showerror(message = "You do not have permission to do this!\nYou can only modify a users permission to be less than yours.")
        elif result == 4: messagebox.showerror(message = "User ID can not be blank!")
        elif result == 5: messagebox.showerror(message = "User ID, skills, and permission must be numbers!")
        elif result == 6: messagebox.showerror(message = "Unexpected error!")



def addEquipWindow():
    top = Toplevel()
    top.title('Add New Equipment')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter data for new equipment.")
    lblID = Label(frmContent, text = "ID Number:")
    lblDesc = Label(frmContent, text = "Description:")
    lblSkills = Label(frmContent, text = "Skills:")
    entID = Entry(frmContent)
    entDesc = Entry(frmContent)
    entSkills = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = W, pady = 2)
    lblDesc.grid(row = 2, column = 0, sticky = W, pady = 2)
    lblSkills.grid(row = 3, column = 0, sticky = W, pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entDesc.grid(row = 2, column = 1, pady = 2)
    entSkills.grid(row = 3, column = 1, pady = 2)

    btnAdd = Button(top, text = "ADD",
        command = lambda: addEquip(entID.get(), entDesc.get(), entSkills.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnAdd.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def addEquip(equipID, desc, skills):
        result = application.addEquipment(equipID, desc, skills)
        if result == 0:
            messagebox.showinfo(message = "Equipment added successfully.")
            displayInRootConsole("All Equipment:\n" + application.getAllEquipment())
            top.destroy()
        elif result == 1: messagebox.showerror(message = "Equipment already exists with this ID!\nIDs must be unique for all equipment.")
        elif result == 2: messagebox.showerror(message = "Fields can not be blank!")
        elif result == 3: messagebox.showerror(message = "Equipment ID and skills must be numbers!")
        elif result == 4: messagebox.showerror(message = "Unexpected error!")



def removeEquipWindow():
    top = Toplevel()
    top.title('Remove Equipment')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter ID of equipment to remove.")
    entID = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = Button(top, text = "REMOVE",
        command = lambda: removeEquip(entID.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def removeEquip(equipID):
        result = application.removeEquipment(equipID)
        if result == 0:
            messagebox.showinfo(message = "Equipment removed successfully.")
            displayInRootConsole("All Equipment:\n" + application.getAllEquipment())
            top.destroy()
        elif result == 1: messagebox.showerror(message = "No equipment exists with this ID!")
        elif result == 2: messagebox.showerror(message = "Fields can not be blank!")
        elif result == 3: messagebox.showerror(message = "Equipment ID must be a number!")
        elif result == 4: messagebox.showerror(message = "Unexpected error!")



def modifyEquipWindow():
    top = Toplevel()
    top.title('Modify Equipment')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter ID of equipment to change.\nEnter any fields you want to\nupdate with the new data.\nLeave fields blank if you\ndo not want them changed.")
    lblID = Label(frmContent, text = "ID Number:")
    lblDesc = Label(frmContent, text = "Description:")
    lblSkills = Label(frmContent, text = "Skills:")
    entID = Entry(frmContent)
    entDesc = Entry(frmContent)
    entSkills = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblID.grid(row = 1, column = 0, sticky = W, pady = 2)
    lblDesc.grid(row = 2, column = 0, sticky = W, pady = 2)
    lblSkills.grid(row = 3, column = 0, sticky = W, pady = 2) 
    entID.grid(row = 1, column = 1, pady = 2)
    entDesc.grid(row = 2, column = 1, pady = 2)
    entSkills.grid(row = 3, column = 1, pady = 2)

    btnApply = Button(top, text = "APPLY",
        command = lambda: modifyEquip(entID.get(), entDesc.get(), entSkills.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnApply.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def modifyEquip(equipID, desc, skills):
        result = application.updateEquipment(equipID, desc, skills)
        if result == 0:
            messagebox.showinfo(message = "Equipment modified successfully.")
            displayInRootConsole("All Equipment:\n" + application.getAllEquipment())
            top.destroy()
        elif result == 1: messagebox.showerror(message = "No equipment exists with this ID!")
        elif result == 2: messagebox.showerror(message = "Equipment ID can not be blank!")
        elif result == 3: messagebox.showerror(message = "Equipment ID and skills must be numbers!")
        elif result == 4: messagebox.showerror(message = "Unexpected error!")



def reportSpecificUserWindow():
    top = Toplevel()
    top.title('Generate User Report')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter ID of user to generate a report of.")
    entID = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = Button(top, text = "SUBMIT",
        command = lambda: generateReport(entID.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def generateReport(userID):
        result = application.getEmployeeAll(userID)
        if result == "x": messagebox.showerror(message = "No user exists with this ID!")
        elif result == "y": messagebox.showerror(message = "User ID can not be blank!")
        elif result == "z": messagebox.showerror(message = "User ID must be a number!")
        else:
            displayInRootConsole("All Activity From User " + userID + ":\n" + result)
            top.destroy()



def reportSpecificEquipWindow():
    top = Toplevel()
    top.title('Generate Equipment Report')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmContent = Frame(top)

    lblInfo = Label(frmContent, text = "Enter ID of equipment to generate a report of.")
    entID = Entry(frmContent)

    lblInfo.grid(row = 0, column = 0, pady = 2)
    entID.grid(row = 1, column = 0, pady = 2)

    btnRemove = Button(top, text = "SUBMIT",
        command = lambda: generateReport(entID.get()))
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    frmContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnRemove.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5)
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def generateReport(equipID):
        result = application.getEquipmentAll(equipID)
        if result == "x": messagebox.showerror(message = "No equipment exists with this ID!")
        elif result == "y": messagebox.showerror(message = "Equipment ID can not be blank!")
        elif result == "z": messagebox.showerror(message = "Equipment ID must be a number!")
        else:
            displayInRootConsole("All Activity For Equipment " + equipID + ":\n" + result)
            top.destroy()



if __name__ == "__main__":
    loadDefaultMenu()
    btnReset = Button(rootMenuFrame, text = "RESET", command = lambda: application.db_conn.reset())
    btnReset.grid(row = 1, column = 0, sticky = "EW")
    mainloop() #infinite loop which can be terminated by keyboard or mouse interrupt 