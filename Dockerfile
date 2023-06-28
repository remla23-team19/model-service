# Dockerfile
FROM python:3.8-slim
WORKDIR /root
COPY requirements.txt /root/
RUN pip install -r requirements.txt
COPY app.py /root/
COPY model_library.py /root/
COPY models/ /root/models/
ENTRYPOINT ["python"]
CMD ["app.py"]
EXPOSE 8080
