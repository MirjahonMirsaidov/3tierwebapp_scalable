from core.utils.email.email import send_email


def send_verification_code(email, code):
    email_body = code + ' - Ваш код подтверждения от Tez ish bor'
    data = {'email_body': email_body, 'to_email': email,
            'email_subject': 'Kод подтверждения'}

    send_email(data)

