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
using ATT layer         |              |                         |      to handle device discovery and
                        ├──────────────┼──────────────┐          │      connection related services
Allow dev to expose --->│     ATT      │    SMP <-----|----------│----- Security Manage Protocol: defines
attributes to others    |              |              |          |      and provides methods for secure
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

### Link Layer (LL)
* Responsible for advertising, scanning and creating/maintaining a connection.
    * Advertises - sends advertising packets.
    * Scanner    - scans for adverttising packets.
    * Master     - initialites and manages a connection.
    * Slave      - accepts a connection request.
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

* Like an Ethernet MAC. 
* 48-bit (6-byte) unique identifier.
* Two types:
    * Public device address - Fixed, factory-programmed address, registered with IEEE.
    * Random - preprogammed or dynamically generated at runtime.
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

Where PDU playload looks like...

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

### Generic Access Profile (GAP)

> Application interoperability in the Bluetooth system is accomplished by Bluetooth profiles. Bluetooth profiles define the
> required functions and features of each layer in the Bluetooth system from the PHY to L2CAP and any other protocols
> outside of this specification ...
>
> ... The Bluetooth system defines a base profile which all Bluetooth devices implement. This profile is the Generic Access
> Profile (GAP), which defines the basic requirements of a Bluetooth device.

> The GAP is used to control how a device is visible and connectable by other devices and also how to discover and connect
> to remote devices.

* Descibes:
    * Device roles. Roles allow devices to have radios that either transmit (TX) only, receive (RX) only, or do both.
                    They determine things like how the device advertises its presence, or how it scans and connects 
                    to other nodes.
        * Broadcaster - (Beacon) A device that sends advertising packets. Does not use connectable ad packets - no one can connect to a broadcaster.
        * Observer    - Device that scans for broadcasters and reports this information to an app.
        * Peripheral  - Device that advertises by using connectable advert packets.
        * Central     - Device that scans for and initialates connections to peripherals.
    * Modes
        * Connectable  - Can make a connection. State: Non-connectable, connectable.
        * Discoverable - Can be discovered (is advertising). State: None, limited, general.
        * Bondable     - If connectable, will pair with connected device for a long-term connection.
    * Advertisement
    * Connection establishment

|          | Broadcaster                 | Observer                       | Peripheral          | Control            |
|----------|-----------------------------|--------------------------------|---------------------|--------------------|
| Radio    | Radio receiver not required | Radio transmitter not required | Both required       | Both required      |
| Transfer | One way data                | One way data                   | Two way data        | Two way data       |
| Stack    | Reduced h/w and stack       | Reduced h/w and stack          | Full h/w and stack  | Full h/w and stack |
<p></p>

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
Establishing a connection requires two devices, one acting as a peripheral that is currently advertising, and one acting as a central that is currently scanning.

* Start of a group of data packets, sent from the master to the slave and back.
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
> The Attribute protocol allows a device referred to as the server to expose a set
> of attributes and their associated values to a peer device referred to as the client
> ...
> To allow devices to read and write small data values held on a server, an Attribute Protocol 
> (ATT) is defined. Each stored value, typically only a few octets, is known as an attribute. 
> This protocol allows attribute to be self identifying using UUIDs to identify the type of data.
> ...
> Attribute protocol messages are sent over L2CAP channels, known as the _ATT bearers_.
> ...
> Attribute protocol defines two roles: Client and Server
> ...
> An ATT bearer is a channel used to send Attribute protocol PDUs. Each ATT
> bearer uses an L2CAP channel. A device may have any number of ATT bearers to a peer device.
> -- BLE Specification
<p></p>

> The Attribute protocol (ATT) layer, and the Generic Attribute Profile (GATT) layer right 
> above it, define how data is represented and exchanged between Bluetooth LE devices. The 
> ATT and GATT layers are concerned with the phase after a connection has been established,
> as opposed to the GAP layer which takes care of the advertisement process which occurs before 
> a connection is established.
> -- Nordic Semiconductor Academy
<p></p>

* Server is the device that is exposing the data and the client is the device consuming it.
* Attributes are arrays that can vary from 0 to 512 bytes.
* Can be fixed or variable length.
* E.g. a device could expose its battery level. It acts as the ATT server.
* An attribute is composed of handle | type | value | permissions
    * Handle: 16-bit, unique, non-zero value that is assigned by each server to its own attributes.
    * Type: A UUID is used to identify every attribute type (no central registry for UUIDs).
    * Value: Byte array of fixed or variable length. May require multiple PDUs to transmit.
    * Permission: Read or write, notified or indicated, security level required to access:
        * Readable, writable or readable and writable.
        * Encryption required or not.
        * Authentication or not.
        * Authorisation required or not.
* An attribute has a type, described by a UUID. The UUID determines what the attribute value means. 
    * 16-bit for official atts
    * 128-bit number for custom atts.
        * But 128-but very large (link layer PDU is 27 bytes) so can also use
            * 16 and 32-bit UUIDs - only used for UUIDs defined be Bluetooth SIG.

> To reduce the burden of storing and transferring 128-bit UUID values, a range
> of UUID values has been pre-allocated for assignment to often-used,
> registered purposes. The first UUID in this pre-allocated range is known as the
> Bluetooth Base UUID and has the value 00000000-0000-1000-8000-
> 00805F9B34FB, from [Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/). UUID values in the pre-allocated
> range have aliases that are represented as 16-bit or 32-bit values. These
> aliases are often called 16-bit and 32-bit UUIDs, but each actually represents a
> 128-bit UUID value.

* ATT PDUs have one of 6 types:

| Type | Purpose | Suffix |
|------|---------|--------|
| Commands | PDUs sent to a server by a client that do not invoke a response. | CMD |
| Requests | PDUs sent to a server by a client that invoke a response. | REQ |
| Responses | PDUs sent to a client by a server in response to a request. | RSP |
| Notifications | Unsolicited PDUs sent to a client by a server that do not invoke a confirmation. | NTF |
| Indications | Unsolicited PDUs sent to a client by a server that invoke a confirmation. | IND |
| Confirmations | PDUs sent to a server by a client to confirm receipt of an indication. | CFM |
<p></p>


### Generic Attribute Profile (GATT)

> Generic Attribute Profile (GATT) is built on top of the Attribute protocol (ATT) and establishes common operations and
> a framework for the data transported and stored by the Attribute protocol...
>
> ... The Bluetooth system defines a base profile which all Bluetooth devices implement. This profile is the Generic Access
> Profile (GAP), which defines the basic requirements of a Bluetooth device. For instance, or BR/EDR, it defines a
> Bluetooth device to include the Radio, Baseband, Link Manager, L2CAP, and the Service Discovery protocol functionality;
> for LE, it defines the Physical Layer, Link Layer, L2CAP, Security Manager, Attribute Protocol and Generic Attribute Profile.
> This ties all the various layers together to form the basic requirements for a Bluetooth device. It also describes the
> behaviors and methods for device discovery, connection establishment, security, authentication, association models and service
> discovery.
>
> In LE, GAP defines four specific roles: Broadcaster, Observer, Peripheral, and Central ... In LE, GAP defines four specific
> roles: Broadcaster, Observer, Peripheral, and Central.
<p></p>

> The Generic Attribute Profile (GATT) layer sits directly on top of the ATT layer, 
> and builds on it by hierarchically classifying attributes into profiles, services and characteristics.
> -- Nordic Semiconductor Academy
<p></p>

* Attributes grouped into services
* Services and characteristics are both attributes.
    * Characteristic is a container for user data
    * Include at least
        * characteristic declaration - metadata
        * characteristic value - user data in the value field
    * And can be followed by descriptors.
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

```
+--------------------------------------------------------------------------------+
|  Profile                                                                       |
|                                                                                |
|  +---------------------+                    +-----------------------------+    |
|  | Service             |                    | Service                     |    |
|  |                     |                    |                             |    |
|  | +----------------+  |                    | +------------------------+  |    |
|  | | Include        |  |                    | | Include                |  |    |
|  | +----------------+  |                    | +------------------------+  |    |
|  |        :            |                    |           :                 |    |
|  |        :            |                    |           :                 |    |
|  |        :            |                    |           :                 |    |
|  | +----------------+  |                    | +------------------------+  |    |
|  | | Include        |  |                    | | Include                |  |    |
|  | +----------------+  |        ...         | +------------------------+  |    |
|  |                     |                    |                             |    |
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
|  | |       o        |  |                    | |          :             |  |    |
|  | |       o        |  |                    | |          :             |  |    |
|  | |       o        |  |                    | |          :             |  |    |
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
| Characteristic Value              |
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
|                | (0x2803)         | | Properties     | Handle | UUID |  | No Authenticatio     |
|                |                  | +-|--------------+-|------+-|----+  | No Authorization     |
+----------------+------------------+---|----------------|--------|-------+----------------------+
                                        |                |        |
                                        |                |        16-bit or 128-bit UUID describing type 
                                        |                |        of Characteristic Value
                                        |                Attribute Handle of the Attribute that contains 
                                        |                the Characteristic Value
                                        A bit field that determines how the Characteristic Value can 
                                        be used: Broadcast, Read, Write Without Response, Write, Notify
                                        Indicate, Authenticated Signed Writes, Extended Properties.
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

## Pairing
Paring means that devices establish a connection with these properties:

* Connection it capable of data encryption to keep the communication confidential.
* Connection it capable of data authentication, ensuring the data comes from a trusted source.
* Connection offers device authentication, confirming the identity of the devices.
* Connection provides device tracking protection, preventing unwanted tracking.


### Steps
1. Feature exchange: paring request and response packets whcih detail a device's features and capabilities.
2. Key generation.
3. Transport-specific key distribution.

## Bonding
* Devices remember the security information exchanged during a successful pairing. 
* Enables automatic re-connect without having to re-pair.
