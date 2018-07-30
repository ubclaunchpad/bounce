# Use the Python 3 image as our base image
FROM python:3.6

# Copy project directory to /opt/bounce
ADD . /opt/bounce

# Set default working directory to /opt/bounce
WORKDIR /opt/bounce

# Make sure pip is up to date and install pip-tools for managing dependencies
RUN pip install --upgrade pip pip-tools

# Install required python packages
RUN make install-requirements && make install-test-requirements
