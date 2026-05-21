VALID_TASK_STATUSES = ["todo", "in_progress", "done"]


def validate_request_body(data):

    return data is not None


def validate_title(title):

    return 3 <= len(title) <= 255


def validate_description(description):

    if description is None:
        return True

    return len(description) <= 1000


def validate_task_status(status):

    return status in VALID_TASK_STATUSES
