FROM python:3.6.5-slim
WORKDIR /app
ADD . /app

RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py", "production"]
