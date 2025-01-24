FROM python:3.8-slim as builder

# Sets the environment variables coming from the build arguments
ARG GIT_USER
ARG GIT_PW

# Installs additional packages for building python packages
RUN apt-get update &&  \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Adds the Python virtual environment to the Path variable
ENV PATH="/opt/venv/bin:$PATH"

# Sets current working directory to the src directory
WORKDIR /app

# Copies the requirements file to the Docker image
COPY requirements.txt .

# Creates a Python virtual environment, upgrades the pip version and installs required Python packages
RUN python -m venv /opt/venv &&  \
    /opt/venv/bin/python -m pip install --no-cache-dir --no-deps --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3.8-alpine3.16

# Copies the Python virtual environment from the build stage
COPY --from=builder /opt/venv /opt/venv

# Adds the Python virtual environment to the Path variable
ENV PATH="/opt/venv/bin:$PATH"

# Sets current working directory to the src directory
WORKDIR /src

# Adds a new user that runs the app
RUN adduser -D app_user && \
    mkdir -p /etc/sudoers.d && \
    echo "app_user ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/app_user && \
    chmod 0440 /etc/sudoers.d/app_user && \
    chown -R app_user:app_user /src

# Sets the newly created user as default
USER app_user

# Copies the application code to the current working directory
COPY src /src

# Sets current working directory to the root directory
WORKDIR /

# Exposes the port where application is running on
EXPOSE 8080/tcp

# Defines the start command of the app
CMD ["gunicorn", "-c", "src/gunicorn_config.py", "src.wsgi:app"]
