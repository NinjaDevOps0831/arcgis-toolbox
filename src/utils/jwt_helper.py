import jwt


def email_from_jwt(token):
    if token is None:
        raise ValueError("Authentication token not provided.")
    else:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded["principal_name"]


def has_role(token, role):
    if token is None:
        raise ValueError("Authentication token not provided.")
    else:
        decoded = jwt.decode(token, options={"verify_signature": False})
        roles = decoded["security_roles"]
        return role in roles
