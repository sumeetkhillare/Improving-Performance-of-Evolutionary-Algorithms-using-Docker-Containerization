FROM python
WORKDIR /userapp
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt ./requirements.txt
RUN python -m pip install -r 'requirements.txt'
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi", "--timeout", "6000"]
