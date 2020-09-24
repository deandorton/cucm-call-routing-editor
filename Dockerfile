# Use minimal Alpine Linux with Python 3.7.3
FROM python:3.7
LABEL maintainer="bzoellers@ddaftech.com"

# Commands to execute after container is deployed
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
WORKDIR /src

# Expose flasks default HTTP port
EXPOSE 5000/tcp

# Run the program
ENTRYPOINT ["python"]
CMD ["app.py"]