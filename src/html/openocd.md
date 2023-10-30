## Install
Clone from Github and compile from source works out of the box. As part of the configuration enable STLink
compatibility if using with any of the STM ARM Cortex chips.

```bash
TEMP_DIR=/tmp
git clone https://git.code.sf.net/p/openocd/code "${TEMP_DIR}/openocd-code"
cd "${TEMP_DIR}/openocd-code" && ./bootstrap && ./configure --enable-stlink && make -j 4 && make install
```
## Run For Nucleo

```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg
```

The various interface and target files are found at these locations:

* `/usr/local/share/openocd/scripts/interface/stlink.cfg`
* `usr/local/share/openocd/scripts/target/stm32f4x.cfg`

