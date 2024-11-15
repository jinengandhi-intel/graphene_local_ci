FROM alpine:3.18

RUN apk add doas sudo; \
    adduser intel -SG wheel -h /intel -g "intel Jenkins" -u 1000; \
    echo 'permit nopass intel as root' >> /etc/doas.d/doas.conf

RUN echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN apk update && \
    apk add automake \
    autoconf \
    avahi-tools \
    bash \
    bc \
    bison \
    binutils-dev \
    bsd-compat-headers \
    build-base \
    busybox \
    cargo \
    cmake \
    coreutils \
    curl \
    elfutils-dev \
    findutils \
    flex \
    gawk \
    gdb \
    git \
    glib-static \
    go \
    grep \
    gettext \
    openjdk11 \
    jq \
    less \
    libmemcached \
    libunwind \
    linux-headers \
    libevent \
    libevent-dev \
    libjpeg-turbo \
    libx11-dev \
    libxxf86vm \
    libxtst \
    libxfixes \
    libxrender-dev \
    lsof \
    'meson<1.2' \
    make \
    musl-dev \
    nasm \
    ncurses-dev \
    ncurses-libs \
    net-tools \
    ninja-build \
    nodejs \
    openssl \
    openssl-dev \
    protobuf-dev \
    protobuf-c-dev \
    patch \
    pkgconf \
    protobuf-c-compiler \
    python3 \
    python3-dev \
    py3-click \
    py3-cryptography \
    py3-elftools \
    py3-jinja2 \
    py3-lxml \
    py3-numpy \
    py3-pip \
    py3-protobuf \
    py3-pytest \
    py3-setuptools \
    py3-scipy \
    py3-tomli \
    py3-tomli-w \
    py3-voluptuous \
    R \
    samurai \
    strace \
    sqlite \
    vim  \
    texinfo \
    wget \
    unzip \
    zip \
    zlib-dev

# Install wrk2 benchmark. This benchmark is used in `benchmark-http.sh`.
RUN git clone https://github.com/giltene/wrk2.git \
    && cd wrk2 \
    && git checkout 44a94c17d8e6a0bac8559b53da76848e430cb7a7 \
    && make \
    && cp wrk /usr/local/bin \
    && cd .. \
    && rm -rf wrk2

# Make sure /intel can be written by intel
RUN chown 1000 /intel

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
CMD ["sh"]