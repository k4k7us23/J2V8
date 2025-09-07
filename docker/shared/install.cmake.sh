echo "Preparing CMake..."
curl https://github.com/Kitware/CMake/releases/download/v3.22.3/cmake-3.22.3-linux-x86_64.sh -O -L
mkdir /opt/cmake
chmod +x cmake-3.22.3-Linux-x86_64.sh
./cmake-3.22.3-Linux-x86_64.sh --prefix=/opt/cmake --skip-license
rm -rf cmake-3.22.3-Linux-x86_64.sh
