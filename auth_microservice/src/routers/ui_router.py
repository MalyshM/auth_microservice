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
    <title>Registration Forms FOR INFORMATIONAL PURPOSES ONLY</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }}

        h1{{
            color: #333;
            margin-bottom: 20px;
        }}

        .form-container {{
            display: none;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 300px;
            margin-top: 20px;
        }}

        .form-container.active {{
            display: block;
        }}

        h2 {{
            color: #555;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}

        label {{
            display: block;
            margin-bottom: 5px;
            color: #666;
            font-weight: bold;
        }}

        input[type="text"],
        input[type="email"],
        input[type="password"] {{
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }}

        button {{
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            background-color: #007bff;
            color: white;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}

        button:hover {{
            background-color: #0056b3;
        }}

        .form-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}

        .form-buttons button {{
            flex: 1;
        }}

        .toggle-buttons {{
            margin-bottom: 20px;
        }}

        .toggle-buttons button {{
            margin: 0 5px;
            background-color: #6c757d;
        }}

        .toggle-buttons button:hover {{
            background-color: #5a6268;
        }}
    </style>
</head>
<body>
    <h1>Registration Forms FOR INFORMATIONAL PURPOSES ONLY</h1>
    <div class="toggle-buttons">
        <button onclick="showForm('usernameForm')">Username/Password</button>
        <button onclick="showForm('emailForm')">Email/Password</button>
        <button onclick="showForm('phoneForm')">Phone/Password</button>
    </div>

    <div id="usernameForm" class="form-container active">
        <h2>Username/Password Registration</h2>
        <form id="usernameRegistrationForm">
            <label for="{USERNAME_FIELD}">Username:</label>
            <input type="text" id="{USERNAME_FIELD}" name="{USERNAME_FIELD}">
            <label for="{PASSWORD_FIELD}">Password:</label>
            <input type="password" id="{PASSWORD_FIELD}"
            name="{PASSWORD_FIELD}">
            <div class="form-buttons">
                <button type="button" onclick="submitUsernameForm()">Register
                </button>
                <button type="button"
                onclick="submitLoginForm('{USERNAME_FIELD}',
                '{PASSWORD_FIELD}')">Login
                </button>
            </div>
        </form>
    </div>

    <div id="emailForm" class="form-container">
        <h2>Email/Password Registration</h2>
        <form id="emailRegistrationForm">
            <label for="{EMAIL_FIELD}">Email:</label>
            <input type="email" id="{EMAIL_FIELD}" name="{EMAIL_FIELD}">
            <label for="{PASSWORD_FIELD}">Password:</label>
            <input type="password" id="{PASSWORD_FIELD}"
            name="{PASSWORD_FIELD}">
            <div class="form-buttons">
                <button type="button" onclick="submitEmailForm()">Register
                </button>
                <button type="button"
                onclick="submitLoginForm('{EMAIL_FIELD}',
                '{PASSWORD_FIELD}')">Login
                </button>
            </div>
        </form>
    </div>

    <div id="phoneForm" class="form-container">
        <h2>Phone/Password Registration</h2>
        <form id="phoneRegistrationForm">
            <label for="{PHONE_FIELD}">Phone:</label>
            <input type="text" id="{PHONE_FIELD}" name="{PHONE_FIELD}">
            <label for="{PASSWORD_FIELD}">Password:</label>
            <input type="password" id="{PASSWORD_FIELD}"
            name="{PASSWORD_FIELD}">
            <div class="form-buttons">
                <button type="button"
                onclick="submitPhoneForm()">
                Register</button>
                <button type="button" onclick="submitLoginForm('{PHONE_FIELD}',
                '{PASSWORD_FIELD}')">Login</button>
            </div>
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
                headers:{{
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
