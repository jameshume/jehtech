## GPIB / IEEE-448, USBTMC, VISA, SCPI... What Does It All Mean?

### References
* [GPIB Tutorial, NI](http://lmu.web.psi.ch/docu/manuals/software_manuals/GPIB/GPIB_tutorial.pdf)
* [Making Sense of Test and Measurement Protocols](https://tomverbeure.github.io/2020/06/07/Making-Sense-of-Test-and-Measurement-Protocols.html)
* [GPIB 101 - A Tutorial About The GPIB Bus](https://www.icselect.com/pdfs/ab48_11%20GPIB-101.pdf)


### GPIB / IEEE-448.x

GPIB is an old standard for *test and measurement equipment* interfaces, which was standardised by the IEEE as
IEEE-448.1 and IEEE-448.2.

IEEE-448.1 is a physical layer specification that sought to make common the physical interfaces between test and
measurement devices so that users could more easily communicate with different bits ok kit.

IEEE-448.2 is a command specification whose goal was to make the control of different instruments more portable. So,
for example, if you had programmable power supply from vendor A and switched to an equally capable supply from vendor B,
you should be able to port your software - there should be less difference in command structures and data formats between
IEEE-488.2 compliant devices.

<blockquote>
<p>
The GPIB concept expressed in IEEE-STD 488 made it easy to
physically interconnect instruments but it did not make it easy for
a programmer to talk to each instrument. Some companies terminated their instrument responses with a carriage return, others used
a carriage return-linefeed sequence, or just a linefeed. Number
systems, command names and coding depended upon the instrument manufacturer. In an attempt to standardize the instrument
formats, Tektronix proposed a set of standard formats in 1985. This
was the basis for the IEEE-STD 488.2 standard that was adopted
in 1987. At the same time, the original IEEE-488 Standard was
renumbered to 488.1.
</p>
<p>...</p>
<p>The required common commands simplified instrument programming
by giving the programmer a minimal set of commands that he can
count on being recognized by each 488.2 instrument</p>
<footer>-- [GPIB 101 - A Tutorial About The GPIB Bus](https://www.icselect.com/pdfs/ab48_11%20GPIB-101.pdf)</footer>
</blockquote>

IEEE-488.2 defines the following mandator common commands:

| Mnemonic | Group            | Description                       |
|----------|------------------|-----------------------------------|
| *CLS     | Status and Event | Clear status                      |
| *ESE     | Status and Event | Event status enable               |
| *ESE?    | Status and Event | Event status enable query         |
| *ESR?    | Status and Event | Event status register query       |
| *IDN?    | System Data      | Identification query              |
| *OPC     | Synchronization  | Operation complete                |
| *OPC?    | Synchronization  | Operation complete query          |
| *RST     | Internal         | Operations Reset                  |
| *SRE     | Status and Event | Service request enable            |
| *SRE?    | Status and Event | Service request enable query      |
| *STB?    | Status and Event | Read status byte query            |
| *TST?    | Internal         | Operations Self-test query        |
| *WAI     | Synchronization  | Wait to complete                  |

For example, when I send the N6705B the <code>*IDN?</code> it replies with the string <code>TODO</code>.

IEEE-488.2 also defines a status reporting model via the Standard Event Status Register (use <code>*ESR></code>) and
Status Byte Register (use <code>*STB?</code>).

<p></p>
<blockquote>
<p>
IEEE 488.2 defines precisely the format of commands sent to instruments and the format and coding of responses sent by instruments
</p>
<footer>-- [GPIB Tutorial, NI](http://lmu.web.psi.ch/docu/manuals/software_manuals/GPIB/GPIB_tutorial.pdf)</footer>
</blockquote>
<p></p>

### SCPI - Standard Commands for Programmable Instruments
A level above the transport layer.

<p></p>
<blockquote>
<p>
SCPI simplifies the programming task by defining a single comprehensive command set for programmable instrumentation, regardless of type or manufacturer. 
</p>
<p>...</p>
<p>SCPI built on the IEEE 488.2 standard and defined device-specific commands that standardize programming instruments.
SCPI systems are much easier to program and maintain. </p>
<footer>-- [GPIB Tutoria](http://lmu.web.psi.ch/docu/manuals/software_manuals/GPIB/GPIB_tutorial.pdf)</footer>
</blockquote>
<p></p>

### VISA - Virtual Instrument Software Architecture
First off, a virtual instrument is one that displays a front panel GUI or image on a computer screen, rather than
presenting its own. But, many VISA compliant instruments will also have their own screen.

VISA is a big wrapper around a lot of the different protocols/transport methods that can be used to talk to a device, be it GPIB, USBTMC,
VXI, Ethernet, serial etc etc. It hides all this complexity so that it becomes easier to connect to devices and help interoperability.

The IVI foundation is responsible for the VISA API.

PyVISA is an open source implementation of the VISA standard. The other option is the NI libvisa library.

### USBTMC - USBTest and Measurement Class
USBTMC stands for USBTest and Measurement Class and allows GPIB-style communication over USB using USBTMC-compliant VISA layers.

The [standard is freely available](https://www.usb.org/sites/default/files/USBTMC_1_006a.zip).

Linux includes an usbtmc kernel module, so you should just be able to plug in a usbtmc device straight into a linux
box and use it.

For example, a quick and dirty way to verify you can talk to a device is:

```
echo "*IDN?" > /dev/usbtmc0
cat /dev/usbtmc0
```

## Some PyVISA Examples

For example, to automatically find my N6705B:

```python
import pyvisa

rm = pyvisa.ResourceManager("@py")

# Search all connected devices for the N6705B
n6705b_dev = None
for device_string in rm.list_resources():     
    tmp_dev = rm.open_resource(device_string)
    device_idn = tmp_dev.query('*IDN?')
    if "N6705B" in device_idn:
        print(f"Using N6705B device {device_string}")
        n6705b_dev = tmp_dev
        break
    tmp_dev.close()

if n6705b_dev is None:
    print("Could not find an N6705B device!")
    print("Devices found where:", file=outfile)
    for device_string in resman.list_resources():     
        n6705b_dev = resman.open_resource(device_string)
        device_idn = n6705b_dev.query('*IDN?')
        print(f"   - {device_string} -- {device_idn}", file=outfile)
        n6705b_dev.close()

rm.close()
```


## Using the NI Backend

### Installing The NI's `libvisa`
You have to install the NI drivers, which on Ubuntu is pretty easy:
```
apt-get install -y ./ni-ubuntu1804firstlook-drivers-stream.deb && \
apt-get update && \
apt-get install -y --no-install-recommends libvisa-dev
```

### Making Sure Your Device Is Accessible
Once the drivers are installed, accessing the device is a bit of a pain, however:

In a terminal type:

```
$ usb-devices
```

I'm using an N6705B. Part of the output will look something like this, if the device is connected:

```
T:  Bus=01 Lev=01 Prnt=01 Port=00 Cnt=01 Dev#=  8 Spd=480 MxCh= 0
D:  Ver= 2.00 Cls=00(>ifc ) Sub=00 Prot=00 MxPS=64 #Cfgs=  1
P:  Vendor=0957 ProdID=0f07 Rev=01.00
S:  Manufacturer=Agilent Technologies
S:  Product=N6705B
S:  SerialNumber=MY53000921
C:  #Ifs= 1 Cfg#= 1 Atr=c0 MxPwr=0mA
I:  If#= 0 Alt= 0 #EPs= 3 Cls=fe(app. ) Sub=03 Prot=01 Driver=usbtmc
E:  Ad=02(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=86(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=88(I) Atr=03(Int.) MxPS=   2 Ivl=125us

```

The `Bus` and `Lev` will vary. If you see `Driver=usbtmc` it means that the <em>linux USBTMC kernel
driver</em> has claimed the device. This means that the `libvisa` be not be able to. You can see this
by doing an `strace` of `./test_nivisa`, where you will see something similar to the following:

```
stat("/dev/bus/usb/001/001", {st_mode=S_IFCHR|0664, st_rdev=makedev(0xbd, 0), ...}) = 0
openat(AT_FDCWD, "/dev/bus/usb/001/001", O_RDWR) = 5
lseek(5, 0, SEEK_SET)                   = 0
read(5, "\22\1\0\2\t\0\1@k\35\2\0\31\5\3\2\1\1", 18) = 18
lseek(5, 18, SEEK_SET)                  = 18
read(5, "\t\2\31\0\1\1\0\340\0\t", 10)  = 10
lseek(5, 18, SEEK_SET)                  = 18
read(5, "\t\2\31\0\1\1\0\340\0\t\4\0\0\1\t\0\0\0\7\5\201\3\4\0\f", 25) = 25
ioctl(5, USBDEVFS_CONTROL, 0x7ffca43b9a40) = 4
ioctl(5, USBDEVFS_CONTROL, 0x7ffca43b9a10) = 26
ioctl(5, USBDEVFS_CLAIMINTERFACE, 0x7ffca43b9cac) = -1 EBUSY (Device or resource busy)
ioctl(5, USBDEVFS_GETDRIVER, 0x7ffca43b9ba0) = 0
```

One can see that the Agilent device is busy when `libvisa` tries to open it. This is why
it cannot find the device.

To allow it access to the device the USBTMC kernel driver module must be unloaded. To do this
type:

```
sudo rmmod usbtmc
```

The next problem you will face is that `/dev/bus/usb/001/001` is owned by `root` and is in the
group `root`. This isn't great, so do a `sudo chgroup plugdev /dev/bus/usb/001/001`. 

If you wanted to do this every time you ran a test setting up a udev rule would be preferable.

### Setting Up A udev Rule

You can use the `udevadm monitor` command to monitor udev events in real time. Simply run the command and plug in your
device. I am using an N6705B device...

```
$ sudo udevadm monitor
monitor will print the received events for:
UDEV - the event which udev sends out after rule processing
KERNEL - the kernel uevent

KERNEL[2958.347940] add      /devices/pci0000:00/0000:00:14.0/usb1/1-2 (usb)
KERNEL[2958.349495] add      /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0 (usb)
KERNEL[2958.355912] add      /class/usbmisc (class)
KERNEL[2958.355962] add      /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0/usbmisc/usbtmc0 (usbmisc)
KERNEL[2958.355990] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0 (usb)
KERNEL[2958.356653] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-2 (usb)
UDEV  [2958.357886] add      /class/usbmisc (class)
UDEV  [2958.376286] add      /devices/pci0000:00/0000:00:14.0/usb1/1-2 (usb)
UDEV  [2958.379804] add      /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0 (usb)
UDEV  [2958.381957] add      /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0/usbmisc/usbtmc0 (usbmisc)
UDEV  [2958.384157] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0 (usb)
UDEV  [2958.393828] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-2 (usb)
```

Once you have your device you can get more info on the device:

```
$ sudo udevadm info -a -n /dev/usbtmc0

Udevadm info starts with the device specified by the devpath and then
walks up the chain of parent devices. It prints for every device
found, all possible attributes in the udev rules key format.
A rule to match, can be composed by the attributes of the device
and the attributes from one single parent device.

  looking at device '/devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0/usbmisc/usbtmc0':
    KERNEL=="usbtmc0"
    SUBSYSTEM=="usbmisc"
    DRIVER==""
    ATTR{power/async}=="disabled"
    ATTR{power/control}=="auto"
    ATTR{power/runtime_active_kids}=="0"
    ATTR{power/runtime_active_time}=="0"
    ATTR{power/runtime_enabled}=="disabled"
    ATTR{power/runtime_status}=="unsupported"
    ATTR{power/runtime_suspended_time}=="0"
    ATTR{power/runtime_usage}=="0"

  looking at parent device '/devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.0':
    KERNELS=="1-2:1.0"
    SUBSYSTEMS=="usb"
    DRIVERS=="usbtmc"
    ATTRS{authorized}=="1"
    ATTRS{bAlternateSetting}==" 0"
    ATTRS{bInterfaceClass}=="fe"
    ATTRS{bInterfaceNumber}=="00"
    ATTRS{bInterfaceProtocol}=="01"
    ATTRS{bInterfaceSubClass}=="03"
    ATTRS{bNumEndpoints}=="03"
    ATTRS{device_capabilities}=="1"
    ATTRS{interface_capabilities}=="0"
    ATTRS{physical_location/dock}=="no"
    ATTRS{physical_location/horizontal_position}=="left"
    ATTRS{physical_location/lid}=="no"
    ATTRS{physical_location/panel}=="top"
    ATTRS{physical_location/vertical_position}=="upper"
    ATTRS{power/async}=="enabled"
    ATTRS{power/runtime_active_kids}=="0"
    ATTRS{power/runtime_enabled}=="disabled"
    ATTRS{power/runtime_status}=="unsupported"
    ATTRS{power/runtime_usage}=="0"
    ATTRS{supports_autosuspend}=="0"
    ATTRS{usb488_device_capabilities}=="15"
    ATTRS{usb488_interface_capabilities}=="7"

  looking at parent device '/devices/pci0000:00/0000:00:14.0/usb1/1-2':
    KERNELS=="1-2"
    SUBSYSTEMS=="usb"
    DRIVERS=="usb"
    ATTRS{authorized}=="1"
    ATTRS{avoid_reset_quirk}=="0"
    ATTRS{bConfigurationValue}=="1"
    ATTRS{bDeviceClass}=="00"
    ATTRS{bDeviceProtocol}=="00"
    ATTRS{bDeviceSubClass}=="00"
    ATTRS{bMaxPacketSize0}=="64"
    ATTRS{bMaxPower}=="0mA"
    ATTRS{bNumConfigurations}=="1"
    ATTRS{bNumInterfaces}==" 1"
    ATTRS{bcdDevice}=="0100"
    ATTRS{bmAttributes}=="c0"
    ATTRS{busnum}=="1"
    ATTRS{configuration}==""
    ATTRS{devnum}=="10"
    ATTRS{devpath}=="2"
    ATTRS{idProduct}=="0f07"
    ATTRS{idVendor}=="0957"
    ATTRS{ltm_capable}=="no"
    ATTRS{manufacturer}=="Agilent Technologies"
    ATTRS{maxchild}=="0"
```

You can then use this information to create a udev rule:

```
KERNEL=="usbtmc[0-9]", ATTRS{idVendor}=="0957", ATTRS{idProduct}=="0f07", GROUP="usbtmc", MODE="0660"
```


### Configure PyVISA To Use `libvisa.so`

Installing `libvisa-dev` on Ubuntu 22 I find the driver installed at `/usr/lib/x86_64-linux-gnu/libvisa.so`. So,
to make PyVISA use it:

```
rm = pyvisa.ResourceManager('/usr/lib/x86_64-linux-gnu/libvisa.so')
```

### Simple Example Using `libvisa.so` directly:

```c
// A silly little test program to list the resources found by NI's libvisa
// independently of PyVisa. Was used to debug NI libvisa not finding USBTMC
// devices.
//
// To compile and run:
//    gcc test_nivisa.c -lvisa -o test_nivisa && ./test_nivisa
#include "visa.h"
#include "visa_version.h"

#include <stdio.h>
#include <string.h>

int main()
{
    // Get VISA resource manager
    ViSession resource_manager;
    ViStatus  status;
    ViFindList find_list;
    ViUInt32 num_found;
    ViChar descr[VI_FIND_BUFLEN];
    ViChar errorString[256]; // From the docs: "The size of the desc parameter should be at least 256 bytes." [https://www.ni.com/docs/en-US/bundle/ni-visa/page/ni-visa/vistatusdesc.html]
    
    printf("You are using an libvisa v%u.%u.%u\n",
        (unsigned int)VI_VERSION_MAJOR(VI_SPEC_VERSION),
        (unsigned int)VI_VERSION_MINOR(VI_SPEC_VERSION),
        (unsigned int)VI_VERSION_SUBMINOR(VI_SPEC_VERSION));

    status = viOpenDefaultRM(&resource_manager);
    if (status != VI_SUCCESS) {
        printf("Could not open VISA resource manager.\n");
        return 1;
    }

    status = viFindRsrc(resource_manager, "?*", &find_list, &num_found, descr);
    if (status != VI_SUCCESS) {
#if VI_SPEC_VERSION >= 0x00500800UL
        viStatusDesc(resource_manager, status, errorString);
        printf("Could not find resources because '%s'\n", errorString);
#else
        // On Ubuntu 18 the install it would appear that libvisa does not support viStatusDesc()
        printf("Could not find resources\n");
#endif
        viClose(resource_manager);
        return 1;
    }

    printf("Found %s\n", descr);
    
    viClose(find_list);
    viClose(resource_manager);
    return 0;
}
```
