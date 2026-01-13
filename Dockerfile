FROM python:3.13

# Установка системных зависимостей (если нужны)
# RUN apt-get update && apt-get install -y --no-install-recommends <ваши_зависимости>

# Установка Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Копируем код проекта
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# # Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

