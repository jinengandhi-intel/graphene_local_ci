From almalinux:9

ENV http_proxy "http://proxy-dmz.intel.com:911"
ENV https_proxy "http://proxy-dmz.intel.com:912"

RUN echo 'proxy=http://proxy-dmz.intel.com:911' >> /etc/yum.conf

RUN sed -i 's/enabled=0/enabled=1/g' /etc/yum.repos.d/almalinux-crb.repo

RUN yum install -y yum-utils epel-release
RUN yum update -y --exclude=texlive-context && env yum install -y \
    libunwind \
    cargo \
    cmake \
    ncurses-devel \
    bc \
    bison \
    busybox \
    flex \
    make \
    elfutils-libelf-devel \
    openssl-devel \
    rpm-build \
#   epel-next-release \
    automake \
    autoconf \
    bison \
    binutils \
    gawk \
    gcc-c++ \
    gdb \
    git \
    glibc-static \
    glibc.i686 \
    golang \
    httpd \
    info \
    java-11-openjdk \
    java-11-openjdk-devel \
    jq \
    less \
    libcurl-devel \
    libevent-devel \
    libjpeg-turbo-devel \
    libmemcached \
    libX11-devel \
    libXxf86vm \
    libXtst \
    libXfixes \
    libXrender \
    lsof \
    nasm \
    nc \
    ncurses-devel \
    ncurses-libs \
    net-tools \
    ninja-build \
    nodejs \
    nss-mdns \
    nss-myhostname \
    openssl-devel \
    protobuf-devel \
    protobuf-c-devel \
    patch \
#   libcurl4-openssl-dev \
#   libprotobuf-c-dev \
#   linux-headers-generic \
    pkg-config \
    procps-ng \
    protobuf-c-compiler \
    python3 \
    python3-click \
    python3-cryptography \
    python3-devel \
    python3-jinja2 \
    python3-lxml \
    python3-pkg-resources \
    python3-pip \
    python3-protobuf \
    python3-pyelftools \
    python3-pytest \
    python3-voluptuous \
    R-core \
    strace \
    stress-ng \
    sqlite \
    sudo \
    vim  \
    texinfo \
    wget \
    unzip \
    zip \
    zlib-devel

# Install wrk2 benchmark. This benchmark is used in `benchmark-http.sh`.
RUN git clone https://github.com/giltene/wrk2.git \
    && cd wrk2 \
    && git checkout 44a94c17d8e6a0bac8559b53da76848e430cb7a7 \
    && make \
    && cp wrk /usr/local/bin \
    && cd .. \
    && rm -rf wrk2

RUN python3 -m pip install -U \
    dataclasses \
    six \
    torchvision \
    pillow \
    numpy \
    scipy \
    'tomli>=1.1.0' \
    'tomli-w>=0.4.0' \
    'meson>=0.56,<0.57'

# Add mongodb workload
RUN echo -e "[mongodb-org-7.0]\nname=MongoDB Repository\nbaseurl=https://repo.mongodb.org/yum/redhat/8/mongodb-org/7.0/x86_64/\ngpgcheck=1\nenabled=1\ngpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc" >> /etc/yum.repos.d/mongodb-org-7.0.repo

RUN dnf update -y && dnf install -y mongodb-org

# Add the user UID:1000, GID:1000, home at /intel
RUN groupadd -r intel -g 1000 && useradd -u 1000 -r -g intel -G wheel -m -d /intel -c "intel Jenkins" intel && \
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
