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

```bash
telnet 127.0.0.1 19021 | ts '[%Y-%m-%d %H:%M:%S]'
```

Then execute the first script and you have an RTT debug feed. Hooray.

## OpenOCD And Multiple STLink Devices
Follow the method found [here](https://stackoverflow.com/a/48215590):

```bash
lsusb -vvv
```

The output will give something like:

```
Bus 001 Device 003: ID 0483:374e STMicroelectronics STLINK-V3
Device Descriptor:     
  bLength                18 
  bDescriptorType         1 
  bcdUSB               2.00 
  bDeviceClass          239 Miscellaneous Device
  bDeviceSubClass         2
  bDeviceProtocol         1 Interface Association
  bMaxPacketSize0        64 
  idVendor           0x0483 STMicroelectronics
  idProduct          0x374e STLINK-V3
  bcdDevice            1.00 
  iManufacturer           1 STMicroelectronics
  iProduct                2 STLINK-V3
  iSerial                 3 123456789012345678901234
  bNumConfigurations      1
  Configuration Descriptor:
    ...
    ...
```

Just take the `iSerial` string and add it to your config as:

```
hla_serial 123456789012345678901234
```


## Connect DDD to OpenOCD Debug Server, Debug ARM Target From x86 Linux Host

```bash
ddd --debugger "/opt/gcc-arm-none-eabi/bin/arm-none-eabi-gdb" --gdb --eval-command="target extended-remote localhost:3333" <path to ELF file>
```

## Example Memory Test Script

```
# Connect to the target
source [find interface/.. your interface here ...]
source [find target/.. your target here..]

# Start OpenOCD server
init

# Halt the CPU
reset halt

# Set SRAM boundaries etc
set start_address  .. your SRAM start address here ..
set end_address    .. your SRAM end address here ..
set mismatch_count 0
set patterns { 0x00 0xFF 0xAA 0x55 }

for {set pattern_idx 0} {$pattern_idx < [llength $patterns]} {incr pattern_idx} {
    set curr_pattern [lindex $patterns $pattern_idx]

    # Zero out RAM in a loop
    puts "Writing pattern $curr_pattern to SRAM..."
    for {set address $start_address} {$address < $end_address} {incr address} {
        write_memory $address 8 $curr_pattern
    }
    puts "DONE"

    puts "Checking SRAM..."
    # Check if it is all zero
    for {set address $start_address} {$address < $end_address} {incr address} {
        # Read memory contents
        set memory_content [read_memory $address 8 1]
        # Check if content is not zero
        if {$memory_content != $curr_pattern} {
            incr mismatch_count
            puts "Mismatch at address $address, value: $memory_content, expected $curr_pattern"
        }
    }
    puts "DONE"
}

# Resume CPU execution
resume

# Exit OpenOCD
shutdown
```

## Scriptlets

### Erase a flash sector

```bash
openocd -f interface/stlink.cfg -f target/stm32f3x.cfg -c "init" -c "reset halt"  -c "flash erase_sector 0 0 last" -c "shutdown"
```



## Command Cheat Sheet

* Target control:
    * `reset halt` - Perform as hard a reset as possible and immediately halt the target
    * `reset init` - Perform as hard a reset as possible, immediately halt the target, and execute the reset-init 
script
* Memory R/W
    * `read_memory <address> <width> <count>`, e.g. `read_memory 0x20000000 32 2`
    * `write_memory <address> <width> <data>`, e.g. `write_memory 0x20000000 32 {0xdeadbeef 0x00230500}`
    * Dump Memory To File
        * `dump_image <filename> <address> <length>`
* Registers    
    * `get_reg {pc sp}`
* Flash
    * `program filename.elf verify reset exit`
    * `program filename.bin verify reset exit 0x08000000`
    * `flash erase <bank num> <first> <last>`, e.g., `flash erase_sector 0 0 last` - erase all of flash
    * `flash md[whb] <addr> [<count>]`
    * `flash fill[dwhb] <addr> <value> <length>`
    * `flash info <bank num>`

## Flash Programming Notes
To program flash on STM devices, generally OpenOCD writes a program to flash (which is why `WORKAREASIZE` is important - this is the amount of RAM that can be used for this program). This program is then used to write to flash. If this fails, it is possible to fall back to a host-controlled halfword by halfword access. For F1's, for example, see `stm32x_write_block` in `src/flash/nor/stm32f1x.c` of OpenOCD source.

To find the algorithm used for target controlled flashing of the device see `stm32x_write_block_async`. It loads the algorithm into
a buffer called `stm32x_flash_write_code` in that function:

```cpp
static const uint8_t stm32x_flash_write_code[] = {
    #include "../../../contrib/loaders/flash/stm32/stm32f1x.inc"
};
```

So thats for F1's. The algorithm is, of course, different, for different STM targets, although its not 1 to 1, i.e. one algorithm could cover more than one STM device family.

Currently I'm interested in the STMF401x family. What algorithm does that use? To get a clue one can look in the config file for that
family, `stm32f4x.cfg`. In it the following lines can be seen:

```
set _FLASHNAME $_CHIPNAME.flash
flash bank $_FLASHNAME stm32f2x 0 0 0 0 $_TARGETNAME
flash bank $_CHIPNAME.otp stm32f2x 0x1fff7800 0 0 0 $_TARGETNAME
```

The `flash bank` command is `flash bank name driver base size chip_width bus_width target [driver_options]`. Thus we can see that the driver is the STM32F2x device driver so we can get the algorithm for that from `contrib/loaders/flash/stm32/stm32f2x.inc`.

## Debug GDB To OpenOCD
In `.gdbinit` file:

```bash
echo \n\n-------------------------------------------------------------------------------\n\n
echo Enabling GDB logging for GDB client and server. See `gdb.txt` and `gdb-remote-debug.txt`.
set remotelogfile gdb-remote-debug.txt
set logging debugredirect on
set logging overwrite on
set logging enabled on
set debug xml on
echo \n-------------------------------------------------------------------------------\n\n
```

To let GDB load this file, you must add its directory to the safe loads list, which can
be done by adding a `.gitinit` file to you home directory:


```
add-auto-load-safe-path /path/to/script
```
