ARG BUILD_OS

From $BUILD_OS

ARG BUILD_OS

RUN zypper -n update;

CMD ["bash"]
