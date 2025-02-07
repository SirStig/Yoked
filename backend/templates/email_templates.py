from jinja2 import Template

EMAIL_VERIFICATION_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; }
        .email-container { max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden; }
        .header { background-color: #007bff; color: #ffffff; text-align: center; padding: 20px; }
        .content { padding: 20px; color: #333333; }
        .button { display: inline-block; padding: 10px 20px; background-color: #007bff; color: #ffffff; 
            text-decoration: none; border-radius: 5px; margin-top: 20px; }
        .footer { text-align: center; padding: 10px; background-color: #f4f4f4; color: #777777; font-size: 12px; }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header"><h1>Welcome to Yoked!</h1></div>
        <div class="content">
            <p>Hi {{ username }},</p>
            <p>Thank you for signing up for Yoked. Please verify your email address by clicking the button below:</p>
            <a href="{{ verification_link }}" class="button">Verify Email</a>
            <p>If you didn’t sign up for Yoked, you can safely ignore this email.</p>
        </div>
        <div class="footer"><p>&copy; {{ current_year }} Yoked. All rights reserved.</p></div>
    </div>
</body>
</html>
""")

EMAIL_CODE_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verify Your Email</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; }
        .email-container { max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 10px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden; }
        .header { background-color: #007bff; color: #ffffff; text-align: center; padding: 20px; }
        .content { padding: 20px; color: #333333; text-align: center; }
        .code-box { font-size: 24px; font-weight: bold; color: #007bff; background-color: #f1f1f1; padding: 10px; 
            border-radius: 5px; display: inline-block; margin-top: 20px; }
        .footer { text-align: center; padding: 10px; background-color: #f4f4f4; color: #777777; font-size: 12px; }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header"><h1>Verify Your Email</h1></div>
        <div class="content">
            <p>Hi {{ username }},</p>
            <p>Your verification code is:</p>
            <div class="code-box">{{ verification_code }}</div>
            <p>This code is valid for 10 minutes. If you did not request this, please ignore this email.</p>
        </div>
        <div class="footer"><p>&copy; {{ current_year }} Yoked. All rights reserved.</p></div>
    </div>
</body>
</html>
""")

