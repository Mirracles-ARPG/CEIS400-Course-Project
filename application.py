import db_conn, os, hashlib



def main():
    while True:
        userID, password = input("Enter your ID number: "), input("Enter your password: ")
        authenticated = login(userID, password)
        if authenticated == 0 or authenticated == 1: print("Incorrect ID/Password Combination!")
        elif authenticated == 2:
            print("This is your first time logging in. You must change your password.")
            while True:
                newPassword, verify = input("Enter your new password: "), input("Verify your new password: ")
                result = firstLoginPasswordChange(userID, newPassword, verify)
                if result == 0:
                    print("Password successfully changed. Please log in with your new password.")
                    break
                elif result == 1: print("Passwords do not match!")
                elif result == 2: print("Password is too short! Your password must be at least 6 characters")
                elif result == 3: print("Unexpected error!")
        elif authenticated == 3: employeeMenu(userID)
        elif authenticated == 4: managerMenu(userID)
        elif authenticated == 5: print("Fields can not be blank!")
        elif authenticated == 6: print("User ID must be a number!")

#EMPLOYEE MENU CODE
def employeeMenu(userID):
    print("--- Employee Menu ---\n")
    print("What would you like to do?")
    print("1. Check-out Equipment")
    print("2. Return Equipment")
    print("3. View All Available Equipment")
    print("4. View Your Equipment History")
    print("5. Log Out\n")
    while True:
        userChoice = input("Enter a menu option: ")
        if userChoice == '1':
            equipID = input("\nEnter Equipment ID Number to check-out: ")
            print(db_conn.checkout(userID, equipID))
            print("\nThis item has now been checked-out.\n")
            continue
        elif userChoice == '2':
            equipID = input("\nEnter Equipment ID Number to check-in: ")
            print(db_conn.returns(userID, equipID))
            print("\nThis item has now been returned.\n")
            continue
        elif userChoice == '3':
            print("\nAll Available Equipment:\n")
            print(db_conn.generateReport(db_conn.REPORT_TYPE_ALL_EQUIPMENT))
            print()
            continue
        elif userChoice == '4':
            print("\nYour Equipment History:\n")
            print(db_conn.generateReport(db_conn.REPORT_TYPE_SELECT_USER_CHECKOUTS, userID))
            print()
            continue
        elif userChoice == '5':
            cont = input("\nLog Out? (y/n): ").lower()
            while True:
                if cont == "y":
                    print("\nSuccessfully Logged Out.\n\n")
                    return
                elif cont == "n":
                    print()
                    break

#MANAGER MENU CODE
def managerMenu(userID):
    print("--- Manager Menu ---\n")
    print("What would you like to do?")
    print("1. Full Employee Equipment Report")
    print("2. Employee Information")
    print("3. Equipment Information")
    print("4. Checked-out Equipment Status")
    print("5. Update an Existing User")
    print("6. Add a New User")
    print("7. Remove a User")
    print("8. Update Existing Equipment")
    print("9. Add Equipment")
    print("10. Remove Equipment")
    print("11. Log Out\n")
    while True:
        userChoice = input("Enter a menu option: ")
        if userChoice == '1':
            print("\nFull Employee Equipment Report\n")
            employeeID = input("Enter the Employee's ID: ")
            print(db_conn.generateReport(db_conn.REPORT_TYPE_SELECT_USER_ALL, employeeID))
            print()
            continue
        elif userChoice == '2':
            print("\nEmployee Information\n")
            employeeID = input("Enter the Employee's ID: ")
            print(db_conn.getUser(employeeID))
            print()
            continue
        elif userChoice == '3':
            print("\nEquipment Information\n")
            equipID = input("Enter the Equipment ID: ")
            print(db_conn.getEquipment(equipID))
            print()
            continue
        elif userChoice == '4':
            print("\nChecked-out Equipment Status\n")
            equipID = input("Enter the Equipment ID: ")
            print(db_conn.isCheckedOut(equipID))
            print()
            continue
        elif userChoice == '5':
            print("\nUpdate Existing User\n")
            employeeID = input("Enter the Existing User's ID: ")
            nameF = input("Enter First Name: ")
            nameL = input("Enter Last Name: ")
            skills = input("Enter Skills: ")
            permission = input("Enter Permission Level: ")
            print(db_conn.updateUser(employeeID, nameF, nameL, skills, permission))
            print()
            continue
        elif userChoice == '6':
            print("\nAdd User\n")
            employeeID = input("Enter New Employee ID: ")
            nameF = input("Enter First Name: ")
            nameL = input("Enter Last Name: ")
            skills = input("Enter Skills: ")
            permission = input("Enter Permission Level: ")
            print(db_conn.addUser(employeeID, nameF, nameL, skills, permission))
            print()
            continue
        elif userChoice == '7':
            print("\nRemove User\n")
            employeeID = input("Enter Employee ID to be Removed: ")
            print(db_conn.removeUser(employeeID))
            print()
            continue
        elif userChoice == '8':
            print("\nUpdate Existing Equipment\n")
            equipID = input("Enter the Existing Equipment ID: ")
            desc = input("Enter Description: ")
            skills = input("Enter Skill Level: ")
            print(db_conn.updateEquipment(equipID, desc, skills))
            print()
            continue
        elif userChoice == '9':
            print("\nAdd Equipment\n")
            equipID = input("Enter New Equipment ID: ")
            desc = input("Enter Description: ")
            skills = input("Enter Skill Level: ")
            print(db_conn.addEquipment(equipID, desc, skills))
            print()
            continue
        elif userChoice == '10':
            print("\nRemove Equipment\n")
            equipID = input("Enter Equipment ID to be Removed: ")
            print(db_conn.removeEquipment(equipID))
            print()
            continue
        elif userChoice == '11':
            cont = input("\nLog Out? (y/n): ").lower()
            while True:
                if cont == "y":
                    print("\nSuccessfully Logged Out.\n\n")
                    return
                elif cont == "n":
                    print()
                    break



#0 = User not found
#1 = Incorrect Password
#2 = First login
#3 = Employee authenticated
#4 = Manager authenticated
#5 = Input field is blank
#6 = User ID is not a number
def login(userID, inputPassword):
    if userID == "" or inputPassword == "": return 5
    if not userID.isdigit(): return 6
    userData = db_conn.getUser(userID)
    if userData != None:
        userPassword = userData[3]
        if userPassword == db_conn.DEFAULT_PASSWORD: 
            if inputPassword == userPassword: return 2
            else: return 1
        else:
            salt, key = userPassword[:32], userPassword[32:]
            if key == hashlib.pbkdf2_hmac('sha256', inputPassword.encode('utf-8'), salt, 100000):
                if userData[5] == 0: return 3
                else: return 4
            else: return 1
    else: return 0

#0 = Password changed successfully
#1 = Passwords do not match
#2 = Password length is too short
#3 = Unexpected error
def firstLoginPasswordChange(userID, newPassword, verify):
    if newPassword != verify: return 1
    if len(newPassword) < 6: return 2
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', newPassword.encode('utf-8'), salt, 100000)
    if db_conn.updateUser(userID, password = salt + key): return 0
    else: return 3

#0 = Checkout successful
#1 = User does not have the requisite skills to check out equipment
#2 = Equipment does not exist
#3 = Another user already has this equipment checked out
#4 = Current user already has this equipment checked out
#5 = Input field is blank
#6 = Equipment ID is not a number
#7 = Unexpected error
def checkout(userID, equipID):
    if equipID == "": return 5
    if not equipID.isdigit(): return 6
    if db_conn.getEquipment(equipID) == None: return 2
    result = db_conn.isCheckedOut(equipID)
    if result == 0:
        userSkills, equipSkills = db_conn.getUser(userID)[4], db_conn.getEquipment(equipID)[2]
        if equipSkills == 0 or equipSkills == userSkills:
            if db_conn.checkout(userID, equipID): return 0
            else: return 7
        else: return 1
    elif result == 1:
        result = db_conn.isCheckedOut(equipID, userID)
        if result == 0: return 3
        elif result == 1: return 4
        elif result == 2: return 7
    elif result == 2: return 7

#0 = Return successful
#1 = Equipment does not exist
#2 = No user has equipment checked out
#3 = Current user does not have equipment checked out
#4 = Input field is blank
#5 = Equipment ID is not a number
#6 = Unexpected error
def returns(userID, equipID):
    if equipID == "": return 4
    if not equipID.isdigit(): return 5
    if db_conn.getEquipment(equipID) == None: return 1
    result = db_conn.isCheckedOut(equipID)
    if result == 0: return 2
    elif result == 1: 
        result = db_conn.isCheckedOut(equipID, userID)
        if result == 0: return 3
        elif result == 1:
            if db_conn.returns(userID, equipID): return 0
            else: return 6
        elif result == 2: return 6
    elif result == 2: return 6

#0 = Add successful
#1 = User already exists with given ID
#2 = User does not have the permission to create a user with this permission value
#3 = Input field is blank
#4 = User ID, skills, or permission is not a number
#5 = Unexpected error
def addUser(managerID, userID, nameF, nameL, skills, permission):
    if userID == "" or nameF == "" or nameL == "" or skills == "" or permission == "": return 3
    if not userID.isdigit() or not skills.isdigit() or not permission.isdigit(): return 4
    if db_conn.getUser(userID) != None: return 1
    if db_conn.getUser(managerID)[5] <= int(permission): return 2
    if db_conn.addUser(userID, nameF, nameL, skills, permission): return 0
    else: return 5

#0 = Remove successful
#1 = User does not exist
#2 = User does not have the permission to delete this user
#3 = Input field is blank
#4 = User ID is not a number
#5 = Unexpected error
def removeUser(managerID, userID):
    if userID == "": return 3
    if not userID.isdigit(): return 4
    userLookup = db_conn.getUser(userID)
    if userLookup == None: return 1
    if db_conn.getUser(managerID)[5] <= userLookup[5]: return 2
    if db_conn.removeUser(userID): return 0
    else: return 5

#0 = Update successful
#1 = User does not exist
#2 = User does not have the permission to modify this user
#3 = User does not have the permission to set user permission to this value
#4 = User ID field is blank
#5 = User ID, skills, or permission is not a number
#6 = Attempt to modify root
#7 = Attempt to modify self
#8 = Unexpected error
def updateUser(managerID, userID, nameF = None, nameL = None, password = 0, skills = None, permission = None):
    if userID == "": return 4
    if not userID.isdigit(): return 5
    if userID == 0: return 6
    if managerID == userID: return 7
    if nameF == "": nameF = None
    if nameL == "": nameL = None
    resetPassword = db_conn.DEFAULT_PASSWORD if password == 1 else None
    if skills == "": skills = None
    elif not skills.isdigit(): return 5
    if permission == "": permission = None
    elif not permission.isdigit(): return 5
    userLookup = db_conn.getUser(userID)
    if userLookup == None: return 1
    managerPermission = db_conn.getUser(managerID)[5]
    if managerPermission <= userLookup[5]: return 2
    if permission != None:
        if int(permission) >= managerPermission: return 3
    if db_conn.updateUser(userID, nameF, nameL, resetPassword, skills, permission): return 0
    else: return 8

#0 = Add successful
#1 = Equipment already exists with given ID
#2 = Input field is blank
#3 = Equipment ID or skills is not a number
#4 = Unexpected error
def addEquipment(equipID, desc, skills):
    if equipID == "" or desc == "" or skills == "": return 2
    if not equipID.isdigit() or not skills.isdigit(): return 3
    if db_conn.getEquipment(equipID) != None: return 1
    if db_conn.addEquipment(equipID, desc, skills): return 0
    else: return 4

#0 = Remove successful
#1 = Equipment does not exist
#2 = Input field is blank
#3 = Equipment ID is not a number
#4 = Unexpected error
def removeEquipment(equipID):
    if equipID == "": return 2
    if not equipID.isdigit(): return 3
    if db_conn.getEquipment(equipID) == None: return 1
    if db_conn.removeEquipment(equipID): return 0
    else: return 4

#0 = Update successful
#1 = Equipment does not exist
#2 = Input field is blank
#3 = User ID or skills is not a number
#4 = Unexpected error
def updateEquipment(equipID, desc = None, skills = None):
    if equipID == "": return 2
    if not equipID.isdigit(): return 3
    if desc == "": desc = None
    if skills == "": skills = None
    elif not skills.isdigit(): return 3
    if db_conn.getEquipment(equipID) == None: return 1
    if db_conn.updateEquipment(equipID, desc, skills): return 0
    else: return 4

def getAllCheckouts():
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_ALL_CHECKOUTS), ""
    for data in report: text = text + "Employee: " + data[0] + " | Equipment: " + data[1] + " | Checkout Time: " + data[2] + '\n' 
    return text

def getAllReturns():
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_ALL_RETURN_LOGS), ""
    for data in report: text = text + "Employee: " + data[0] + " | Equipment: " + data[1] + " | Checkout Time: " + data[2] + " | Return Time: " + data[3] + '\n' 
    return text

#x = User does not exist
#y = Input field is blank
#z = User ID is not a number
def getEmployeeAll(userID):
    if userID == "": return "y"
    if not userID.isdigit(): return "z"
    if db_conn.getUser(userID) == None: return "x"
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_SELECT_USER_ALL, userID), ""
    for data in report: text = text + data[0] + " | Checkout Time: " + data[1] + " | Return Time: " + data[2] + '\n' 
    return text

#x = Equipment does not exist
#y = Input field is blank
#z = Equipment ID is not a number
def getEquipmentAll(equipID):
    if equipID == "": return "y"
    if not equipID.isdigit(): return "z"
    if db_conn.getEquipment(equipID) == None: return "x"
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_SELECT_EQUIP_ALL, equipID), ""
    for data in report: text = text + data[0] + " | Checkout Time: " + data[1] + " | Return Time: " + data[2] + '\n' 
    return text



def getUserNameplate(userID):
    data = db_conn.getUser(userID)
    return "#" + str(data[0]) + " " + data[1] + " " + data[2]

def getEquipNameplate(equipID):
    data = db_conn.getEquipment(equipID)
    return "#" + str(data[0]) + " " + data[1]

def getEmployeeCheckouts(userID):
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_SELECT_USER_CHECKOUTS, userID), ""
    for data in report: text = text + data[0] + " | Checkout Time: " + data[1] + '\n' 
    return text

def getAllUsers():
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_ALL_USERS), ""
    for data in report: text = text + data[0] + " | Skills: " + str(data[1]) + " | Permission: " + str(data[2]) + '\n' 
    return text

def getAllEquipment():
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_ALL_EQUIPMENT), ""
    for data in report: text = text + data[0] + " | Skills: " + str(data[1]) + '\n' 
    return text



if __name__ == "__main__":
    db_conn.initialize()
    main()