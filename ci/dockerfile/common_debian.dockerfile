ARG BUILD_OS

FROM $BUILD_OS

# Add steps here to set up dependencies
RUN apt-get update && env DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y \
    curl \
    gcc\
    git \
    lsb-release \
    vim \
    make \
    meson \
    netcat-openbsd \
    pkg-config \
    python3-pip \
    python3-pytest \
    sudo \
    sshpass \
    wget


# if you don't already have backports repo enabled:
RUN echo "deb http://deb.debian.org/debian $(lsb_release -sc)-backports main" \
| sudo tee /etc/apt/sources.list.d/backports.list

RUN echo 'deb [arch=amd64] https://download.01.org/intel-sgx/sgx_repo/ubuntu bionic main' \
    > /etc/apt/sources.list.d/intel-sgx.list \
    && wget https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key \
    && apt-key add intel-sgx-deb.key

RUN curl -fsSLo /usr/share/keyrings/gramine-keyring.gpg https://packages.gramineproject.io/gramine-keyring.gpg

RUN apt-get update

RUN apt install -y libsgx-dcap-default-qpl libsgx-dcap-default-qpl-dev

# Add the user UID:1000, GID:1000, home at /intel
RUN groupadd -r intel -g 1000 && useradd -u 1000 -r -g intel -G sudo -m -d /intel -c "intel Jenkins" intel && \
    chmod 777 /intel

# Make sure /intel can be written by intel
RUN chown 1000 /intel 

RUN echo 'intel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'http_proxy="http://proxy-dmz.intel.com:911/"\nhttps_proxy="http://proxy-dmz.intel.com:912/"' >> /etc/environment
RUN echo 'Acquire::http::proxy "http://proxy-dmz.intel.com:911/";\nAcquire::http::proxy "http://proxy-dmz.intel.com:911/";' >> /etc/apt/apt.conf.d/80proxy

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
