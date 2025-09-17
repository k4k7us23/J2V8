echo no | $ANDROID_HOME/tools/android create avd -f -n test -k "system-images;android-35;google_apis_ps16k;arm64-v8a"
echo no | $ANDROID_HOME/emulator/emulator -avd test -noaudio -no-window -gpu off -verbose -qemu -usbdevice tablet -vnc :0
