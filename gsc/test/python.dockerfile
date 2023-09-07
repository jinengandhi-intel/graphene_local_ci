ARG BUILD_OS

FROM $BUILD_OS

ARG BUILD_OS

COPY test/setup.sh ./setup.sh

RUN chmod +x ./setup.sh
RUN /bin/bash -c './setup.sh'

CMD ["python3"]