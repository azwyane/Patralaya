FROM python:3.8

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Dont let python to write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# create root directory for our project in the container
RUN mkdir /Patralaya

# Set the working directory to /Patralaya
WORKDIR /Patralaya

# Copy the current directory contents into the container at /Patralaya
ADD . /Patralaya/

# Install gnu gettext
RUN apt install gettext

# Install packages specified in requirements.txt
RUN pip install -r requirements.txt