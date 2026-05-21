import re


def validate_request_body(data):

    return data is not None


def validate_required_fields(*fields):

    return all(field for field in fields)


def validate_email_format(email):

    email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    return re.match(email_pattern, email)


def validate_username(username):

    return 3 <= len(username) <= 50


def validate_password(password):

    return len(password) >= 8
