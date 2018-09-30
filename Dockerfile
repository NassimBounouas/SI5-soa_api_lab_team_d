FROM python:3.6.5-slim
WORKDIR /app
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV FLASK_APP="app.py"
ENV FLASK_ENV="development"

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["app.py"]
