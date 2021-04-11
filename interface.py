from tkinter import *
from tkinter import messagebox
import application

CURRENTLY_LOGGED_IN = None

root = Tk() #creating main tkinter window
root.title('Equipment Depot Software')

rootMenuFrame = LabelFrame(root, text = "Menu")
#BOX

rootMenuFrame.grid(row = 0, column = 0)
#BOX



def loadDefaultMenu():
    btnLogin = Button(rootMenuFrame, text = "LOGIN", command = lambda: loginWindow())
    btnLogin.grid(row = 0, column = 0)

def loadEmployeeMenu():
    btnCheckout = Button(rootMenuFrame, text = "CHECKOUT")
    btnReturn = Button(rootMenuFrame, text = "RETURN")
    btnView = Button(rootMenuFrame, text = "VIEW")
    btnLogout = Button(rootMenuFrame, text = "LOGOUT", command = lambda: logout())

    btnCheckout.grid(row = 0, column = 0)
    btnReturn.grid(row = 1, column = 0)
    btnView.grid(row = 2, column = 0)
    btnLogout.grid(row = 3, column = 0)

def loadManagerMenu():
    btnCheckout = Button(rootMenuFrame, text = "CHECKOUT")
    btnReturn = Button(rootMenuFrame, text = "RETURN")
    btnView = Button(rootMenuFrame, text = "VIEW M")
    btnLogout = Button(rootMenuFrame, text = "LOGOUT", command = lambda: logout())

    btnCheckout.grid(row = 0, column = 0)
    btnReturn.grid(row = 1, column = 0)
    btnView.grid(row = 2, column = 0)
    btnLogout.grid(row = 3, column = 0)

def logout():
    CURRENTLY_LOGGED_IN = None
    unloadCurrentMenu()
    loadDefaultMenu()

def unloadCurrentMenu(): 
    for widget in rootMenuFrame.winfo_children(): widget.destroy()



def loginWindow():
    top = Toplevel()
    top.title('Login')
    top.resizable(0, 0)
    top.attributes('-toolwindow', True)

    frmLoginContent = Frame(top)
    
    lblID = Label(frmLoginContent, text = "User ID#: ") #this wil create a label widget
    lblPass = Label(frmLoginContent, text = "Password: ")
    entID = Entry(frmLoginContent) #entry widgets, used to take entry from user 
    entPass = Entry(frmLoginContent)
    
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
        authenticated = application.login(userID, password)
        if authenticated == 0 or authenticated == 1:
            messagebox.showerror(message = "Incorrect ID/Password Combination.")
        elif authenticated == 2:
            firstLoginWindow(userID)
            top.destroy()
        elif authenticated == 3:
            currentlyLoggedIn = userID
            unloadCurrentMenu()
            loadEmployeeMenu()
            top.destroy()
        elif authenticated == 4:
            currentlyLoggedIn = userID
            unloadCurrentMenu()
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
    entPass = Entry(frmFirstLoginContent) #entry widgets, used to take entry from user 
    entVerify = Entry(frmFirstLoginContent)
    
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