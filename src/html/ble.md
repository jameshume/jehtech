## The Basics

* Low power, low bandwidth application focus
* 2.4GHz ISM Band (Industrial Scientific Medical Band)
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
┌─────────────────┐
│ Application     │
└─────────────────┘
┌─────────────────┐
│ GATT            │
└─────────────────┘
┌────┐ ┌──┐ ┌─────┐
│ GAP│ │SM│ │ATT  │
└────┘ └──┘ └─────┘
┌─────────────────┐
│ L2CAP           │
└─────────────────┘
┌─────────────────┐
│ HCI             │
└─────────────────┘
┌─────────────────┐
│ Link Layer      │
└─────────────────┘
┌─────────────────┐
│ RF and PHY      │
└─────────────────┘
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
* Ensures packets are structured properly

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


#### Packets

* Advertising - For finding and connecting to other devices.
* Data - For sending/receving data once a connection is made.

```
PACKET STRUCTURE FOR LR UNCODED PHYs
┌─────────┐┌──────────────────┐┌──────────┐┌────────────────────┐┌─────┐┌─────┐┌───────┐
│         ││                  ││ PDU Hdr  ││ PDU Payload        ││ MIC ││ CRC ││ TERM2 │
└─────────┘└──────────────────┘└──────────┘└────────────────────┘└─────┘└─────┘└───────┘


PACKET STRUCTURE FOR LE CODED PHYs
┌─────────┐┌──────────────────┐┌──────┐┌─────────┐┌──────────┐┌────────────────────┐┌─────┐┌─────┐┌───────┐
│Preamble ││ Access Address   ││ CI   ││ TERM1   ││ PDU Hdr  ││ PDU Payload        ││ MIC ││ CRC ││ TERM2 │
└─────────┘└──────────────────┘└──────┘└─────────┘└──────────┘└────────────────────┘└─────┘└─────┘└───────┘
```

* Access address
    * 32-bites in size.
    * Advertising - for broadcasting data or when advertising, scanning, or intiatin connections
    * Data access address - used in connection adter a connection has been establish between two devices

* Header
    * Different for ad vs data packet.

* The shortes allowable packet is with no data is 80 microseconds long.
* Longest allowable packet is a fully loaded advertising packet, 376 microseconds long.
* Typical advertising packet is 128 microseconds long.
* Typical data packet is 144 microseconds long.

### HCI - Host Controller Inteface
* Sends commands to controller and receives events back.
* Sends and receives data from a peer device.
* Interface between the physical and logical interface between devices.
    * Loigical interface defines packet formats for commands, events and data.
    * Physical interface defines how logical packets are send between host and controller.

### Logical Link Control and Adaption Protocol (L2CAP)

> The Bluetooth Logical Link Control and Adaptation Protocol (L2CAP) supports higher level protocol multiplexing,
> packet segmentation and reassembly, and the conveying of quality of service information.

* A protocol multiplexing layer - multiple protocols from upper layers into standard BLE.
* Handles the Attribute Protocol (ATT) and Security Manager Protocol.
* Enables segmentation and reassembly of packets that are larger than what the radio can deliver.
* Error control and retransmissions.


### Attribute Protocol (ATT)

> To allow devices to read and write small data values held on a server, an Attribute Protocol (ATT) is defined.
> Each stored value, typically only a few octets, is known as an attribute. This protocol allows attribute to be
> self identifying using UUIDs to identify the type of data.
>
> Attribute protocol messages are sent over L2CAP channels, known as the _ATT bearers_.
>
> Attribute protocol defines two roles: Client and Server

### GAT

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

### Generic Access Profile (GAP)

> Application interoperability in the Bluetooth system is accomplished by Bluetooth profiles. Bluetooth profiles define the
> required functions and features of each layer in the Bluetooth system from the PHY to L2CAP and any other protocols
> outside of this specification ...
>
> ... The Bluetooth system defines a base profile which all Bluetooth devices implement. This profile is the Generic Access
> Profile (GAP), which defines the basic requirements of a Bluetooth device.

* Descibes:
    * Device roles.
        * Broadcaster - (Beacon) A device that sends advertising packets. Does not use connectable ad packets - no one can connect to a broadcaster.
        * Observer    - Device that scans for broadcasters and reports this information to an app.
        * Peripheral  - Device that advertises by using connectable advert packets.
        * Control     - Device that initialates connections to peripherals.
    * Device roles
    * Advertisement
    * Connection establishment

|          | Broadcaster                 | Observer                       | Peripheral          | Control            |
|----------|-----------------------------|--------------------------------|---------------------|--------------------|
| Radio    | Radio receiver not required | Radio transmitter not required | Both required       | Both required      |
| Transfer | One way data                | One way data                   | Two way data        | Two way data       |
| Stack    | Reduced h/w and stack       | Reduced h/w and stack          | Full h/w and stack  | Full h/w and stack |

In the advertising stateL

* Device sends out packets at fixes intervals.
* Same packet transmitted on each of the 3 primary advertisement channels.
    * Primary channel limited to 31 bytes
    * Secondary limited to 254 bytes
* Scan request and response to send additional data that exceeds above limits. This is _active scanning_
    * Receiving scans for advertisment data and sends a _scan request_
    * Advertiser provides _scan response_ if supported.
* _Passive scanning_ is where the device just listends for advertisment data without sending scan requests subsequently.



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
