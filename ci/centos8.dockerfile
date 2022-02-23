# Currently tested base OS images are Ubuntu 18.04 and Ubuntu 20.04.
From centos:8

ENV http_proxy "http://proxy-dmz.intel.com:911"
ENV https_proxy "http://proxy-dmz.intel.com:912"

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Linux-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-Linux-* 

RUN sed 's/enabled=0/enabled=1/g' /etc/yum.repos.d/CentOS-Linux-PowerTools.repo  | tee /etc/yum.repos.d/CentOS-Linux-PowerTools.repo
RUN echo 'proxy=http://proxy-dmz.intel.com:911' >> /etc/yum.conf

RUN cat /etc/yum.repos.d/CentOS-Linux-PowerTools.repo
RUN yum install yum-utils -y
RUN yum install -y epel-release 
RUN yum install libunwind -y
RUN cat /etc/yum.repos.d/CentOS-Linux-PowerTools.repo
RUN yum install -y ncurses-devel bison flex make elfutils-libelf-devel openssl-devel rpm-build 
RUN dnf copr enable -y ngompa/musl-libc
#dwarves 
RUN yum update -y \
    && env yum install -y \
        epel-release \
#        libunwind \
#        epel-next-release \
        automake \
        autoconf \
        bison \
        binutils \
#        coreutils \
        curl \
        gawk \
        gdb \
        git \
        glibc-static \
        glibc.i686 \
        golang \
        jq \
        net-tools \
        nc \
        ncurses-devel \
        ncurses-libs \
        nss-mdns \
        openssl-devel \
        protobuf-devel \
        protobuf-c-devel \
        less \
        libcurl-devel \
        httpd \
        libevent-devel \
        libX11-devel \
        libXxf86vm \
        libXtst \
        libXfixes \
        libXrender \
        patch \
        gcc-c++ \
        info \
#        libcurl4-openssl-dev \
#        libprotobuf-c-dev \
#        linux-headers-generic \
        musl-devel \
        musl-gcc \
        ninja-build \
        nss_nis \
        pkg-config \
        protobuf-c-compiler \
        python3 \
        python3-click \
        python3-cryptography \
        python3-jinja2 \
        python3-lxml \
        python3-numpy \ 
        python3-scipy \
        python3-pyelftools \
        python3-pytest \
        strace \
        vim  \      
        python3-pip \
        python3-protobuf \
        sqlite \
        texinfo \
        wget \
    && python3 -B -m pip install --proxy=http://proxy-dmz.intel.com:911 'toml>=0.10' 'meson>=0.55'

RUN pip3 install -U six     

RUN adduser intel
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo 'Acquire::http::proxy "http://proxy-dmz.intel.com:911/"; Acquire::https::proxy "http://proxy-dmz.intel.com:912/"; Acquire::ftp::proxy "ftp://proxy-dmz.intel.com:911/";' >> /etc/yum.conf

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

