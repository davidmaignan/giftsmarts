USERNAME_REGEX = "^[\w]{10}$"
PASSWORD_REGEX = "^(?=[^\d_].*?\d)\w(\w|[!@#$%]){7,20}$"
#This regex can be used to restrict passwords to a length of 8 to 20 aplhanumeric characters and select special characters. The password also can not start with a digit, underscore or special character and must contain at least one digit.

USERNAME_EXISTS_MSG = "Username already exists!"
INVALID_USERNAME_MSG = "Invalid username format!"
INVALID_PASSWORD_MSG = "Invalid password format!"


#Reserved roles
ROLES = {
    "ADMIN": 0,
    "TEACHER": 1,
    "STUDENT": 2
}
