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
