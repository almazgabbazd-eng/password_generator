import random
import string

def generate_password(length, use_letters=True, use_digits=True, use_special=True):
    """Генерирует случайный пароль с заданными параметрами."""
    if length < 1:
        raise ValueError("Длина пароля должна быть хотя бы 1 символ")

    chars = ""
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation

    if not chars:
        raise ValueError("Должен быть выбран хотя бы один тип символов")

    return ''.join(random.choice(chars) for _ in range(length))
