ARG BUILD_OS

FROM $BUILD_OS

# Add steps here to set up dependencies
RUN apt-get update -y && env DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
    cmake \
    curl \
    diffutils \
    gcc \
    git \
    lsb-release \
    lsof \
    make \
    nginx \
    pkg-config \
    python3-pip \
    python3-pkg-resources \
    python3-pytest \
    sudo \
    sshpass \
    wget

RUN if [ "$(lsb_release -sc)" = "noble" ]; then \
        apt install -y netcat-openbsd meson && \
        userdel -r ubuntu; \
    else \
        python3 -m pip install -U 'meson>=0.56,<0.57' && \
        apt install -y netcat; \
    fi

RUN mkdir -p /etc/apt/keyrings

RUN curl -fsSLo /etc/apt/keyrings/intel-sgx-deb.asc https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key

RUN echo "deb [arch=amd64  signed-by=/etc/apt/keyrings/intel-sgx-deb.asc] https://download.01.org/intel-sgx/sgx_repo/ubuntu $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/intel-sgx.list

RUN curl -fsSLo /etc/apt/keyrings/gramine-keyring-$(lsb_release -sc).gpg https://packages.gramineproject.io/gramine-keyring-`lsb_release -sc`.gpg

RUN apt update -y && apt install -y libsgx-dcap-default-qpl libsgx-dcap-default-qpl-dev

# Add the user UID:1000, GID:1000, home at /intel
RUN groupadd -r intel -g 1000 && useradd -u 1000 -r -g intel -G sudo -m -d /intel -c "intel Jenkins" intel && \
    chmod 777 /intel

# Make sure /intel can be written by intel
RUN chown 1000 /intel 

RUN echo 'intel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'http_proxy="http://proxy-dmz.intel.com:911/"\nhttps_proxy="http://proxy-dmz.intel.com:912/"' >> /etc/environment

# Blow away any random state
RUN rm -f /intel/.rnd

# Make a directory for the intel driver
RUN mkdir -p /opt/intel && chown 1000 /opt/intel

# Make a directory for the Gramine installation
RUN mkdir -p /home/intel/gramine_install && chown 1000 /home/intel/gramine_install

# Set the working directory to intel home directory
WORKDIR /intel

# Specify the user to execute all commands below
USER intel

# Set environment variables.
ENV HOME /intel

# Define default command.
CMD ["bash"]
