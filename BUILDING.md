# Getting started / building from source

**Important:** this fork supports only android version of J2V8

#### Requirements

0. Linux with x86_64 architecture
1. Python 2
2. Docker 


#### Build

1. run `source j2v8-cli.sh`
2. build j2v8 for each android architecture using `build -i` command. Select each android architecture, one by one. Leave "Override build-steps ?" empty.  
3. Find native \*.so that were built in step inside `cmake.out` directory
4. Replace old libraries with new once inside src/main/jniLibs/
5. Run `./gradlew assemble`

Aar built for all android architectures will be located in build/outputs/aar/j2v8-release.aar
