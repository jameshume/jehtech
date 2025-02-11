* [Building QEMU for specific targets](https://stackoverflow.com/a/26672463)
    * E.g., `./configure --target-list=arm-softmmu`. I only want to support ARM emulation.
    * On my Ubuntu 18 VM I did:
      ```bash
      sudo apt-get install -y ninja-build libglib2.0-dev libpixman-1-dev
      git clone git://git.qemu-project.org/qemu.git
      cd qemu
      git submodule init
      git submodule update --recursive
      git submodule status --recursive
      git checkout stable-6.1
      mkdir build
      cd build
      ../configure --target-list=arm-softmmu --prefix=/opt/qemu-6.1.0/
      make -s$(nsproc)
      sudo make install
      ```

* [Adding a custom ARM platform to QEMU 5.2.0](http://souktha.github.io/software/qemu-port/)
* [Embedded Programming with the GNU Toolchain](http://www.bravegnu.org/gnu-eprog/)
* [Visual Studio Code for C/C++ with ARM Cortex-M: Part 4 – Debug](https://mcuoneclipse.com/2021/05/09/visual-studio-code-for-c-c-with-arm-cortex-m-part-4/)


