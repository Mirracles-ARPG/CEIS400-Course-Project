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
    displayInRootConsole("Sign in to use the Equipment Depot Inventory Management Assistant.")

    btnLogin = Button(rootMenuFrame, text = "LOGIN", command = lambda: loginWindow())
    btnLogin.grid(row = 0, column = 0, sticky = "EW")

def loadEmployeeMenu():
    unloadCurrentMenu()
    displayInRootConsole("Your Current Checkouts:\n" + application.getEmployeeCheckouts(CURRENTLY_LOGGED_IN))

    btnCheckout = Button(rootMenuFrame, text = "CHECKOUT")
    btnReturn = Button(rootMenuFrame, text = "RETURN")
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

    btnAddUser = Button(rootMenuFrame, text = "ADD NEW\nUSER")
    btnRemoveUser = Button(rootMenuFrame, text = "REMOVE\nA USER")
    btnModifyUser = Button(rootMenuFrame, text = "MODIFY\nA USER")
    btnBack = Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

    btnAddUser.grid(row = 0, column = 0, sticky = "EW")
    btnRemoveUser.grid(row = 1, column = 0, sticky = "EW")
    btnModifyUser.grid(row = 2, column = 0, sticky = "EW")
    btnBack.grid(row = 3, column = 0, sticky = "EW")

def loadEquipSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("All Equipment:\n" + application.getAllEquipment())

    btnAddEquip = Button(rootMenuFrame, text = "ADD NEW\nEQUIPMENT")
    btnRemoveEquip = Button(rootMenuFrame, text = "REMOVE\nEQUIPMENT")
    btnModifyEquip = Button(rootMenuFrame, text = "MODIFY\nEQUIPMENT")
    btnBack = Button(rootMenuFrame, text = "BACK", command = lambda: loadManagerMenu())

    btnAddEquip.grid(row = 0, column = 0, sticky = "EW")
    btnRemoveEquip.grid(row = 1, column = 0, sticky = "EW")
    btnModifyEquip.grid(row = 2, column = 0, sticky = "EW")
    btnBack.grid(row = 3, column = 0, sticky = "EW")

def loadReportsSubMenu():
    unloadCurrentMenu()
    displayInRootConsole("Choose a report type to generate.")

    btnRepCheckouts = Button(rootMenuFrame, text = "VIEW ALL\nCHECKOUTS")
    btnRepReturns = Button(rootMenuFrame, text = "VIEW ALL\nRETURN LOGS")
    btnRepUserAll = Button(rootMenuFrame, text = "VIEW ALL\nFROM A\nSELECT USER")
    btnRepEquipAll = Button(rootMenuFrame, text = "VIEW ALL\nFOR SELECT\nEQUIPMENT")
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
        if authenticated == 0 or authenticated == 1:
            messagebox.showerror(message = "Incorrect ID/Password Combination.")
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



def firstLoginWindow(userID):
    top = Toplevel()
    top.title('Change Password')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmFirstLoginContent = Frame(top)

    lblInfo = Label(frmFirstLoginContent, text = "This is your first time logging in.\nYou need to change your password.")
    lblPass = Label(frmFirstLoginContent, text = "New Password: ") #this wil create a label widget
    lblVerify = Label(frmFirstLoginContent, text = "Confirm New Password: ")
    entPass = Entry(frmFirstLoginContent, show = "*") #entry widgets, used to take entry from user 
    entVerify = Entry(frmFirstLoginContent, show = "*")
    
    lblInfo.grid(row = 0, column = 0, columnspan = 2, pady = 2)
    lblPass.grid(row = 1, column = 0, sticky = W, pady = 2) #put label widget on the screen 
    lblVerify.grid(row = 2, column = 0, sticky = W, pady = 2) 
    entPass.grid(row = 1, column = 1, pady = 2) #this will arrange input widgets 
    entVerify.grid(row = 2, column = 1, pady = 2)

    btnSubmit = Button(top, text = "SUBMIT",
        command = lambda: firstLogin(entPass.get(), entVerify.get())) #this will create a login button 
    btnCancel = Button(top, text = "CANCEL", command = top.destroy)

    # grid method to arrange labels in respective 
    frmFirstLoginContent.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)
    btnSubmit.grid(row = 1, column = 0, sticky = E, padx = 5, pady = 5) #this will arrange the login button 
    btnCancel.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 5)

    def firstLogin(password, verify):
        if password == verify:
            application.firstLoginPasswordChange(userID, password)
            messagebox.showinfo(message = "Password changed successfully.\nPlease login with your new password.")
            top.destroy()
        else: messagebox.showerror(message = "Passwords do not match!")



if __name__ == "__main__":
    loadDefaultMenu()
    mainloop() #infinite loop which can be terminated by keyboard or mouse interrupt 