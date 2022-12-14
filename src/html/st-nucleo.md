## Intro
* [ST Nucleo F401RE](https://www.st.com/resource/en/datasheet/stm32f401re.pdf)
    * 32-bit ARM Cortex M4
* [ST Nucleo L552ZE](https://www.st.com/resource/en/datasheet/stm32l552ze.pdf)
    * 32-bit ARM Cortex M33
* [Awesome example code](https://github.com/prtzl/Embedded_videos) by some chap called Matej Blagsic.

## Debugging
* The STM32Cube IDE uses the STLink GDB server, but I cannot find this as an independent package to install, without installing all of the STM32Cube IDE.
    * Note the "ST-link server" and "ST-link DGB server" are *not* the same thing! [[Ref]](https://stackoverflow.com/a/71937416).
* For non-STM32Cube IDEs most guides suggest using OpenOCD.

    > The Open On-Chip Debugger (OpenOCD) aims to provide debugging, in-system programming and boundary-scan testing for embedded target devices.
    >
    > It does so with the assistance of a debug adapter, which is a small hardware module which helps provide the right kind of electrical signaling to the target being debugged. 

* The Nucleo boards have debug adaptor module on-board (ST-LINK/V2-1 debugger): well, really its an STM32F103C8, which is a very small ARM Cortex-M3 MCU that acts as the debug adaptor. The firmware can be upgraded using the [app found here](https://www.st.com/en/development-tools/stsw-link007.html).
