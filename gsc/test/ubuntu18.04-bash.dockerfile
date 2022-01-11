From ubuntu:18.04

RUN apt-get update

ENV LD_LIBRARY_PATH = "${LD_LIBRARY_PATH}:/usr/lib/x86_64-linux-gnu"

CMD ["bash"]
