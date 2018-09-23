import string





def Is_Special_Character(character):
    valid_characters = string.ascii_letters + string.digits + "@."
    if character not in valid_characters:
        return True
    else:
        return False

def Registration_Checker(attempted_username, attempted_email, attempted_password,
                         attempted_repassword, attempted_accept):
    password_rules = [lambda s: any(x.isupper() for x in s),
                  lambda s: any(x.islower() for x in s),
                  lambda s: any(x.isdigit() for x in s),
                  lambda s: len(s) >= 6]
    all_characters = attempted_username + attempted_email + attempted_password
    special_characters = []
    special_characters = [character for character in all_characters if Is_Special_Character(character)]
    if len(special_characters) > 0:
        return ("You can only use the ASCII characters, basically english alphabet and numerical    " +
                 "characters plus the @ sign for the e-mail adress.")
    elif len(attempted_username) < 4 or len(attempted_username) >= 25:
        return "The username has to be between 4 and 25 characters long!"
    elif len(attempted_email) >= 125 or attempted_email == "":
        return "The email field is required and has to be shorter than 125 characters!"
    elif not all(password_rule(attempted_password) for password_rule in password_rules):
        return ("The password has to be at least 6 characters long. Must also contain " +
                 "UPPER and lower case letters alongside with at least 1 d1g1t(s).")
    elif attempted_password != attempted_repassword:
        return "The two password fields have to match!"
    elif attempted_accept == False:
        return "You have to accept the Terms of Service"
    else:
        return ""
    
    
"""
all_characters = attempted_username + attempted_email + attempted_password
special_characters = []
special_characters = [character for character in all_characters if is_special(character, valid_characters)]
if len(special_characters) > 0:
    error = ("You can only use the ASCII characters, basically english alphabet and numerical" +
             "characters plus the @ sign for the e-mail adress.")
    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
elif len(attempted_username) < 4 or len(attempted_username) >= 25:
    error = "The username has to be between 4 and 25 characters long!"
    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
elif len(attempted_email) >= 125 or attempted_email == "":
    error = "The email field is required and has to be shorter than 125 characters!"
    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
elif not all(password_rule(attempted_password) for password_rule in password_rules):
    error = ("The password has to be at least 6 characters long. Must also contain " +
             "UPPER and lower case letters alongside with at least 1 d1g1t(s).")
    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
elif attempted_password != attempted_repassword:
    error = "The two password fields have to match!"
    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
elif attempted_accept == False:
    error = "You have to accept the Terms of Service"
    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
    
    
"""
    
    
    
    
    
    
    
    
    