import random
import string

def generate_password(length=12, include_uppercase=True, include_numbers=True, include_symbols=True):
  """
  Генерирует случайный пароль заданной длины, используя заданные символы.

  Args:
    length: Длина пароля (по умолчанию 12 символов).
    include_uppercase: Включать ли прописные буквы (по умолчанию True).
    include_numbers: Включать ли цифры (по умолчанию True).
    include_symbols: Включать ли символы (по умолчанию True).

  Returns:
    Случайный пароль.
  """

  characters = string.ascii_lowercase  # строчные буквы
  if include_uppercase:
    characters += string.ascii_uppercase  # прописные буквы
  if include_numbers:
    characters += string.digits  # цифры
  if include_symbols:
    characters += string.punctuation  # символы

  password = ''.join(random.choice(characters) for i in range(length))
  return password

# Пример использования
password = generate_password(length=16, include_symbols=False)  # пароль длиной 16 символов без символов
print("Ваш Пароль:", password)
