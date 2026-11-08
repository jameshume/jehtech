## Links
* [BLE Advertising Benchmarks For Vendors](https://github.com/em-foundation/BlueJoule/blob/main/docs/ReadMore.md)

## The Basics

* Low power, low bandwidth application focus
* 2.4GHz ISM Band (Industrial Scientific Medical Band) (2400 MHz – 2483.5 MHz)
    * Channel bandwidth is 2Mhz
    * 40 RF channels
* Range 10-30 meters depending on the environment
* Optimised for low power
* Peak current under 15mA typically.
* v4 in 2010
* v4.2 in 2014
* v5 in 2016
* Operates over 40 RF channels
* Discovery occurs over 3 channels (quicker connection)

```
Bluetooth LE: 40 channels, spaced 2 MHz apart                 Frequency increases -->

     2402 MHz                           2426 MHz                                                                         2480 MHz
      |                                  |                                                                                |
      A  D  D  D  D  D  D  D  D  D  D  D  A  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  D  A
     37 00 01 02 03 04 05 06 07 08 09 10 38 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 39

     +-------------------------------+    +-------------------------------+    +-------------------------------+
     |         Wi-Fi channel 1       |    |         Wi-Fi channel 6       |    |         Wi-Fi channel 11      |
     |           2412 MHz            |    |           2437 MHz            |    |           2462 MHz            |
     +-------------------------------+    +-------------------------------+    +-------------------------------+
                         Wi-Fi band positions and widths are approximate.

     A = Primary advertising channel (37, 38, 39)
     D = Data channel (0-36)
```

### Device Types

* Bluetooth Smart - BLE only - single mode
* Bluetooth Smart Ready - BLE and bluetooth classic - dual mode
* Bluetooth - Classic only (BR - basic rate/EBR - enhanced basic rate)

### BLE architecture blocks

* Application - uses the host softeare to build use cases
* Host - manages how two or more devicesd commuinicater
    * Generic Access Profile
    * Generic Attributre Profile
    * Attribute Protocol | Security Manager
    * Logical Link Control and Adaption Protocol
    * -- HCI --
* Controller - a physical device that can transmit and receive radio signals.
    * -- HCI 00
    * Link Layer
    * PHysical Layer | Direct Test Mode
* Can have as a single chip solution or 2-bip solution with host on an MCU and Controller on separate RF chip.

```
                        ┌────────────────────────────────────────┐
                        │              Application               │
                        └────────────────────────────────────────┘
                        ┌────────────────────────────────────────┐
                        │                 Host                   │
                        ├──────────────┬─────────────────────────┤
Subprocedures for  ---->│     GATT     │    GAP                  │ <--- Interfaces directly with app
using ATT layer         │              |                         │      to handle device discovery and
                        ├──────────────┼──────────────┐          │      connection related services
Allow dev to expose --->│     ATT      │    SMP <-----|----------│----- Security Manage Protocol: defines
attributes to others    │              |              |          │      and provides methods for secure
                        ├──────────────┴──────────────┤          │      comms.
Data encapsulation ---->│           L2CAP             │          │
services to upper       |                             |          |
layers                  └─────────────────────────────┴──────────┘
                      - - - - Host Controller Interface (HCI) - - - -
                        ┌────────────────────────────────────────┐
                        │              Controller                │
                        ├────────────────────────────────────────┤
                        │         Link Layer (LL)                │
                        ├────────────────────────────────────────┤
                        │         Physical Layer (PHY)           │
                        └────────────────────────────────────────┘
```

## Layers
### Physical Layer (PHY)

* The radio hardware
* 2.4GHz ISM band
* Spectrum is segmented into 40 RF channels, each spearated by 2MHz
* 3/40 channels are primary advertising channels, the rest secondary advertising and data transfer.
* Frequency hopping spread spectrum (FHSS)
    * Minimises effect of ratio interferenced from other technologies in the same spectrum.
* v4, v4.1, v4.2, data rate fixed at 1MBps - called 1M PHY
* v5, 2 new physical layers introduced.
    * BLE 5 optimised for IoT. x2 speed, x4 range, x8 advertising capacity of BLE 4.
    * 2 Mbps PHY. x2 speedup! Reduces power consuption because same data transfered in less time == less radio on time.
    * Coded PHY. Longer range compared to v4 BLE. Increases power consuption because multiple symbols needed transmitted for 1 bit of data. Reduces speed since more bits required for same data.
* Bit stream encoded using Guassian Frequency Shift Keying (GFSK).
* Data rates:
    * 1 Mbps (standard)
    * 2 Mbps (high speed)
    * 125/500 Kbps (long range - LE coded PHY, S=8, S=2 respectively)


### Link Layer (LL)
* Responsible for advertising, scanning and creating/maintaining a connection.
    * Advertises      - sends advertising packets on channels 37, 38, and 39.
    * Scanner         - scans for adverttising packets.
    * Master          - initialites and manages a connection.
    * Slave           - accepts a connection request.
    * Channel hopping - hop channels to avoid interference.
* Defines packet structure, includes the state machine and radio control, and provides link layer-level encryption.

```
                      ┌─────────────┐
                      │             │
                      │ Scanning    │ (Scans for devices that are advertising)
                      │             │
                      └──────▲──────┘
                             │
                             │
                             │
                             │
(Sends out ad packets)       │ (Radio does not tx or rx)
┌─────────────┐       ┌──────▼──────┐        ┌─────────────┐
│             │       │             │        │             │ (Scanning device decides to
│ Advertising ◄───────► Standby     ◄────────► Initiating  │  establish a connection with
│             │       │             │        │             │  advertising device)
└──────┬──────┘       └──────▲──────┘        └──────┬──────┘
       │                     │                      │
       │                     │                      │
       │                     │                      │
       │                     │                      │
       │                     │                      │
       │              ┌──────┼──────┐               │
       │              │             │               │
       └──────────────► Connected   ◄───────────────┘
                      │             │
                      └─────────────┘
                      (Device has establish a link with another device.)
```
<p></p>

#### Device Address
Every Bluetooth LE device is identified by a unique 48-bit address.

* Like an Ethernet MAC. 
* 48-bit (6-byte) unique identifier.
* Two types:
    * Public device address - Fixed, factory-programmed address, registered with IEEE registration authority.
    * Random - preprogammed or dynamically generated at runtime.
        * Does not require registration with the IEEE.
        * Can be manually configured.
    * A BLE device distinguishes between a public and a random device address by examining the
      TxAdd and RxAdd bits in the Protocol Data Unit (PDU) header. If the address is public, these
      bits are set to 0, while a setting of 1 indicates a random address.

#### Packets

* Advertising - For finding and connecting to other devices.
* Data - For sending/receving data once a connection is made.

```
PACKET STRUCTURE FOR LE UNCODED PHYs

┌─────────┬────────────────┬────────────┬─────────────────────────────┬─────┬─────┬──────────────┐
│Preamble │Access Address  │ PDU Header │       PDU Payload           │ MIC │ CRC │ Constant Tone│
│         │                │            │                             │     │     │  Extension   │
└─────────┴────────────────┴────────────┴─────────────────────────────┴─────┴─────┴──────────────┘
              :            :       :                   :                          :       :
              :            :       :                   :                          :       :
         Carries physical  :       :                   :                          : Carries direction
         channel access    : Carries the logical       :                          : finding information
         code              : transport and logical     :                          :
                           : link identifiers          :                          :
                           :                           :                          :
                           :                     Carries one of the following:    :
                           :                     L2CAP signals, L2CAP frames,     :
                           :                     ISOAL segments, isochronous      :
                           :                     data, or other user data         :
                           :                                                      :
                           \______________________________________________________/
                                                    |
                                    Carries the Link Layer Protocol


PDUs on ad channels use the Adverising Physical Channel PDU.
On a data channel use the Data Channel PDU.
On Osochronous Pysical Channel uses that PDU.

Where PDU advertising PDU header looks like...

               ┌─────────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌─────────────────┐
 PDU Payload:  │PDU Type     ││RFU     ││ChSel   ││TxAdd   ││RXAdd   ││Length           │
               │(4 bits)     ││(1 bit) ││(1 bit) ││(1 bit) ││(1 bit) ││(8 bits)         │
               └─────────────┘└────────┘└────────┘└────────┘└────────┘└─────────────────┘


PACKET STRUCTURE FOR LE CODED PHYs
┌─────────┐┌──────────────────┐┌──────┐┌─────────┐┌──────────┐┌────────────────────┐┌─────┐┌─────┐┌───────┐
│Preamble ││ Access Address   ││ CI   ││ TERM1   ││ PDU Hdr  ││ PDU Payload        ││ MIC ││ CRC ││ TERM2 │
└─────────┘└──────────────────┘└──────┘└─────────┘└──────────┘└────────────────────┘└─────┘└─────┘└───────┘
```
<p></p>


* Access address
    * 32-bites in size.
    * Advertising - for broadcasting data or when advertising, scanning, or intiating connections
    * Data access address - used in connection after a connection has been establish between two devices

* Header
    * Different for advertisement vs data packet.

* The shortest allowable packet is with no data is 80 microseconds long.
* Longest allowable packet is a fully loaded advertising packet, 376 microseconds long.
* Typical advertising packet is 128 microseconds long.
* Typical data packet is 144 microseconds long.

A list of PDU types:

| PDU Type | PDU Name | Physical Channel | LE 1M | LE 2M | LE Coded |
|----------|----------|------------------|-------|-------|----------|
| 0b0000 | ADV_IND | Primary Advertising | x | | |
| 0b0001 | ADV_DIRECT_IND | Primary Advertising | x | | |
| 0b0010 | ADV_NONCONN_IND | Primary Advertising | x | | |
| 0b0011 | SCAN_REQ | Primary Advertising | x | | |
| 0b0011 | AUX_SCAN_REQ | Secondary Advertising | x | x | x |
| 0b0100 | SCAN_RSP | Primary Advertising | x | | |
| 0b0101 | CONNECT_IND | Primary Advertising | x | | |
| 0b0101 | AUX_CONNECT_REQ | Secondary Advertising | x | x | x |
| 0b0110 | ADV_SCAN_IND | Primary Advertising | x | | |
| 0b0111 | ADV_EXT_IND | Primary Advertising | x | | x |
| 0b0111 | AUX_ADV_IND | Secondary Advertising | x | x | x |
| 0b0111 | AUX_SCAN_RSP | Secondary Advertising | x | x | x |
| 0b0111 | AUX_SYNC_IND | Periodic | x | x | x |
| 0b0111 | AUX_CHAIN_IND | Secondary Advertising and Periodic | x | x | x |
| 0b0111 | AUX_SYNC_SUBEVENT_IND | Periodic | x | x | x |
| 0b0111 | AUX_SYNC_SUBEVENT_RSP | Periodic | x | x | x |
| 0b1000 | AUX_CONNECT_RSP | Secondary Advertising | x | x | x |
| All other values | Reserved for future use | | | | |
<p></p>

#### Advertising
* Allows device to broadcast prescense and therefore connections.
* Broadcast data, e.g. supported services, name, etc.

Advertising channel PDU:

```
Advertising physical channel PDU

LSB                                                                    MSB
┌─────────────┬──────────────────────────────────────────────────────────┐
│   Header    │                    Payload                               │
│  (16 bits)  │                  (1-255 octets)                          │
└─────────────┴──────────────────────────────────────────────────────────┘


Advertising physical channel PDU header

LSB                                                                    MSB
┌──────────┬─────────┬─────────┬─────────┬─────────┬──────────────────┐
│ PDU Type │   RFU   │  ChSel  │  TxAdd  │  RxAdd  │      Length      │
│ (4 bits) │ (1 bit) │ (1 bit) │ (1 bit) │ (1 bit) │     (8 bits)     │
└──────────┴─────────┴─────────┴─────────┴─────────┴──────────────────┘
```
<p></p>

In the PDU, 255 octets does not mean 255 bytes of application advertising data. For example, legacy `ADV_IND` has a 6-byte advertiser address plus 0–31 bytes of advertising data, giving a 6–37-byte payload. Extended advertising permits larger payloads, which also contain protocol fields. See [Part B. Link Layer Specification](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/low-energy-controller/link-layer-specification.html).


The 3 advertising channels are:

| Channel Index | Center Frequency  | Position in Band |
|---------------|-------------------|------------------|
| 37	| 2402 MHz	| Bottom of the band |
| 38	| 2426 MHz	| Middle of the band |
| 39	| 2480 MHz	| Top of the band    |

The are spread out to avoid a single noise source knocking out all advertising bands.

Advertising interval = time between start of one advertising event and the next +/- some random
jitter, up to 10ms, to helpa void collisisions.

Shorter adv interval means faster discovery but more power consumption, whereas longer interval means slower discovery, but less power consumption.

These are the advertising PDU types (BLE 5.4):

| PDU type | Family | Channel | Purpose / behaviour |
|---|---|---|---|
| `ADV_IND` | Legacy | Primary | General advertising: accepts both connection requests and scan requests. |
| `ADV_DIRECT_IND` | Legacy | Primary | Invites a specific device to connect; does not accept scan requests. |
| `ADV_NONCONN_IND` | Legacy | Primary | Broadcasts data; accepts neither connection requests nor scan requests. |
| `ADV_SCAN_IND` | Legacy | Primary | Advertises and accepts scan requests for additional information; does not accept connections. |
| `ADV_EXT_IND` | Extended | Primary | Announces extended advertising, usually pointing to an auxiliary packet on a secondary channel. |
| `AUX_ADV_IND` | Extended | Secondary | Carries the auxiliary advertisement; can support connections, scanning, or neither, depending on its mode. |
| `AUX_CHAIN_IND` | Extended | Secondary / periodic | Carries additional advertising data that continues from an earlier packet. |
| `AUX_SYNC_IND` | Extended | Periodic | Carries periodic advertisements
<p></p>

#### Data

```
Data Physical Channel PDU

LSB                                                                    MSB
┌───────────────────┬─────────────────────────────┬─────────────────────┐
│      Header       │          Payload            │        MIC          │
│ (16 bits or 24    │                             │      (32 bits)      │
│      bits)        │                             │     (optional)      │
└───────────────────┴─────────────────────────────┴─────────────────────┘

Data Physical Channel PDU header

                           Header
┌────────┬────────┬────────┬────────┬────────┬────────┬────────┬──────────┐
│  LLID  │  NESN  │   SN   │   MD   │   CP   │  RFU   │ Length │ CTEInfo  │
│(2 bits)│(1 bit) │(1 bit) │(1 bit) │(1 bit) │(2 bits)│(8 bits)│ (8 bits) │
│        │        │        │        │        │        │        │(optional)│
└────────┴────────┴────────┴────────┴────────┴────────┴────────┴──────────┘
```
<p></p>


### HCI - Host Controller Inteface
* Sends commands to controller and receives events back.
* Sends and receives data from a peer device.
* Interface between the physical and logical interface between devices.
    * Loigical interface defines packet formats for commands, events and data.
    * Physical interface defines how logical packets are send between host and controller.

See [Core Spec](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/host-controller-interface/host-controller-interface-functional-specification.html) for a list of all HCI commands and events - too many to summarise here!!

### Logical Link Control and Adaption Protocol (L2CAP)

> The Bluetooth Logical Link Control and Adaptation Protocol (L2CAP) supports higher level protocol multiplexing,
> packet segmentation and reassembly, and the conveying of quality of service information.

* A protocol multiplexing layer - multiple protocols from upper layers into standard BLE.
* Handles the Attribute Protocol (ATT) and Security Manager Protocol.
* Enables segmentation and reassembly of packets that are larger than what the radio can deliver.
* Error control and retransmissions.

* 3 main channels:
    * Channel 0x0004: ATT (Attribute Protocol) traffic
    * Channel 0x0006: SMP (Security Manager Protocol) traffic
    * Channel 0x0005: L2CAP signaling (like connection parameter updates)

### Generic Access Profile (GAP)

<p></p>

> Application interoperability in the Bluetooth system is accomplished by Bluetooth profiles. Bluetooth profiles define the
> required functions and features of each layer in the Bluetooth system from the PHY to L2CAP and any other protocols
> outside of this specification ...
>
> ... The Bluetooth system defines a base profile which all Bluetooth devices implement. This profile is the Generic Access
> Profile (GAP), which defines the basic requirements of a Bluetooth device.

> The GAP is used to control how a device is visible and connectable by other devices and also how to discover and connect
> to remote devices.

* Descibes:
    * **Device roles**. Roles allow devices to have radios that either transmit (TX) only, receive (RX) only, or do both.
        * They determine things like how the device advertises its presence, or how it scans and connects to other nodes.
        * NOTE: GAP roles (Central/Peripheral) describe the **connection relationship: who initiates and who accepts**. The GATT client/server relationship is separate.
        * Roles include:
            * **Broadcaster** - (Beacon) A device that sends advertising packets. Does not use connectable ad packets - no one can connect to a broadcaster.
            * **Observer**    - Device that scans for broadcasters and reports this information to an app.
            * **Peripheral**  - Device that advertises by using connectable advert packets.
            * **Central**     - Device that scans for and initialates connections to peripherals.
    * **Device modes**.
        * **Connectable**  - Can make a connection. State: Non-connectable, connectable.
        * **Discoverable** - Can be discovered (is advertising). State: None, limited, general.
        * **Bondable**     - If connectable, will pair with connected device for a long-term connection.
    * Advertisement
    * Connection establishment
* GAP uses HCI directly for advertising, scanning and connection control. It doesn't have its own L2CAP channel.
* The GAP GATT service is distinct from GAP’s discovery/connection logic.

|          | Broadcaster                 | Observer                       | Peripheral          | Control            |
|----------|-----------------------------|--------------------------------|---------------------|--------------------|
| Radio    | Radio receiver not required | Radio transmitter not required | Both required       | Both required      |
| Transfer | One way data                | One way data                   | Two way data        | Two way data       |
| Stack    | Reduced h/w and stack       | Reduced h/w and stack          | Full h/w and stack  | Full h/w and stack |
<p></p>

#### Discovery Modes and Proceedures
Discovery modes describe whether an advertising device should appear during device discovery. This happens
before GATT service discovery: first you find the device, then you explore its services and characteristics.

BLE has three discoverability modes:

| Mode | Meaning | Example use |
|---|---|---|
| **Non-discoverable** | Excluded from GAP's general and limited discovery procedures | A configured sensor that no longer needs to appear during setup |
| **General discoverable** | Available for discovery without a mandated time limit | A sensor available for an app to find |
| **Limited discoverable** | Temporarily available for discovery, for at most **180 seconds** | A device whose setup button was just pressed |

A non-discoverable device can still advertise. Its packets remain visible to scanning tools, so this mode does not hide its radio traffic.

The advertising device has a mode; the scanning device follows a procedure.

The names are similar, but their relationship is:

| Scanner’s discovery procedure | Finds general-discoverable devices? | Finds limited-discoverable devices? |
|---|---:|---:|
| **General discovery** | Yes | Yes |
| **Limited discovery** | No | Yes |

The advertiser communicates its mode through the Flags field in its advertising data. General mode sets the General Discoverable flag; limited mode sets the Limited Discoverable flag; non-discoverable mode sets neither.

NOTE: Discoverability is separate from connectability:

* *Advertising*: Is the device transmitting announcements?
* *Discoverability*: Should GAP discovery procedures report it?
* *Connectability*: Is it accepting connection requests?



#### Advertising

In the advertising state:

* Device sends out packets at fixes intervals to announce its presense.
    * Advertising intervals: The interval at which an advertising packet is sent. In the range of 20 ms to 10.24 s, with a 
      step increase of 0.625 ms.
    * Tradeoff power consumption v.s. time for device to be discovered.
* Same packet transmitted on each of the 3 primary advertisement channels.
    * Primary channel limited to 31 bytes
    * Secondary limited to 254 bytes
* Scan request and response to send additional data that exceeds above limits. This is _active scanning_
    * Receiving scans for advertisment data and sends a _scan request_
    * Advertiser provides _scan response_ if supported.
* _Passive scanning_ is where the device just listens for advertisment data without sending scan requests subsequently.

Advertising events:

| Connectable | Scannable | Directed | Description                                                                                                  |
|-------------|-----------|----------|--------------------------------------------------------------------------------------------------------------|
| Yes         | Yes       | No       | ADV_IND -Listeners can receive the ad packets, send scan requests and establish a connection.                |
| Yes         | No        | No       | Listeners can receive the ad packets and establish a connection.                                             |
| Yes         | No        | Yes      | ADV_DIRECT_IND - Specific device receives ad packets and can establish connection.                           |
| No          | No        | No       | ADV_NONCONN_IND - Listeners can receive the ad packets, canNOT sent scan requests or establish a connection. |
| No          | Yes       | No       | ADV_SCAN_IND - Only accept scan requests, but will not allow establishing a connection with it.              |
<p></p>

Advertising channels:
```
Frequency: 2402 MHz ─────────────────────────────────────────► 2480 MHz
           │                                                     │
Channel:   37  0  1  2  3  4  5  6  7  8  9  10 38 11 12...23 24 39
           │                                    │                │
           ▼                                    ▼                ▼
         ┌───┐                                ┌───┐             ┌───┐
         │ ■ │ Primary Advertisement          │ ■ │             │ ■ │
         └───┘ (Ch 37, 38, 39)                └───┘             └───┘
          2MHz                                                    
           │
         ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
         │ □ │ □ │ □ │ □ │ □ │ □ │ □ │ □ │ □ │ □ │ □ │ □ │ □ │ □ │
         └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
          0   1   2   3   4   5   6   7   8   9  10  11  12 ...36
         
         Data Transfer (Channels 0-36)


Legend:
  ■ = Primary Advertisement Channels (37, 38, 39)
  □ = Data Transfer Channels (0-36)
  
  • 3 advertising channels spaced across the band
  • 37 data channels for actual communication
  • 2 MHz spacing between channels
```
<p></p>

#### Connection (Event)
<p></p>

> The most common way to achieve two-way communication in Bluetooth Low Energy is to use connections.
> In addition, a connection grants you benefits like higher data throughput, mechanisms to handle 
> packet loss, and added security.
>
> -- Nordic Academy
<p></p>

Establishing a connection requires two devices, one acting as a peripheral that is currently advertising, and one acting as a central that is currently scanning.

* Start of a group of data packets, sent from the master to the slave and back.
* Connection no longer uses ad channels, but other 37 data channels.
* Connection parameters include:
    * Connection interval
    * Supervision timeout
    * Prehipheral latency
    * PHY radio mode
    * Data length and MTU
* Done periodically until connection is closed/lost.
* Advertises has short RX window after each advert to listen for incoming connection requests.
    * Perhipheral mostly has to accept connection req (and disconnect later if it wants) unless accpt list filter is used.
* Connection interval: The interval at which two devices in a connection wake up to exchange data.
    * Set by the central in the connection request packet. Can later be changed.
    * 7.5ms to 4s
    * Smaller interval == greater power consumption but higher throughput
* Connection event: Occurs every connection interval, when the central sends a packet to the peripheral.
* Peripheral latency: # connection events peripheral can skip without risking disconnection.
* Payload:
    * Default size is 27 bytes
    * Increase up to 251 bytes using Data Length Extensions (DLE)
* Connection supervision timeout:
    * Max time between two received data packets before connection dead.
    * 100ms to 32s.

     

### Attribute Protocol (ATT)
<p></p>
ATT (Attribute Protocol) is the message protocol that lets one Bluetooth device discover, read, and write data on another. GATT uses those messages to give the data a useful structure: services, characteristics, and descriptors.


> The Attribute protocol allows a device referred to as the server to expose a set
> of attributes and their associated values to a peer device referred to as the client
>
> ...
>
> To allow devices to read and write small data values held on a server, an Attribute Protocol 
> (ATT) is defined. Each stored value, typically only a few octets, is known as an attribute. 
> This protocol allows attribute to be self identifying using UUIDs to identify the type of data.
>
> ...
>
> Attribute protocol messages are sent over L2CAP channels, known as the _ATT bearers_.
>
> ...
>
> Attribute protocol defines two roles: Client and Server
>
> ...
>
> An ATT bearer is a channel used to send Attribute protocol PDUs. Each ATT
> bearer uses an L2CAP channel. A device may have any number of ATT bearers to a peer device.
>
> -- BLE Specification
<p></p>

> The Attribute protocol (ATT) layer, and the Generic Attribute Profile (GATT) layer right 
> above it, define how data is represented and exchanged between Bluetooth LE devices. The 
> ATT and GATT layers are concerned with the phase after a connection has been established,
> as opposed to the GAP layer which takes care of the advertisement process which occurs before 
> a connection is established.
>
> -- Nordic Semiconductor Academy
<p></p>

* Server is the device that is exposing the data and the client is the device consuming it.
    * So controller is usually the client and the peripheral is usually the servier.
* Attributes are arrays that can vary from 0 to 512 bytes.
* Can be fixed or variable length.
* E.g. a device could expose its battery level. It acts as the ATT server.
* An attribute is composed of [handle | type | value | permissions]
    * **Handle**: 	The attribute’s address within this server. A 16-bit, unique, non-zero value that is assigned by each server to its own attributes. 
        * It makes the attribute "addressable" and does not change during a single connection.
        * **The handle tells you where to access the value**.
    * **Type**: Describes what the value represents, using a UUID (2-byte or 16-byte) to identify every attribute type (no central registry for UUIDs). 
        * There are two types of UUIDs: Service UUID and Characteristic UUID.
        * **The UUID tells you what something is**.
    * **Value**: Byte array of fixed or variable length. May require multiple PDUs to transmit.
    * **Permission**: 	Rules governing access. Read or write, notified or indicated, security level required to access:
        * Readable, writable or readable and writable.
        * Encryption required or not.
        * Authentication or not.
        * Authorisation required or not.
* An attribute has a type, described by a UUID. The UUID determines what the attribute value means. 
    * 16-bit for official atts
    * 128-bit number for custom atts.
        * But 128-but very large (link layer PDU is 27 bytes) so thats why standard ones are defined:
            * 16 and 32-bit UUIDs - only used for UUIDs defined be Bluetooth SIG.

> To reduce the burden of storing and transferring 128-bit UUID values, a range
> of UUID values has been pre-allocated for assignment to often-used,
> registered purposes. The first UUID in this pre-allocated range is known as the
> Bluetooth Base UUID and has the value 00000000-0000-1000-8000-
> 00805F9B34FB, from [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/). UUID values in the pre-allocated
> range have aliases that are represented as 16-bit or 32-bit values. These
> aliases are often called 16-bit and 32-bit UUIDs, but each actually represents a
> 128-bit UUID value.
<p></p>

For the 5 main operations one does, the ATT exchanges look like this:

| Operation | ATT messages | Direction |
|---|---|---|
| Read | Read Request → Read Response | Client asks; server returns bytes |
| Write with response | Write Request → Write Response | Client supplies bytes; server reports success or an error |
| Write without response | Write Command | Client supplies bytes; no ATT reply |
| Notify | Handle Value Notification | Server supplies bytes; no ATT reply |
| Indicate | Handle Value Indication → Confirmation | Server supplies bytes; client confirms receipt |
<p></p>

Here, "without response" means no acknowledgement at the ATT level. BLE’s lower layers still provide radio retransmission. An indication’s confirmation also does not prove that the receiving application has finished acting on the data.


ATT PDUs have one of 6 types:

| Type          | Purpose                                                                          | Suffix |
|---------------|----------------------------------------------------------------------------------|--------|
| Commands      | PDUs sent to a server by a client that do not invoke a response.                 | CMD    |
| Requests      | PDUs sent to a server by a client that invoke a response.                        | REQ    |
| Responses     | PDUs sent to a client by a server in response to a request.                      | RSP    |
| Notifications | Unsolicited PDUs sent to a client by a server that do not invoke a confirmation. | NTF    |
| Indications   | Unsolicited PDUs sent to a client by a server that invoke a confirmation.        | IND    |
| Confirmations | PDUs sent to a server by a client to confirm receipt of an indication.           | CFM    |
<p></p>

A Protocol Data Unit, or PDU, is one ATT message. It begins with an opcode identifying the operation, followed by operation-specific fields.


### Generic Attribute Profile (GATT)
GATT (Generic Attribute Profile) defines how Bluetooth devices organise data and how other devices interact with it. It gives you the services, characteristics, and descriptors you see when working with Bluetooth Low Energy.

<p></p>

> Generic Attribute Profile (GATT) is built on top of the Attribute protocol (ATT) and establishes common operations and
> a framework for the data transported and stored by the Attribute protocol...
>
>...
>
> The Bluetooth system defines a base profile which all Bluetooth devices implement. This profile is the Generic Access
> Profile (GAP), which defines the basic requirements of a Bluetooth device. For instance, or BR/EDR, it defines a
> Bluetooth device to include the Radio, Baseband, Link Manager, L2CAP, and the Service Discovery protocol functionality;
> for LE, it defines the Physical Layer, Link Layer, L2CAP, Security Manager, Attribute Protocol and Generic Attribute Profile.
> This ties all the various layers together to form the basic requirements for a Bluetooth device. It also describes the
> behaviors and methods for device discovery, connection establishment, security, authentication, association models and service
> discovery.
>
>
> In LE, GAP defines four specific roles: Broadcaster, Observer, Peripheral, and Central ... In LE, GAP defines four specific
> roles: Broadcaster, Observer, Peripheral, and Central.
<p></p>

> The Generic Attribute Profile (GATT) layer sits directly on top of the ATT layer, 
> and builds on it by hierarchically classifying attributes into profiles, services and characteristics.
>
> -- Nordic Semiconductor Academy
<p></p>

> The GATT layer is in charge of defining a hierarchical data structure that demonstrates the 
> relationship or connection between the data stored in an ATT server.
>
> -- Novel bits.
<p></p>

The GATT layer groups attributes from the ATT layer into services, further subdivided into characteristics, where each characteristic
has a value and a descriptor.

**Services, characteristics, and descriptors are all represented using ATT attributes**.


* Services and characteristics are both attributes.
    * Services group related functionality (like "Heart Rate" or "Battery")
    * Characteristic is a container for user data: they represent individual data points within a service (like "Heart Rate Measurement" or "Battery Level")
    * Include at least
        * characteristic declaration - metadata
        * characteristic value - user data in the value field
    * And can be followed by descriptors, which provide metadata about characteristics (like whether notifications are enabled)
* GATT defines how services and characteristics can be discovered and used.

> A service is a collection of data and associated behaviors to accomplish a
> particular function or feature.
> ...
> There are two types of services: primary service and secondary service

* Primary service exposes the primary usable functionality of the device.
    * Can be included in other services
    * Can be discovered using Primary Service Discovery procedures. 
* Secondary service only intended to be included from a primary service
  or another secondary service.

GATT uses a client-server architecture:

* The GATT Server holds the database of services and characteristics. It responds to read/write requests and sends notifications/indications.
* The GATT Client discovers the server's database and performs read/write operations. It subscribes to notifications and indications.

Imagine a Bluetooth temperature sensor connected to your phone. The sensor exposes a structured collection of data, and GATT tells the phone how to discover and use it.

The structure has three main building blocks:

| Building block | Purpose | Example |
|---|---|---|
| **Service** | Groups related functionality | Battery Service |
| **Characteristic** | Holds a value and describes the supported operations | Battery Level: 85%, readable and notifiable |
| **Descriptor** | Supplies extra information or configuration for a characteristic | A setting that enables battery notifications |

A device might expose this structure:

```
Temperature sensor
│
├── Temperature Service
│   └── Temperature Measurement characteristic
│       ├── Value: encoded temperature
│       └── Descriptor: configuration for updates
│
└── Battery Service
    └── Battery Level characteristic
        ├── Value: 85%
        └── Descriptor: configuration for updates
```

Each service and characteristic has a UUID, an identifier describing its type. Standard UUIDs let devices from different manufacturers agree on meanings such as "Battery Level". Custom UUIDs support application-specific functionality.

For the above its GATT database would be a flat table of ATT attributes. The declarations and their order give that table the service → characteristic → descriptor structure:

| Handle | Attribute type UUID | Attribute value / meaning |
|---|---|---|
| `0x0001` | Primary Service — `0x2800` | Health Thermometer Service UUID: `0x1809` |
| `0x0002` | Characteristic Declaration — `0x2803` | Properties: **Indicate**; value handle: `0x0003`; characteristic UUID: `0x2A1C` |
| `0x0003` | Temperature Measurement — `0x2A1C` | Encoded temperature measurement |
| `0x0004` | CCCD — `0x2902` | `00 00`: indications disabled for this client |
| `0x0005` | Primary Service — `0x2800` | Battery Service UUID: `0x180F` |
| `0x0006` | Characteristic Declaration — `0x2803` | Properties: **Read + Notify**; value handle: `0x0007`; characteristic UUID: `0x2A19` |
| `0x0007` | Battery Level — `0x2A19` | `55` hex = **85%** |
| `0x0008` | CCCD — `0x2902` | `00 00`: notifications disabled for this client |

Each row also has permissions, omitted here to keep the table readable.

CCCD stands for Client Characteristic Configuration Descriptor, UUID `0x2902`. It's the setting your phone writes to enable or disable updates from a particular characteristic.

UUID vs Handle:

| | UUID | Handle |
|---|---|---|
| Purpose | Identifies a type or meaning | Addresses a specific attribute |
| Size | 128 bits; assigned Bluetooth UUIDs can use a shortened form | 16 bits |
| Unique within a database? | Can appear multiple times | Each attribute has its own |
| Example | `0x2902` means CCCD | `0x0008` identifies one particular CCCD |


```
+--------------------------------------------------------------------------------+
|  Profile                                                                       | The GATT layer defines a 4-level tree-like framework:
|                                                                                |    - The root node is named the profile. (level 0)
|  +---------------------+                    +-----------------------------+    |    - Children of the profile are named services. (level 1)
|  | Service             |                    | Service                     |    |    - Children of services are named characteristics. (level 2)
|  |                     |                    |                             |    |    - And characteristics can be defined by a single value and 
|  | +----------------+  |                    | +------------------------+  |    |      0-n descriptors (level 3)
|  | | Include        |  |                    | | Include                |  |    |
|  | +----------------+  |                    | +------------------------+  |    |    GATT Server
|  |        :            |                    |           :                 |    |       |
|  |        :            |                    |           :                 |    |       +---- Service
|  |        :            |                    |           :                 |    |       |        |
|  | +----------------+  |                    | +------------------------+  |    |       |        +---- Characteristic
|  | | Include        |  |                    | | Include                |  |    |       |        |        |
|  | +----------------+  |        ...         | +------------------------+  |    |       |        |        +---- Value
|  |                     |                    |                             |    |       |        |        |
|  | +----------------+  |                    | +------------------------+  |    |       |        |        +---- Descriptor
|  | | Characteristic |  |                    | | Characteristic         |  |    |       |        |
|  | |                |  |                    | |                        |  |    |       |        +---- Characteristic
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |       |                 |
|  | | |Properties |  |  |                    | | | Properties        |  |  |    |       |                 +---- Value
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |       |                 |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |       |                 +---- Descriptor
|  | | | Value     |  |  |                    | | | Value             |  |  |    |       |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |       +---- Service
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |                |
|  | | |Descriptor |  |  |                    | | | Descriptor        |  |  |    |                +---- Characteristic
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |                         |
|  | |       o        |  |                    | |          :             |  |    |                         +---- Value
|  | |       o        |  |                    | |          :             |  |    |                         |
|  | |       o        |  |                    | |          :             |  |    |                         +---- Descriptor
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | | |Descriptor |  |  |                    | | | Descriptor        |  |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | +----------------+  |                    | +------------------------+  |    |
|  |        :            |                    |           :                 |    |
|  |        :            |                    |           :                 |    |
|  |        :            |                    |           :                 |    |
|  | +----------------+  |                    | +------------------------+  |    |
|  | | Characteristic |  |                    | | Characteristic         |  |    |
|  | |                |  |                    | |                        |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | | |Properties |  |  |                    | | | Properties        |  |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | | | Value     |  |  |                    | | | Value             |  |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | | |Descriptor |  |  |                    | | | Descriptor        |  |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | |       :        |  |                    | |          :             |  |    |
|  | |       :        |  |                    | |          :             |  |    |
|  | |       :        |  |                    | |          :             |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | | |Descriptor |  |  |                    | | | Descriptor        |  |  |    |
|  | | +-----------+  |  |                    | | +-------------------+  |  |    |
|  | +----------------+  |                    | +------------------------+  |    |
|  +---------------------+                    +-----------------------------+    |
+--------------------------------------------------------------------------------+
```
<p></p>


Characteristics look like this:

```
+-----------------------------------+
| Characteristic Declaration        | - An attribute. UUID set to "characteristic" - 0x2803.
+-----------------------------------+
| Characteristic Value              | - An attribute. Contains the _value_ of a characteristic.
| Declaration                       |
+-----------------------------------+
| Descriptor Declaration            |
+-----------------------------------+
              o o o
+-----------------------------------+
| Descriptor Declaration            |
+-----------------------------------+
```
<p></p>


The characteristic declaration:

```
+----------------+------------------+-------------------------------------+----------------------+
| Attribute      | Attribute Type   | Attribute Value                     | Attribute            |
| Handle         |                  |                                     | Permission           |
+----------------+------------------+-------------------------------------+----------------------+
| 0xNNNN         | Characteristic   | +----------------+--------+------+  | Read Only            |
| |              | (0x2803)         | | Properties     | Handle | UUID |  | No Authenticatio     |
| |              |                  | +-|--------------+-|------+-|----+  | No Authorization     |
+-|--------------+------------------+---|----------------|--------|-------+----------------------+
  |                                     |                |        |
  |                                     |                |        16-bit or 128-bit UUID describing type 
  |                                     |                |        of Characteristic Value
  |                                     |                Attribute Handle of the Attribute that contains 
  |                                     |                the Characteristic Value
  |                                     A bit field that determines how the Characteristic Value can 
  |                                     be used: Broadcast, Read, Write Without Response, Write, Notify
  |                                     Indicate, Authenticated Signed Writes, Extended Properties.
  A handle identifies where that particular attribute is in a device’s database.
  This is different from a UUID, which identifies what an attribute is.
```
<p></p>


* GAP service is *manditory*. 
    * A device shall have only one instance of the GAP service in the GATT server
    * Characteristic is the device name string and a value that determines device appearance:   
        * Device name - the name of the device as an UTF-8 string - type is set to 0x2A00
        * Appearance - type is set to 0x2A01 - enables the discovering device to represent the
          device to the user using an icon, or a string, etc.
        * Peripheral Preferred Connection Parameters
        * Central Address Resolution
        * Resolvable Private Address Only

Most likely services you'll bump into:

| GATT service | UUID | What it provides | Typical devices |
|---|---|---|---|
| **Battery** | `0x180F` | Battery level and related information | Sensors, wearables, keyboards |
| **Device Information** | `0x180A` | Manufacturer, model, serial number, firmware version | Many types of peripherals |
| **Heart Rate** | `0x180D` | Heart-rate measurements | Chest straps, fitness sensors |
| **Human Interface Device (HID)** | `0x1812` | Input reports such as key presses and mouse movement | Keyboards, mice, controllers |
| **Environmental Sensing** | `0x181A` | Measurements such as temperature, humidity, and pressure | Environmental monitors |
| **Health Thermometer** | `0x1809` | Temperature measurements for health applications | Medical thermometers |
| **Cycling Speed and Cadence** | `0x1816` | Wheel and crank revolution measurements | Bicycle sensors |
| **Blood Pressure** | `0x1810` | Blood-pressure measurements | Blood-pressure monitors |

You'll also encounter two infrastructure services:

* Generic Access / GAP Service (0x1800) exposes information such as the device name and appearance.
* Generic Attribute / GATT Service (0x1801) supports managing the GATT database—for example, informing a client that the services have changed through the Service Changed characteristic.

#### Sending Data
* The server can send information to the client, without a client actually requesting information, or a client
  can request data from the server.
    * Service discovery: The process in which a GATT client discovers the services and characteristics in
      an attribute table hosted by a GATT server.
* Client initiated data requests:
    * Read, write, write without reponse
* Servier initiated: Client must subscribe to characteristics and enable notifiy/indicate ops.
    * Noitfy: automatically push the value of a certain attribute to the client. Client not required to ack.
    * Indicate: Like notify but client must ack. Can only send one per connection interval so slower than notifications.       

#### Service Discovery
To discover services:

* The client sends ATT discovery requests that ask the server to describe its GATT database. It learns service UUIDs and handle ranges, then discovers the characteristics and descriptors within them.
* After connecting, the client sends an ATT Read By Group Type Request, asking to find Primary Service declarations (UUID `0x2800`) between handlers `0x0001` and `0xFFFF`.
* The server returns a set of entries so that the client can know which services exist and where each service's attributes live. If they do not all fit in one response, it repeats the request starting after the last returned service end handle. An "Attribute Not Found" response normally marks the end of the search.

To discover a service's characteristics:

* The client sends an ATT Read By Type Request asking to "find Characteristic declarations (UUID `0x2803`) between handles A and B".
* The response descrobes the characteristics.

Then to discover the descriptors:
* The client sends an ATT Find Information Request over the space after the characteristic value, up to the end of that characteristic.


### SMP (Security Manager Protocol)
#### Pairing
Paring means that devices establish a secure connection with these properties:

* Connection is capable of data encryption to keep the communication confidential.
* Connection is capable of data authentication, ensuring the data comes from a trusted source.
* Connection offers device authentication, confirming the identity of the devices.
* Connection provides device tracking protection, preventing unwanted tracking.

Generating, distributing and authenticating the encruption keys is what the pairing process does.

Process has 3 phases:

1. Initiate paring.
    * Central sends pairing request. Periphal responds with pairing response.
    * Exchance or pairing features, including IO capabilities:
        * DisplayOnly - Peer only has a display
        * DisplayYesNo - Peer can ask user to select yes or no
        * KeyboardOnly - Peer has a keyboard
        * NoInputNoOuput - No IO!
        * KeyboardDisplay - Both keyboard and display 
2. Perform paring.
    * Keys generated
    * Bluetooth v4.2 introduced more secure keys ("LE Secure Connections" - uses elliptic curve pub/priv keys).
    * Methods - determied my OOB, MITM flags and I/O capabilities:
        * Just works - Short Term Key (STK) generated based on info exhanged in plain text - eek! UNAUTHENTICATED!
        * Passkey - 6-digit number shown on one device entered on the other. I/O capabilities determine who displays.
        * Out of band - Keys exchanged by some other means.
        * Numeric comparison - Both devices display a 6-digit number and user selects y/n to confirm.
3. Key distribution.
    * Long Term Key (LTK) is used to distribute the rest of the keys

##### Steps
1. Feature exchange: paring request and response packets whcih detail a device's features and capabilities.
2. Key generation.
3. Transport-specific key distribution.

#### Bonding
* Devices remember the security information exchanged during a successful pairing.  I.e. caches the keys.
* Enables automatic re-connect without having to re-pair.


## BleuIO BLE Dongle AT Command Cheatsheet
 (AI Generated)

Quick reference for the most commonly used [BleuIO USB BLE Dongle commands](https://www.bleuio.com/getting_started/docs/commands/), covering scanning, advertising, connecting and GATT operations.

### 1. Basic Commands and Device Configuration

| Command | Description |
|---|---|
| `AT` | Test communication with dongle |
| `ATI` | Show firmware version and device information |
| `ATR` | Reset dongle |
| `AT+GAPSTATUS` | Show BLE role and connection status |
| `AT+CENTRAL` | Set central role |
| `AT+PERIPHERAL` | Set peripheral role |
| `AT+DUAL` | Set dual role |
| `AT+GETMAC` | Get dongle BLE MAC address |
| `AT+DEVICENAME` | Get or set the BLE device name |

### 2. Scanning for BLE Devices

| Command | Description |
|---|---|
| `AT+GAPSCAN` | Scan continuously |
| `AT+GAPSCAN=5` | Scan for 5 seconds |
| `AT+SCANFILTER=NAME=Sensor` | Filter by advertised name |
| `AT+SCANFILTER=UUID=180F` | Filter by service UUID |
| `AT+SCANFILTER=CLEAR` | Clear scan filter |
| `AT+SCANTARGET=[0]AA:BB:CC:DD:EE:FF=5` | Scan one device for 5 seconds |
| `AT+SCANPARAM` | Get or configure scan parameters |
| `Ctrl+C` | Stop an active scan |

### 3. Connecting and Disconnecting

| Command | Description |
|---|---|
| `AT+GAPCONNECT=[0]AA:BB:CC:DD:EE:FF` | Connect to public address |
| `AT+GAPCONNECT=[1]AA:BB:CC:DD:EE:FF` | Connect to random address |
| `AT+GAPCONNECT=1!` | Connect using scan result index 1 |
| `AT+GAPDISCONNECT` | Disconnect current peer |
| `AT+GAPDISCONNECTALL` | Disconnect all peers |
| `AT+GETCONN` | List connected devices |
| `AT+TARGETCONN=0000` | Select connection index 0 |

### 4. GATT Services and Characteristics

| Command | Description |
|---|---|
| `AT+GETSERVICES` | Discover remote GATT services and characteristics |
| `AT+GETSERVICESONLY` | Discover services only |
| `AT+GETSERVICEDETAILS=0017` | Get characteristics for service at handle 0x0017 |
| `AT+GATTCREAD=0012` | Read attribute handle 0x0012 |
| `AT+GATTCWRITE=0012 HELLO` | Write ASCII data |
| `AT+GATTCWRITEB=0012 010203` | Write binary data as hex |
| `AT+GATTCWRITEWR=0012 HELLO` | Write ASCII without response |
| `AT+SETNOTI=0012` | Enable characteristic notifications |
| `AT+CLEARNOTI=0012` | Disable characteristic notifications |
| `AT+SETINDI=0012` | Enable characteristic indications |
| `AT+NOTI` | Configure notifications (course command) |
| `AT+INDI` | Configure indications (course command) |
| `AT+CUSTOMSERVICE` | Create a custom local GATT service |

**Notes:**

- GATT read/write operations use attribute handles, not UUIDs.
- Attribute handles are specific to the remote GATT database.
- Discover services and characteristics before accessing their handles.
- Notifications do not require acknowledgement at the ATT layer.
- Indications require acknowledgement at the ATT layer.
- Notifications and indications are generally enabled by configuring
  the Client Characteristic Configuration Descriptor (CCCD).
- The course lists `AT+NOTI` and `AT+INDI`, whereas the original
  cheatsheet uses `AT+SETNOTI`, `AT+CLEARNOTI` and `AT+SETINDI`.
  Check which variants your firmware supports.

### 5. BLE Advertising

| Command | Description |
|---|---|
| `AT+ADVSTART` | Start advertising |
| `AT+ADVSTOP` | Stop advertising |
| `AT+ADVDATA` | Read configured advertising data |
| `AT+ADVDATA=04:09:43:41:54` | Set advertising data (example name CAT) |
| `AT+ADVRESP` | Read scan response data |
| `AT+ADVRESP=00` | Clear scan response data |

**Notes:**

- Legacy BLE advertising uses channels 37, 38 and 39.
- Advertising allows nearby central devices to discover the dongle.
- Advertising data can include device names, service UUIDs and
  manufacturer-specific information.
- Scan response data can provide additional information to scanners.

### 6. Security, Pairing and Bonding (SMP)

| Command | Description |
|---|---|
| `AT+GAPPAIR` | Initiate BLE pairing |
| `AT+ENTERPASSKEY` | Enter a passkey during pairing |
| `AT+NUMCOMPA` | Confirm numeric comparison during pairing |
| `AT+SECLVL` | Set minimum security level |
| `AT+GETBOND` | List bonded devices |
| `AT+GAPUNPAIR` | Remove stored bonding information |
| `AT+GAPIOCAP` | Configure device I/O capabilities |

**Notes:**

- Pairing establishes security keys between devices.
- Bonding stores keys for reuse on subsequent connections.
- Encryption protects communication over an established BLE link.
- I/O capabilities influence the pairing method selected.
- Numeric Comparison requires user confirmation of matching numbers.
- Passkey Entry requires a six-digit passkey.
- Just Works pairing does not provide MITM protection.
- BLE Secure Connections uses ECDH key agreement.

### 7. Connection Parameters, Scanning and MTU

| Command | Description |
|---|---|
| `AT+CONNPARAM` | Get or configure BLE connection parameters |
| `AT+SCANPARAM` | Get or configure scan interval and window |
| `AT+MTU` | Configure ATT Maximum Transmission Unit |

#### Connection Parameters

| Parameter | Description |
|---|---|
| Connection Interval | Time between connection events |
| Peripheral Latency | Number of consecutive connection events the peripheral may skip |
| Supervision Timeout | Maximum time without successful communication before connection loss |
| Scan Interval | Time between the starts of consecutive scan windows |
| Scan Window | Duration spent scanning during each scan interval |
| ATT MTU | Maximum size of an ATT protocol data unit |

**Notes:**

- Shorter connection intervals can reduce communication latency
  but may increase power consumption.
- Peripheral latency allows a peripheral to skip connection events
  to reduce power consumption.
- The supervision timeout determines when a connection is considered lost.
- A larger ATT MTU can improve throughput for larger GATT values.
- The default ATT MTU is 23 bytes.
- The maximum attribute value in a single ATT notification is
  typically ATT_MTU - 3 bytes.
- ATT MTU negotiation does not directly change the Link Layer
  data length. These are separate mechanisms.

### 8. Typical BLE Central Connection Sequence

```text
AT
ATI
AT+CENTRAL
AT+GAPSCAN=5
AT+GAPCONNECT=[0]AA:BB:CC:DD:EE:FF
AT+GETSERVICES
AT+GATTCREAD=0012
AT+SETNOTI=0012
AT+GAPDISCONNECT
```

### 9. Typical BLE Peripheral Sequence

```text
AT
ATI
AT+PERIPHERAL
AT+ADVSTART
AT+GAPSTATUS
AT+ADVSTOP
```

For a custom GATT server, configure the required services and
characteristics before starting advertising.

### 10. BLE Protocol Stack Command Mapping

| Protocol Layer | AT Commands | Purpose |
|---|---|---|
| Application | `AT`, `ATI`, `ATR` | Dongle control and information |
| GAP | `AT+CENTRAL`, `AT+PERIPHERAL`, `AT+DUAL` | Device roles |
| GAP | `AT+GAPSCAN`, `AT+GAPCONNECT`, `AT+GAPDISCONNECT` | Discovery and connections |
| GAP | `AT+ADVSTART`, `AT+ADVSTOP`, `AT+DEVICENAME` | Advertising and device identity |
| GATT | `AT+GETSERVICES`, `AT+GETSERVICEDETAILS` | Service and characteristic discovery |
| GATT / ATT | `AT+GATTCREAD`, `AT+GATTCWRITE`, `AT+GATTCWRITEB` | Attribute read/write |
| GATT / ATT | `AT+NOTI`, `AT+INDI`, `AT+SETNOTI`, `AT+SETINDI` | Notifications and indications |
| GATT | `AT+CUSTOMSERVICE` | Local GATT server configuration |
| SMP | `AT+GAPPAIR`, `AT+ENTERPASSKEY`, `AT+NUMCOMPA` | Pairing |
| SMP | `AT+SECLVL`, `AT+GAPIOCAP` | Security configuration |
| SMP | `AT+GETBOND`, `AT+GAPUNPAIR` | Bond management |
| Link Layer | `AT+CONNPARAM` | Connection timing |
| GAP / Link Layer | `AT+SCANPARAM` | Scanning configuration |
| ATT / L2CAP | `AT+MTU` | ATT MTU configuration |

