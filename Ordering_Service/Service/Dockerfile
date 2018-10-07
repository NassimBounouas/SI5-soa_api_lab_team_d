FROM python:3.6.5-slim
WORKDIR /app
ADD db.ini ServiceCommand.py /app/
RUN pip install flask
RUN pip3 install PyMySQL

ENTRYPOINT ["python"]
CMD ["ServiceCommand.py"]
