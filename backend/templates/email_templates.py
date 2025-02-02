# backend/templates/email_templates.py

from datetime import datetime

# Email verification template
EMAIL_VERIFICATION_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
        }
        .email-container {
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .header {
            background-color: #007bff;
            color: #ffffff;
            text-align: center;
            padding: 20px;
        }
        .content {
            padding: 20px;
            color: #333333;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }
        .footer {
            text-align: center;
            padding: 10px;
            background-color: #f4f4f4;
            color: #777777;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Welcome to Yoked!</h1>
        </div>
        <div class="content">
            <p>Hi {{ username }},</p>
            <p>Thank you for signing up for Yoked. Please verify your email address by clicking the button below:</p>
            <a href="{{ verification_link }}" class="button">Verify Email</a>
            <p>If you didn’t sign up for Yoked, you can safely ignore this email.</p>
        </div>
        <div class="footer">
            <p>&copy; {year} Yoked. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
""".replace("{year}", str(datetime.now().year))
