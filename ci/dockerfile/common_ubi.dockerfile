ARG BUILD_OS

FROM redhat/${BUILD_OS}

ARG BUILD_OS

RUN echo 'proxy=http://proxy-dmz.intel.com:911' >> /etc/yum.conf

RUN dnf distro-sync -y && dnf install 'dnf-command(config-manager)' -y

COPY redhat.repo /etc/yum.repos.d/redhat.repo

COPY redhat-uep.pem /etc/rhsm/ca/redhat-uep.pem

COPY redhat-uep.pem /etc/rhsm-host/ca/redhat-uep.pem

COPY entitlement /etc/pki/entitlement

RUN sed -i 's/enabled = 1/enabled = 0/' /etc/yum.repos.d/redhat.repo

RUN if [[ "$BUILD_OS" == "ubi8" ]]; then \
        rm -rf /etc/rhsm-host \
        && subscription-manager repos --enable rhel-8-for-x86_64-appstream-rpms \
        && subscription-manager repos --enable rhel-8-for-x86_64-baseos-rpms \
        && subscription-manager repos --enable codeready-builder-for-rhel-8-x86_64-rpms \
        && dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
    elif [[ "$BUILD_OS" == "ubi9" ]]; then \
        cp -f /etc/rhsm/rhsm.conf /etc/rhsm-host/rhsm.conf \
        && sed -i 's/%(ca_cert_dir)s/\/etc\/rhsm\/ca\//' /etc/yum.repos.d/redhat.repo \
        && dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm; \
    fi

# Add steps here to set up dependencies
RUN yum update -y && yum install -y \
    cmake \
    diffutils \
    gcc\
    git \
    make \
    python3-pip \
    python3-setuptools \
    python3-pytest \
    sshpass \
    sudo \
    wget \
    yum-utils

RUN python3 -m pip install -U 'meson>=0.56,<0.57'

RUN yum-config-manager --add-repo https://packages.gramineproject.io/rpm/gramine.repo 

RUN yum update -y

# Add the user UID:1000, GID:1000, home at /intel
RUN groupadd -r intel -g 1000 && useradd -u 1000 -r -g intel -G wheel -m -d /intel -c "intel Jenkins" intel && \
    chmod 777 /intel

# Make sure /intel can be written by intel
RUN chown 1000 /intel

RUN echo 'intel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN echo -e 'http_proxy="http://proxy-dmz.intel.com:911/"\nhttps_proxy="http://proxy-dmz.intel.com:912/"' >> /etc/environment

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
