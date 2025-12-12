ARG sys_image=ubuntu:20.04

FROM $sys_image

ARG MIRROR=ftp.uni-stuttgart.de/ubuntu
RUN sed -i "s|archive.ubuntu.com|${MIRROR}|g" /etc/apt/sources.list && \
    sed -i "s|security.ubuntu.com|${MIRROR}|g" /etc/apt/sources.list

# default values
ARG vendor=debian
ARG target_os=linux
ARG target_cpu=x64

# Update depedency of V8
RUN apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --upgrade -qq -y --no-install-recommends \
    git \
    curl \
    wget \
    build-essential \
    software-properties-common \
    patchelf \
    sudo \
    zip \
    unzip \
    gcc gcc-multilib \
    g++ g++-multilib \
    execstack \
    python3 \
    python \
    python3-distutils \ 
    python3-testresources \
    python3-pip

RUN mkdir -p /v8build
WORKDIR /v8build


# DEPOT TOOLS install
RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
ENV PATH /v8build/depot_tools:"$PATH"
RUN echo $PATH

ENV target_os ${target_os}

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --upgrade -qq -y --no-install-recommends \
    file keyboard-configuration

WORKDIR /v8build

RUN fetch v8 && \
    cd /v8build/v8 && \
    git checkout 13.8.258.19 && \
    cd /v8build && \
    echo "target_os= ['${target_os}']" >> .gclient && \
    gclient sync

ENV target_cpu ${target_cpu}
ENV build_platform ${target_cpu}.release
ENV path_to_args ${target_os}-${target_cpu}/args.gn

WORKDIR /v8build/v8
RUN apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --upgrade -qq -y --no-install-recommends \
    pkg-config

COPY patches/ /patches/

RUN cd /v8build/v8 && \
    git apply /patches/*.patch

RUN ./tools/dev/v8gen.py ${build_platform} -vv

RUN rm out.gn/${build_platform}/args.gn
COPY ./${path_to_args} out.gn/${build_platform}/args.gn
RUN ls -al out.gn/${build_platform}/
RUN cat out.gn/${build_platform}/args.gn
RUN touch out.gn/${build_platform}/args.gn

RUN apt-get -qq update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --upgrade -qq -y --no-install-recommends \
    python3.9 && \
    ln -sf /usr/bin/python3.9 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.9 /usr/bin/python

# Build the V8 monolithic static liblary
RUN ninja -C out.gn/${build_platform} -t clean
RUN ninja -C out.gn/${build_platform} v8_monolith
