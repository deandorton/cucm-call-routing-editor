# Use minimal Alpine Linux with Python 3.7.3
FROM python:3.7
LABEL maintainer="bzoellers@ddaftech.com"

# Use current directory
WORKDIR /src

# Commands to execute after container is deployed
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

# Expose flasks default HTTP port
EXPOSE 5000/tcp

# Run the program
ENTRYPOINT ["python"]
CMD ["app.py"]