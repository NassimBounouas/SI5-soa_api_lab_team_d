FROM python:3.6.5-slim
WORKDIR /app
ADD Eta.py /app/
RUN pip install flask

ENTRYPOINT ["python"]
CMD ["Eta.py"]
