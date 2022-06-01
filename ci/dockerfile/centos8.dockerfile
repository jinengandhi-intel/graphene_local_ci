From centos:8

ENV http_proxy "http://proxy-dmz.intel.com:911"
ENV https_proxy "http://proxy-dmz.intel.com:912"

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Linux-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-Linux-* 

RUN sed 's/enabled=0/enabled=1/g' /etc/yum.repos.d/CentOS-Linux-PowerTools.repo  | tee /etc/yum.repos.d/CentOS-Linux-PowerTools.repo
RUN echo 'proxy=http://proxy-dmz.intel.com:911' >> /etc/yum.conf

RUN yum install -y yum-utils epel-release
RUN dnf copr enable -y ngompa/musl-libc
RUN yum update -y --exclude=texlive-context && env yum install -y \
    libunwind \
    ncurses-devel \
    bison \
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
    curl \
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
    libX11-devel \
    libXxf86vm \
    libXtst \
    libXfixes \
    libXrender \
    lsof \
    musl-devel \
    musl-gcc \
    nasm \
    nc \
    ncurses-devel \
    ncurses-libs \
    net-tools \
    ninja-build \
    nodejs \
    nss_nis \
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
    protobuf-c-compiler \
    python3 \
    python3-click \
    python3-cryptography \
    python3-devel \
    python3-jinja2 \
    python3-lxml \
    python3-numpy \
    python3-pip \
    python3-protobuf \
    python3-pyelftools \
    python3-pytest \
    python3-scipy \
    R-core \
    strace \
    sqlite \
    sudo \
    vim  \
    texinfo \
    wget \
    unzip \
    zip \
    zlib-devel

RUN python3 -m pip install -U \
    six \
    torchvision \
    pillow \
    'toml>=0.10' \
    'meson>=0.55'

# Add the user UID:1000, GID:1000, home at /intel
RUN groupadd -r intel -g 1000 && useradd -u 1000 -r -g intel -G wheel -m -d /intel -c "intel Jenkins" intel && \
    chmod 777 /intel

# Make sure /intel can be written by intel
RUN chown 1000 /intel

RUN echo '%wheel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
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

