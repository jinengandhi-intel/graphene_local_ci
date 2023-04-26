From quay.io/centos/centos:stream9

RUN dnf distro-sync -y && dnf install 'dnf-command(config-manager)' -y

#RUN dnf copr enable -y ngompa/musl-libc
RUN dnf config-manager --set-enabled -y crb && \
    dnf install -y yum-utils && \
    dnf install -y epel-release && \
    dnf install -y --allowerasing \
        libunwind \
        ncurses-devel \
        bc \
        bison \
        flex \
        make \
        elfutils-libelf-devel \
        openssl-devel \
        rpm-build \
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
        # musl-devel \
        # musl-gcc \
        nasm \
        nc \
        ncurses-devel \
        ncurses-libs \
        net-tools \
        ninja-build \
        nodejs \
        # nss_nis \
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

RUN dnf clean all && rm -r /var/cache/dnf && dnf upgrade -y && dnf update -y

# Install wrk2 benchmark. This benchmark is used in `benchmark-http.sh`.
RUN git clone https://github.com/giltene/wrk2.git \
    && cd wrk2 \
    && git checkout 44a94c17d8e6a0bac8559b53da76848e430cb7a7 \
    && make \
    && cp wrk /usr/local/bin \
    && cd .. \
    && rm -rf wrk2

RUN python3 -m pip install -U \
    six \
    torchvision \
    pillow \
    'tomli>=1.1.0' \
    'tomli-w>=0.4.0' \
    'meson>=0.56,<0.57'

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