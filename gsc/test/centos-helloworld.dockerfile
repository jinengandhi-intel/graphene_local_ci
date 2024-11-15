ARG BUILD_OS

From $BUILD_OS

ARG BUILD_OS

RUN if [ "$BUILD_OS" != "redhat/ubi9-minimal:9.4" ]; then \
    yum update -y; \
    fi

CMD ["echo", "\"Hello World! Let's check escaped symbols: < & > \""]
