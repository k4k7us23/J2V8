ARG sys_image=ubuntu:20.04

FROM $sys_image

ARG MIRROR=ftp.uni-stuttgart.de/ubuntu
RUN sed -i "s|archive.ubuntu.com|${MIRROR}|g" /etc/apt/sources.list && \
    sed -i "s|security.ubuntu.com|${MIRROR}|g" /etc/apt/sources.list

RUN mkdir -p /temp/docker/shared/
WORKDIR /temp/docker/shared/

# NOTE: copy shared scripts and run them separately
# this helps when changing commands only in a single script,
# since it will not requrie rebuilding all docker image layers
# but just the ones that were affected

COPY ./shared/install.debian.packages.sh /temp/docker/shared
RUN ./install.debian.packages.sh

ENV ANDROID_HOME "/usr/local/android-sdk"

ENV NDK_VERSION "r28c"
ENV NDK_NAME "android-ndk-$NDK_VERSION-linux"
RUN echo "Preparing Android NDK..." && \
    mkdir -p /build && \
    cd /build && \
    curl -fSOL https://dl.google.com/android/repository/$NDK_NAME.zip && \
    unzip -qq $NDK_NAME.zip && \
    rm $NDK_NAME.zip

RUN echo "Preparing Android GCC-Toolchain..." && \
    mkdir -p /build && \
    cd /build && \
    git clone https://github.com/sjitech/android-gcc-toolchain
ENV NDK "/build/android-ndk-$NDK_VERSION"
ENV PATH "$PATH:/build/android-gcc-toolchain:$NDK"

ENV PATH "$PATH:$ANDROID_HOME/tools"
ENV PATH "$PATH:$ANDROID_HOME/platform-tools"
ENV PATH "$PATH:$ANDROID_HOME/tools/bin"
ENV PATH "$PATH:$ANDROID_HOME/cmdline-tools/bin"


RUN mkdir -p ${ANDROID_HOME} && \
    cd ${ANDROID_HOME} && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-13114758_latest.zip -O android_tools.zip && \
    unzip -qq android_tools.zip && \
    rm android_tools.zip


COPY ./shared/install.jdk.sh /temp/docker/shared
RUN ./install.jdk.sh
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME

COPY ./shared/install-android-dependencies.sh /temp/docker/shared
RUN ./install-android-dependencies.sh

COPY ./shared/install.cmake.sh /temp/docker/shared
RUN apt-get update \
  && apt-get -y install build-essential \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/* \
  && wget https://github.com/Kitware/CMake/releases/download/v3.22.3/cmake-3.22.3-Linux-x86_64.sh \
      -q -O /tmp/cmake-install.sh \
      && chmod u+x /tmp/cmake-install.sh \
      && mkdir /opt/cmake-3.22.3 \
      && /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake-3.22.3 \
      && rm /tmp/cmake-install.sh \
      && ln -s /opt/cmake-3.22.3/bin/* /usr/local/bin

COPY ./shared/install.gradle.sh /temp/docker/shared
RUN ./install.gradle.sh
ENV GRADLE_HOME "/opt/gradle-8.14.3"
ENV PATH "$PATH:$GRADLE_HOME/bin"

RUN mkdir -p /temp
COPY ./shared/build.gradle /temp
COPY ./android/AndroidManifest.xml /temp/src/main/AndroidManifest.xml
WORKDIR /temp
RUN cd /temp && gradle --dry-run

# Install the Android tools
RUN sdkmanager --sdk_root=$ANDROID_HOME emulator
RUN sdkmanager --sdk_root=$ANDROID_HOME platform-tools
RUN sdkmanager --sdk_root=$ANDROID_HOME "system-images;android-35;default;arm64-v8a"

# Required for Android ARM Emulator
RUN apt-get update && apt-get install -y libqt5widgets5
ENV QT_QPA_PLATFORM offscreen
ENV LD_LIBRARY_PATH ${ANDROID_HOME}/tools/lib64:${ANDROID_HOME}/emulator/lib64:${ANDROID_HOME}/emulator/lib64/qt/lib

ARG KEYSTORE
ARG KEYSTORE_PASSWORD

ENV KEYSTORE=$KEYSTORE
ENV KEYSTORE_PASSWORD=$KEYSTORE_PASSWORD

RUN mkdir ~/.gnupg

RUN if [ -n "$KEYSTORE" ]; then echo $KEYSTORE | base64 -d > my-private-key.asc; fi
RUN if [ -n "$KEYSTORE" -a -n "$KEYSTORE_PASSWORD" ]; then echo $KEYSTORE_PASSWORD | gpg --import --batch --yes --passphrase-fd 0 my-private-key.asc; fi

RUN cp -r ~/.gnupg /

EXPOSE 22
EXPOSE 5037
EXPOSE 5554
EXPOSE 5555
EXPOSE 5900

RUN apt-get -qq update && \
	DEBIAN_FRONTEND=noninteractive apt-get -qq install -y \
	python-is-python2

