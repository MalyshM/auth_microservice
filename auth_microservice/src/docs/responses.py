response_401 = {
    "description": (
        "Unauthorized. The user is not "
        "authenticated or the token is invalid."
    ),
    "content": {
        "application/json": {
            "example": {"detail": "Not authenticated"},
        }
    },
}
auth_200 = {
    "description": "Authentication successful. Returns the user GUID.",
    "content": {
        "application/json": {"example": "af926384-fa75-4da9-a5b2-1d81f2e1e5f8"}
    },
}

auth_403 = {
    "description": "Authentication is not successful. Returns JSON.",
    "content": {
        "application/json": {"example": {"detail": "Send true code_verifier"}}
    },
}
reg_response_400 = {
    "description": (
        "Bad Request. User could not be registered. "
        "This may be due to invalid input or other validation errors."
    ),
    "content": {
        "application/json": {
            "example": {
                "detail": (
                    "User  could not be registered. <specific error message>"
                )
            },
        }
    },
}
logout_200 = {
    "description": "Successfully logged out..",
    "content": {
        "application/json": {"example": {"detail": "Successfully logged out."}}
    },
}
create_response_400 = {
    "description": (
        "Bad Request. User could not be created. "
        "This may be due to invalid input or other validation errors."
    ),
    "content": {
        "application/json": {
            "example": {
                "detail": (
                    "User could not be created. <specific error message>"
                )
            },
        }
    },
}
update_response_400 = {
    "description": (
        "Bad Request. User could not be updated. "
        "This may be due to invalid input or other validation errors."
    ),
    "content": {
        "application/json": {
            "example": {
                "detail": (
                    "User could not be updated. <specific error message>"
                )
            },
        }
    },
}
delete_response_400 = {
    "description": (
        "Bad Request. User could not be deleted. "
        "This may be due to invalid input or other validation errors."
    ),
    "content": {
        "application/json": {
            "example": {
                "detail": (
                    "User could not be deleted. <specific error message>"
                )
            },
        }
    },
}
response_403 = {
    "description": (
        "Forbidden. The user provided incorrect data. "
        "This may indicate that the user does not have permission "
        "to perform this action or the data provided is invalid."
    ),
    "content": {
        "application/json": {
            "example": {"detail": "User  provided incorrect data."},
        }
    },
}
response_404 = {
    "description": (
        "Not Found. The specified user could not be found. "
        "This may indicate that the user ID does not exist."
    ),
    "content": {
        "application/json": {
            "example": {"detail": "User  not found. <specific error message>"},
        }
    },
}

response_400_general = {
    "description": (
        "Bad Request. An error occurred while processing the request. "
        "This may be due to invalid input or other issues."
    ),
    "content": {
        "application/json": {
            "example": {"detail": "Error: <specific error message>"},
        }
    },
}
