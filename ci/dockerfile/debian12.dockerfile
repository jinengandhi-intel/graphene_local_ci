FROM debian:12

# Add steps here to set up dependencies
RUN apt-get update -y && env DEBIAN_FRONTEND=noninteractive apt-get install -y \
    autoconf \
    bc \
    bison \
    build-essential \
    busybox \
    cmake \
    clang \
    curl \
    default-jdk \
    file \
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
    libcjson-dev \
    libelf-dev \
    libevent-dev \
    libexpat1 \
    libexpat1-dev \
    libjpeg-dev \
    libmemcached-tools \
    libnss-mdns \
    libnss-myhostname \
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
    linux-headers-amd64 \
    libjudy-dev \
    libpixman-1-dev \
    libipsec-mb-dev \
    lsb-release \
    lsof \
    meson \
    musl \
    musl-tools \ 
    nasm \
    net-tools \
    netcat-openbsd \
    ninja-build \
    nodejs \
    pkg-config \
    protobuf-c-compiler \
    protobuf-compiler \
    pylint \
    python3-apt \
    python3-breathe \
    python3-click \
    python3-cryptography \
    python3-jinja2 \
    python3-lxml \
    python3-numpy \
    python3-pandas \
    python3-pil \
    python3-pip \
    python3-pkg-resources \
    python3-protobuf \
    python3-pyelftools \
    python3-pytest \
    python3-pytest-xdist \
    python3-recommonmark \
    python3-scipy \
    python3-sphinx-rtd-theme \
    python3-tomli \
    python3-tomli-w \
    python3-torchvision \
    python3-voluptuous \
    r-base \
    sqlite3 \
    shellcheck \
    sphinx-doc \
    stress-ng \
    texinfo \
    uthash-dev \
    vim \
    wget \
    zlib1g \
    sudo \
    zlib1g-dev \
    gnupg2 \
    binutils

# Install latest Rust and cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN cp -rf $HOME/.cargo/bin/* /usr/bin/

# Install wrk2 benchmark. This benchmark is used in `benchmark-http.sh`.
RUN git clone https://github.com/giltene/wrk2.git \
    && cd wrk2 \
    && git checkout 44a94c17d8e6a0bac8559b53da76848e430cb7a7 \
    && make \
    && cp wrk /usr/local/bin \
    && cd .. \
    && rm -rf wrk2

# Adding mongodb repo installation
RUN curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
        sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/debian $(lsb_release -sc)/mongodb-org/7.0 main" | \
        sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

RUN apt-get update && apt-get install -y mongodb-org

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
