import db_conn, os, hashlib


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


def getAllUsers():
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_ALL_USERS), ""
    for data in report: text = text + "ID#: " + str(data[0]) + " | Name: " + data[1] + " | Skills: " + str(data[2]) + " | Permission: " + str(data[3]) + '\n'
    return text

def getAllEquipment():
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_ALL_EQUIPMENT), ""
    for data in report: text = text + "ID#: " + str(data[0]) + " | Name: " + data[1] + " | Skills: " + str(data[2]) + '\n'
    return text

def getEmployeeCheckouts(userID):
    report, text = db_conn.generateReport(db_conn.REPORT_TYPE_SELECT_USER_CHECKOUTS, userID), ""
    for data in report: text = text + "Equipment: " + data[0] + " | Checkout Time: " + data[1] + '\n'
    return text

def firstLoginPasswordChange(userID, newPassword):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', newPassword.encode('utf-8'), salt, 100000)
    db_conn.updateUser(userID, password = salt + key)

#0 = User not found
#1 = Incorrect Password
#2 = First login
#3 = Employee authenticated
#4 = Manager authenticated
def login(userID, inputPassword):
    userData = db_conn.getUser(userID)
    if userData != None:
        userPassword = userData[3]
        if userPassword == inputPassword == db_conn.DEFAULT_PASSWORD: return 2
        elif userPassword != db_conn.DEFAULT_PASSWORD:
            salt, key = userPassword[:32], userPassword[32:]
            if key == hashlib.pbkdf2_hmac('sha256', inputPassword.encode('utf-8'), salt, 100000):
                if userData[5] == 0: return 3
                else: return 4
            else: return 1
    else: return 0

def main():
    while True:
        userID = input("\nEnter your ID number: ")
        password = input("Enter your password: ")
        authenticated = login(userID, password)
        if authenticated == 0 or authenticated == 1:
            print("Incorrect ID/Password Combination!")
        elif authenticated == 2:
            print("This is your first time logging in. You must change your password.")
            while True:
                newPassword = input("Enter your new password: ")
                verify = input("Verify your new password: ")
                if newPassword == verify:
                    firstLoginPasswordChange(userID, newPassword)
                    print("Password successfully changed. Please log in with your new password.")
                    break
                else: print("Passwords do not match!")
        elif authenticated == 3: employeeMenu(userID)
        elif authenticated == 4: managerMenu(userID)

if __name__ == "__main__":
    main()