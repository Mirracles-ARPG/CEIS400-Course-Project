import db_conn, os, hashlib

#EMPLOYEE MENU CODE
def employeeMenu():
    print("--- Employee Menu ---\n")
    print("What would you like to do?")
    print("1. Check-out Equipment")
    print("2. Return Equipment")
    print("3. View Your Equipment Records")
    print("4. Track New Equipment Orders")
    print("5. Log Out\n")
    while True:
        userChoice = input("Enter a menu option: ")
        if userChoice == '1':
            equipID = input("Enter Equipment ID Number to check-out: ")
            checkout(userID, equipID)
            print("\nThis item has now been checked-out.\n\n")
            continue
        elif userChoice == '2':
            equipID = input("Enter Equipment ID Number to check-in: ")
            returns(userID, equipID)
            print("\nThis item has now been returned.\n\n")
            continue
        elif userChoice == '3':
            print("Your Equipment Records:")
            getUser(userID)
            print()
            continue
        elif userChoice == '4':
            print("All New Equipment Orders:")
            generateReport(reportType, userID = None)
            print()
            continue
        elif userChoice == '5':
            cont = input("\nLog Out? (y/n): ").lower()
            while True:
                if cont == "y":
                    print("\nSuccessfully logged out.\n\n")
                    main()
                elif cont == "n":
                    print()
                    employeeMenu()
            


#MANAGER MENU CODE
def managerMenu():
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
            print("Full Employee Equipment Report:")
            generateReport(reportType, userID = None)
            print()
            continue
        elif userChoice == '2':
            print("Employee Information:")
            userID = input("Enter specific user ID: ")
            getUser(userID)
            print()
            continue
        elif userChoice == '3':
            print("Equipment Information:")
            equipID = input("Enter the Equipment ID: ")
            getEquipment(equipID)
            print()
            continue
        elif userChoice == '4':
            print("Checked-out Equipment Status:")
            equipID = input("Enter the Equipment ID: ")
            isCheckedOut(equip)
            print()
            continue
        elif userChoice == '5':
            print()
            
            print()
            continue
        elif userChoice == '6':
            print()
            
            print()
            continue
        elif userChoice == '7':
            print()
            
            print()
            continue
        elif userChoice == '8':
            print()
            
            print()
            continue
        elif userChoice == '9':
            print()
            
            print()
            continue
        elif userChoice == '10':
            print()
            
            print()
            continue
        elif userChoice == '11':
            cont = input("\nLog Out? (y/n): ").lower()
            while True:
                if cont == "y":
                    print("\nSuccessfully logged out.\n\n")
                    main()
                elif cont == "n":
                    print()
                    managerMenu()



def firstLoginPasswordChange(userID):
	print("This is your first time logging in. You must set your password.")
	while True:
		newPassword, verify = input("Enter a secure password: "), input("Enter your password again to verify: ")
		if newPassword == verify:
			salt = os.urandom(32)
			key = hashlib.pbkdf2_hmac('sha256', newPassword.encode('utf-8'), salt, 100000)
			db_conn.updateUser(userID, password = salt + key)
			return True
		else: print("Password entries do not match!")

def login(userID):
    inputPassword = input("Enter your password: ")
    userData = db_conn.getUser(userID)
    if userData != None:
        if userData[3] == inputPassword == db_conn.DEFAULT_PASSWORD: return firstLoginPasswordChange(userID)
        elif userData[3] != db_conn.DEFAULT_PASSWORD:
            salt, key = userData[3][:32], userData[3][32:]
            return key == hashlib.pbkdf2_hmac('sha256', inputPassword.encode('utf-8'), salt, 100000)
    else: return False

def main():
    while True:
        userID = input("Enter your ID number: ")
        if login(userID):
            if db_conn.getUser(userID)[5] == 0: employeeMenu()
            else: managerMenu()
        else: print("Incorrect ID/Password Combination!")

if __name__ == "__main__":
    main()