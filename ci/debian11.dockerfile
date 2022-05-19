FROM debian:11

ENV DEBIAN_FRONTEND=noninteractive
ENV http_proxy "http://proxy-dmz.intel.com:911"
ENV https_proxy "http://proxy-dmz.intel.com:912"

RUN apt-get update && apt-get install -y gnupg ca-certificates

# Intel's RSA-1024 key signing intel-sgx/sgx_repo below. Expires 2023-05-24.
COPY pkey.txt /

RUN cat /pkey.txt | apt-key add -

RUN echo deb https://download.01.org/intel-sgx/sgx_repo/ubuntu focal main > /etc/apt/sources.list.d/intel-sgx.list
RUN apt-get update

# keep this list synced with Build-Depends: in debian/control
RUN apt-get install -y build-essential \
    apache2-utils \
    autoconf \
    bison \
    devscripts \
    gawk \
    libaio1 \
    libcurl4-openssl-dev \
    libprotobuf-c-dev \
    libsgx-dcap-quote-verify-dev \
    libnss-mdns \
    libssl-dev \
    libxi6 \
    libxxf86vm1 \
    libxfixes3 \
    libxrender1 \
    lsof \
    meson \
    nasm \
    net-tools \
    netcat-openbsd \
    ninja-build \
    pkg-config \
    protobuf-c-compiler \
    python3-breathe \
    python3-cryptography \
    python3-numpy \
    python3-pytest \
    python3-scipy \
    python3-sphinx \
    python3-sphinx-rtd-theme \
    sudo \
    sqlite3 \
    wget \
    zlib1g \
    zlib1g-dev

# Add the user UID:1000, GID:1000, home at /intel
RUN groupadd -r intel -g 1000 && useradd -u 1000 -r -g intel -G sudo -m -d /intel -c "intel Jenkins" intel && \
    chmod 777 /intel

# Make sure /intel can be written by intel
RUN chown 1000 /intel 

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'http_proxy="http://proxy-dmz.intel.com:911/"\nhttps_proxy="http://proxy-dmz.intel.com:912/"' >> /etc/environment

RUN echo 'Acquire::http::proxy "http://proxy-dmz.intel.com:911/";\n Acquire::https::proxy "http://proxy-dmz.intel.com:912/"; Acquire::ftp::proxy "ftp://proxy-dmz.intel.com:911/";\n' >> /etc/apt/apt.conf.d/proxy.conf

# Set the working directory to intel home directory
WORKDIR /intel

# Specify the user to execute all commands below
USER intel

# Set environment variables.
ENV HOME /intel

# Define default command.
CMD ["bash"]
