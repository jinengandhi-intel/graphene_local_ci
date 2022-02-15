From centos:8

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-Linux-* &&\
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-Linux-*

RUN echo 'proxy=http://proxy-dmz.intel.com:911' >> /etc/yum.conf

RUN yum update -y

CMD ["bash"]

