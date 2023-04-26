import re

class Validation():
    def register_validation(name, email):
        return not (re.match("^[a-zA-Z ]*$", name) and re.match("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email))
  