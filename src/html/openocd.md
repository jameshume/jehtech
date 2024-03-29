From the website:

> The Open On-Chip Debugger (OpenOCD) aims to provide debugging, in-system programming and boundary-scan testing for
> embedded target devices.
>
> It does so with the assistance of a debug adapter, which is a small hardware module which helps provide the right kind
> of electrical signaling to the target being debugged. 

## References
* [OpenOCD and STLink](https://pfeerick.github.io/InfiniTime/doc/openOCD.html)
* [STM32 Debugging using OpenOCD, GDB...](https://elrobotista.com/en/posts/stm32-debug-linux/)

## Install
Clone from Github and compile from source works out of the box. As part of the configuration enable STLink
compatibility if using with any of the STM ARM Cortex chips.

```bash
TEMP_DIR=/tmp
git clone https://git.code.sf.net/p/openocd/code "${TEMP_DIR}/openocd-code"
cd "${TEMP_DIR}/openocd-code" && ./bootstrap && ./configure --enable-stlink && make -j 4 && make install
```

## Use
Use one config file, named `openocd.cfg` to let your OCD server know about the adaptor being used and board etc.

You should use configuration files provided by OEMs and the like found in `/usr/local/share/openocd/scripts`.

* `/usr/local/share/openocd/scripts/interface/...` - contains a number of `.cfg` files, one for each debug adaptor.
* `/usr/local/share/openocd/scripts/board/...` - contains a number of `.cfg` files, one for each board.
* `/usr/local/share/openocd/scripts/target/...` - contains a number of `.cfg` files, one for each target.

The board config files for boards with a single MCU will normally contain target config, so if one is available you
shouldn't need the target config.

For example, for the STM Nucleo ... the following is sufficient:

```
source [find interface/stlink.cfg]
source [find board/st_nucleo_f0.cfg]
```

When using with GDB one can specify extra options such as shown below [[GDB Configuration]](https://openocd.org/doc/html/Server-Configuration.html#gdbconfiguration):

```
source [find interface/stlink.cfg]

gdb_flash_program enable
gdb_breakpoint_override hard

source [find board/st_nucleo_f0.cfg]
```

Then if using GDB, launch your GDB and type:

```
target extended-remote:3333
```

You can also get GDB to start OpenOCD itself [[GDB and OpenOCD]](https://openocd.org/doc/html/GDB-and-OpenOCD.html#GDB-and-OpenOCD):

```
target extended-remote | openocd -f openocd.cfg -c "gdb_port pipe; log_output openocd.log"
```

## OpenOCD and RTT
RTT is a great alternative to semihosting on ARM. It is way less intrusive and much faster.

Easy when you have a SEGGER debug probe and can just use their OZONE debugger. But if you have
neither OpenOCD has good support!

Just install `expect` and `moreutils` (to get the `ts` command to timestamp output) and create the
following two scripts:

The main script is:

```
#!/usr/bin/expect
# If expect not installed then run `sudo apt-get install -y expect`
# If moreutils not installed then run `sudo apt-get install -y moreutils`

# CLion starts OpenOCD with a telnet port of 4444. So need to `telnet 127.0.0.1 4444` and then run these commands.
spawn telnet 127.0.0.1 4444

# Configure RTT to search for the control block from the start of RAM, with a length of 12K
expect > {send "rtt setup 0x20000000 0x4000 \"SEGGER RTT\"\n"}

# Start
expect > {send "rtt start\n"}

# Kill any previous server instance
expect > {send "rtt server stop 19021\n"}

# Setup a server that will send the RTT commands as raw text over a TCP socket. When the client connects it will
# send the string "Welcome". This, in combination with port 19021, allows the JLinkRTTClient to be used, although
# a simple telnet session would suffice.
expect > {send "rtt server start 19021 0  \"Welcome\"\n"}
expect "Listening on port 19021 for rtt connections"

trap {
  send_user "\n\nCTRL-C pressed. Stopping RTT server and exiting\n"
  send "rtt server stop 19021\n"
  exit
} SIGINT

# Exit
expect > {send "exit\n"}

# Spawn a Telnet session to get the RTT debug output!
spawn ./openocd_telnet_rtt.sh
set timeout -1
expect "some string that wont occur so we wait forever" {send "exit\n"}
```

And a little helper that will timestamp telnet output and is spawnable from `expect`,
called `openocd_telnet_rtt.sh`:

```
telnet 127.0.0.1 19021 | ts '[%Y-%m-%d %H:%M:%S]'
```

Then execute the first script and you have an RTT debug feed. Hooray.
