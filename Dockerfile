
FROM python:3.9-slim-buster

# Install the security updates
RUN apt-get update
RUN apt-get -y upgrade

# Build-essentials is needed to execute gcc commands,
# to build discord packages dependencies "multidict"
RUN apt-get install -y build-essential

# Remove all cached file. Get a smaller image
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# Copy the application
COPY . /opt/app
WORKDIR /opt/app

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install python libraries
RUN pip install -r requirements.txt

# Start the app
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]