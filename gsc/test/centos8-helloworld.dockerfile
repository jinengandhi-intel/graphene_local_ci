ARG BUILD_OS

From $BUILD_OS

ARG BUILD_OS

RUN if [ "$BUILD_OS" = "centos:8" ]; then \
    sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Linux-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-Linux-* && \
    echo 'proxy=http://proxy-dmz.intel.com:911' >> /etc/yum.conf; \
    fi

RUN if [ "$BUILD_OS" = "redhat/ubi8-minimal:8.8" ]; then \
    microdnf update -y; \
    else \
    yum update -y; \
    fi

CMD ["echo", "\"Hello World! Let's check escaped symbols: < & > \""]