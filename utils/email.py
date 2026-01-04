import os
from jinja2 import Environment, FileSystemLoader


def send_verification_email(
    email: str,
    name: str,
    token: str,
    base_url: str = "http://127.0.0.1:8000"
) -> None:
    """
    Отправляет письмо со ссылкой для верификации на указанный email.
    В тестах — выводит в консоль, в продакшене можно заменить на SMTP.
    """
    verify_url = f"{base_url}/verify-email?token={token}"
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("verify_email.html")
    html_content = template.render(name=name, verify_url=verify_url)

    # Логируем письмо (в продакшене — отправка через SMTP)
    print(f" Отправка письма на: {email}")
    print(f"--- Тема: Подтвердите ваш email ---")
    print(f"{html_content}")
    print(f"--- Конец письма ---\n")


# Пример для future: асинхронная отправка (можно расширить)
async def send_email_async(
    email: str,
    subject: str,
    template_name: str,
    context: dict,
    base_url: str = "http://127.0.0.1:8000"
):
    # В будущем: использовать aiosmtplib, FastAPI BackgroundTasks
    pass