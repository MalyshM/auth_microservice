import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

USERNAME_FIELD = os.getenv("USERNAME_FIELD", "username")
EMAIL_FIELD = os.getenv("EMAIL_FIELD", "email")
PHONE_FIELD = os.getenv("PHONE_FIELD", "phone")
PASSWORD_FIELD = os.getenv("PASSWORD_FIELD", "password")

ui_router = APIRouter(prefix="/ui", tags=["UI"])


registration_forms = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration Forms</title>
    <style>
        .form-container {{ display: none; }}
        .active {{ display: block; }}
        button {{ margin: 5px; }}
    </style>
</head>
<body>
    <h1>Registration Forms</h1>
    <button onclick="showForm('usernameForm')">Username/Password</button>
    <button onclick="showForm('emailForm')">Email/Password</button>
    <button onclick="showForm('phoneForm')">Phone/Password</button>

    <div id="usernameForm" class="form-container active">
        <h2>Username/Password Registration</h2>
        <form id="usernameRegistrationForm">
            <label for="{USERNAME_FIELD}">Username:</label><br>
            <input type="text" id="{USERNAME_FIELD}"
            name="{USERNAME_FIELD}"><br><br>
            <label for="{PASSWORD_FIELD}">Password:</label><br>
            <input type="password" id="{PASSWORD_FIELD}"
            name="{PASSWORD_FIELD}"><br><br>
            <button type="button"
            onclick="submitUsernameForm()">Register</button>
            <button type="button"
            onclick="submitLoginForm('{USERNAME_FIELD}', '{PASSWORD_FIELD}')">
            Login</button>
        </form>
    </div>

    <div id="emailForm" class="form-container">
        <h2>Email/Password Registration</h2>
        <form id="emailRegistrationForm">
            <label for="{EMAIL_FIELD}">Email:</label><br>
            <input type="email" id="{EMAIL_FIELD}" name="{EMAIL_FIELD}"><br><br>
            <label for="{PASSWORD_FIELD}">Password:</label><br>
            <input type="password" id="{PASSWORD_FIELD}"
            name="{PASSWORD_FIELD}"><br><br>
            <button type="button" onclick="submitEmailForm()">Register</button>
            <button type="button"
            onclick="submitLoginForm('{EMAIL_FIELD}', '{PASSWORD_FIELD}')">
            Login</button>
        </form>
    </div>

    <div id="phoneForm" class="form-container">
        <h2>Phone/Password Registration</h2>
        <form id="phoneRegistrationForm">
            <label for="{PHONE_FIELD}">Phone:</label><br>
            <input type="text" id="{PHONE_FIELD}" name="{PHONE_FIELD}"><br><br>
            <label for="{PASSWORD_FIELD}">Password:</label><br>
            <input type="password" id="{PASSWORD_FIELD}"
            name="{PASSWORD_FIELD}"><br><br>
            <button type="button" onclick="submitPhoneForm()">Register</button>
            <button type="button"
            onclick="submitLoginForm('{PHONE_FIELD}', '{PASSWORD_FIELD}')">
            Login</button>
        </form>
    </div>

    <script>
        function showForm(formId) {{
            // Hide all forms
            document.querySelectorAll('.form-container').forEach(form => {{
                form.classList.remove('active');
            }});
            // Show the selected form
            document.getElementById(formId).classList.add('active');
        }}

        async function submitUsernameForm() {{
            const username = document.getElementById('{USERNAME_FIELD}').value;
            const password = document.getElementById('{PASSWORD_FIELD}').value;

            const response = await fetch('/register', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{ {USERNAME_FIELD}: username,
                {PASSWORD_FIELD}: password }}),
            }});

            const result = await response.json();
        }}

        async function submitEmailForm() {{
            const email = document.getElementById('{EMAIL_FIELD}').value;
            const password = document.getElementById('{PASSWORD_FIELD}').value;

            const response = await fetch('/register', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{ {EMAIL_FIELD}: email,
                {PASSWORD_FIELD}: password }}),
            }});

            const result = await response.json();
        }}

        async function submitPhoneForm() {{
            const phone = document.getElementById('{PHONE_FIELD}').value;
            const password = document.getElementById('{PASSWORD_FIELD}').value;

            const response = await fetch('/register', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{ {PHONE_FIELD}: phone,
                {PASSWORD_FIELD}: password }}),
            }});

            const result = await response.json();
        }}

        async function submitLoginForm(field, passwordField) {{
            const fieldValue = document.getElementById(field).value;
            const password = document.getElementById(passwordField).value;

            const response = await fetch('/login', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{ [field]: fieldValue,
                [passwordField]: password }}),
            }});

            const result = await response.json();
        }}
    </script>
</body>
</html>
"""


@ui_router.get("/", response_class=HTMLResponse)
async def get_registration_forms():
    return HTMLResponse(content=registration_forms)
