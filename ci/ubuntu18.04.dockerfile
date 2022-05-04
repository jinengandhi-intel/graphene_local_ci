# Start with 18.04
FROM ubuntu:18.04

# Add steps here to set up dependencies
RUN apt-get update && env DEBIAN_FRONTEND=noninteractive apt-get install -y \
    apache2-utils \
    autoconf \
    bison \
    build-essential \
    curl \
    flex \
    gawk \
    gdb \
    gettext \
    git \
    golang \
    jq \
    libaio1 \
    libapr1-dev \
    libaprutil1-dev \
    libcurl4-openssl-dev \
    libelf-dev \
    libevent-dev \
    libexpat1 \
    libexpat1-dev \
    libmemcached-tools \
    libnss-mdns \
    libnuma1 \
    libomp-dev \
    libpcre2-dev \
    libpcre3-dev \
    libprotobuf-c-dev \
    libssl-dev \
    libunwind8 \
    libxfixes3 \
    libxi6 \
    libxml2-dev \
    libxrender1 \
    libxxf86vm1 \
    libjudy-dev \
    libpixman-1-dev \
    libipsec-mb-dev \
    linux-headers-4.15.0-20-generic \
    musl \
    musl-tools \
    nasm \
    net-tools \
    netcat-openbsd \
    ninja-build \
    pkg-config \
    protobuf-c-compiler \
    pylint3 \
    python \
    python3-apport \
    python3-apt \
    python3-breathe \
    python3-click \
    python3-cryptography \
    python3-jinja2 \
    python3-lxml \
    python3-numpy \
    python3-pip \
    python3-protobuf \
    python3-pyelftools \
    python3-pytest \
    python3-pytest-xdist \
    python3-scipy \
    sqlite3 \
    shellcheck \
    sudo \
    texinfo \
    uthash-dev \
    vim \
    wget \
    zlib1g \
    zlib1g-dev

# NOTE about meson version: we support "0.55 or newer", so in CI we pin to latest patch version of
# the earliest supported minor version (pip implicitly installs latest version satisfying the
# specification)
RUN python3 -m pip install -U \
    asv \
    recommonmark \
    'Sphinx==1.8' \
    sphinx_rtd_theme \
    'toml>=0.10' \
    'meson>=0.55,<0.56'

# # Add the user UID:1000, GID:1000, home at /intel
# RUN groupadd -r intel -g 1000 && useradd -u 1000 -r -g intel -m -d /intel -c "intel Jenkins" intel && \
#     chmod 777 /intel

# # Make sure /intel can be written by intel
# RUN chown 1000 /intel

RUN adduser --disabled-password --gecos '' intel
RUN adduser intel sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'Acquire::http::proxy "http://proxy-dmz.intel.com:911/"; Acquire::https::proxy "http://proxy-dmz.intel.com:912/"; Acquire::ftp::proxy "ftp://proxy-dmz.intel.com:911/";' >> /etc/apt/apt.conf.d/proxy.conf

# Blow away any random state
RUN rm -f /intel/.rnd

# Make a directory for the intel driver
RUN mkdir -p /opt/intel && chown 1000 /opt/intel

RUN mkdir -p /home/intel/rust_binaries && chown 1000 /home/intel/rust_binaries
ENV CARGO_HOME="/home/intel/rust_binaries"
ENV RUSTUP_HOME="/home/intel/rust_binaries"
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable

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
