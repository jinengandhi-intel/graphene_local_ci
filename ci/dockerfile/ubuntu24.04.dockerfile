FROM ubuntu:24.04

# Add steps here to set up dependencies
RUN apt-get update -y && env DEBIAN_FRONTEND=noninteractive apt-get install -y \
    autoconf \
    bc \
    bison \
    binutils \
    build-essential \
    busybox \
    cargo \
    cmake \
    clang \
    curl \
    flex \
    gawk \
    file \
    gdb \
    gettext \
    git \
    gnupg \
    gnupg2 \
    golang \
    jq \
    libapr1-dev \
    libaprutil1-dev \
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
    libjudy-dev \
    libpixman-1-dev \
    libipsec-mb-dev \
    lsb-release \
    lsof \
    musl \
    musl-tools \ 
    nasm \
    net-tools \
    netcat-openbsd \
    nginx \
    ninja-build \
    nodejs \
    openjdk-11-jdk \
    pkg-config \
    protobuf-c-compiler \
    protobuf-compiler \
    pylint \
    python3-apport \
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
    python3-voluptuous \
    r-base \
    shellcheck \
    sphinx-doc \
    stress-ng \
    sqlite3 \
    sudo \
    texinfo \
    uthash-dev \
    vim \
    wget \
    zlib1g \
    zlib1g-dev

RUN apt-get update && apt-get satisfy -y \
    'libcurl4 (>= 7.58)' \
    'python3' \
    'python3 (>= 3.10) | python3-pkg-resources' \
    'python3-pyelftools' \
    'python3-tomli (>= 1.1.0)' \
    'python3-tomli-w (>= 0.4.0)' \
    'docutils' \
    'meson'  

# Install wrk2 benchmark. This benchmark is used in `benchmark-http.sh`.
RUN git clone https://github.com/giltene/wrk2.git \
    && cd wrk2 \
    && git checkout 44a94c17d8e6a0bac8559b53da76848e430cb7a7 \
    && make \
    && cp wrk /usr/local/bin \
    && cd .. \
    && rm -rf wrk2

RUN usermod -aG sudo ubuntu

RUN echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'http_proxy="http://proxy-dmz.intel.com:911/"\nhttps_proxy="http://proxy-dmz.intel.com:912/"' >> /etc/environment

# Define default command.
CMD ["bash"]
