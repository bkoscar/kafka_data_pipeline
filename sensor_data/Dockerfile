# Base image
FROM ubuntu:22.04 AS base
LABEL maintainer="Omar"

# System configuration
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Mexico_City

# Install base dependencies
RUN apt-get update \
    && apt-get install -y sudo software-properties-common tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# User environment variables
ENV USER_NAME=omar
ENV HOME_DIR=/home/$USER_NAME
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user
RUN useradd -m -s /bin/bash -u 1000 $USER_NAME && \
    echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER_NAME && \
    chmod 0440 /etc/sudoers.d/$USER_NAME

# Set working directory
USER $USER_NAME
WORKDIR $HOME_DIR

# Install Python and development tools
RUN sudo add-apt-repository ppa:deadsnakes/ppa -y && \
    sudo apt-get update && \
    sudo apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    && sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN sudo chown -R $USER_NAME:$USER_NAME $HOME_DIR && \
    python3 -m venv $HOME_DIR/sensor_venv
# Set Python environment variables
ENV PATH=$HOME_DIR/sensor_venv/bin:$PATH

RUN pip install --upgrade pip

# Copy project files
COPY src $HOME_DIR/

# Expose port
EXPOSE 5555



# Configure shell
SHELL ["/bin/bash", "-c"]
CMD ["python", "main.py"]