import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown


def send_email(settings: dict, subject: str, markdown_body: str):
    env = settings["env"]

    required = ["EMAIL_FROM", "EMAIL_TO", "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD"]
    missing = [k for k in required if not env.get(k)]
    if missing:
        raise ValueError(f"Missing email settings: {', '.join(missing)}")

    html_body = markdown.markdown(markdown_body, extensions=["tables", "fenced_code"])

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = env["EMAIL_FROM"]
    msg["To"] = env["EMAIL_TO"]

    msg.attach(MIMEText(markdown_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(env["SMTP_HOST"], int(env["SMTP_PORT"])) as server:
        server.starttls()
        server.login(env["SMTP_USER"], env["SMTP_PASSWORD"])
        server.sendmail(env["EMAIL_FROM"], [env["EMAIL_TO"]], msg.as_string())
