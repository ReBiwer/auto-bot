FROM python:3.12

WORKDIR /app

COPY app/requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
CMD ["python", "aiogram_run.py"]
