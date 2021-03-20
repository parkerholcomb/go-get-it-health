FROM amazonlinux:2.0.20210219.0
RUN yum install -y python3 && \
    yum install -y python3-pip && \
    yum install -y zip && \
    yum clean all
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install virtualenv