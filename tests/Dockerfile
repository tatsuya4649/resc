# This Dockerfile is for test remote host.
FROM ubuntu:latest

ENV TZ=Asia/Tokyo

RUN apt update
RUN apt install -y tzdata
RUN apt install -y vim
RUN apt install -y python3-pip
RUN apt install -y openssh-server

RUN mkdir /run/sshd
RUN useradd test_resc

RUN echo "root:test_resc" | chpasswd root

RUN mkdir /root/.ssh
COPY test_data/test_resc.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication/PasswordAuthentication/' /etc/ssh/sshd_config

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
