# CEIS400-Course-Project

Upon download/install the database will be in it's default state.
There will only be 1 user, the root user.
The root user has an ID of 0, and a password of 'Password' (case sensitive).
Upon signing in for the first time you will be prompted to change the password from the default and log in again.
After signing in with your new password you may user the root user to add any number of users/equipment you wish.
ID numbers for users/equipment you create must be unique.
Skills will restrict equipment to only be able to be checked out by a user with the same skill number.
If skills is set to 0 the equipment can be checked out by anyone.
Permission determines whether someone is an employee or manager of the system (permission=0 for employees / permission>0 for managers).
Permission also determines what managers can do. They can only create/modify users with permission less than theirs.
