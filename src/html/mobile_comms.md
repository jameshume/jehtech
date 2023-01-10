## Different Mobile Comms Standards

|    | Standards                         | Technology | SMS | Voice Switching | Data Switching       | Data Rates   |
|----|-----------------------------------|------------|-----|-----------------|----------------------|--------------|
| 1G | AMPS, TACS                        | Analog     | No  | Circuit         | Circuit              | N/A          |
| 2G | GSM, CDMA, EDGE, GPRS             | Digital    | Yes | Circuit         | Circuit / Packet (1) | 236.8 kbps   |
| 3G | UTMS, CDMA2k, HSPDA, EVDO         | Digital    | Yes | Circuit         | Packet               | 384 kbps     |
| 4G | LTE advanced, IEEE 802.16 (WiMax) | Digital    | Yes | Packet          | Packet               | up to 1 Gbps |
[[Ref]](https://www.javatpoint.com/history-of-wireless-communication)

(1) GPRS is a packet-switched network and GSM is a circuit-switched network [[Ref]](https://byjus.com/gate/difference-between-gsm-and-gprs/#:~:text=The%20GSM%20is%20a%20circuit,packet%2Dswitched%20type%20of%20network.&text=The%20GSM%20technology%20provides%20a,for%20all%20of%20its%20users.)



See:

* [Difference Between GSM and GPRS](https://byjus.com/gate/difference-between-gsm-and-gprs/#:~:text=The%20GSM%20is%20a%20circuit,packet%2Dswitched%20type%20of%20network.&text=The%20GSM%20technology%20provides%20a,for%20all%20of%20its%20users.))
* [What are phone bands (GSM, CDMA) and why do they matter?](https://www.verizon.com/articles/Smartphones/what-are-phone-bands-and-why-do-they-matter/#:~:text=What%20does%20the%20CDMA%2FGSM,to%202G%20and%203G%20connectivity.)
* [What is EDGE (Enhanced Data Rate for GSM Evolution)?](https://www.tutorialspoint.com/what-is-edge-enhanced-data-rate-for-gsm-evolution#:~:text=EDGE%20allows%20for%20a%20faster,work%20on%20any%20GPRS%20network.)


Notes:

* GSM = Global Systems for Mobile
    * Standard bearer of 2G tech,
    * Introduced Simple Messaging Service (SMS),
    * Circuit switched,
    * Can make voice calls and transmit data at the same time,
    * Most widely used standard (CDMA is US and Asia)
* GPRS = General Packet Radio Service
    * Upgrade to GSM: Standard bearer of 2.5G tech
    * Packet switched,
    * Introduced Multimedia Messaging Service (MMS),
    * Can make voice calls and transmit data at the same time.
* EDGE = Enhanced Data Rate for FSM Evolution
    * Improves upon the GSM/GPRS family: higher bit-rates per radio channel: 2.75 tech.
* CDMA = Code Division Multiple Access
    * Can *_not_* make voice calls and transmit data at the same time,
    * GSM is widely used across the world, CDMA is mostly only common in the US/Asia
* UMTS = Universal Mobile Telecommunications System
    * Fully compatible with GSM, but
    * Required upgrades to existing 2G networks (whether GSM, GPRS or EDGE) as UMTS uses different access technology (WCDMA) - new base stations required.
* HSPA = High Speed Packet Access
    * Tech used to enhance UMTS to improve data rates.
    * Combination of HSUPA (High Speed Uplink Packet Access) and HSDPA (High Speed Downlink Packet Access)
    * "3G+" or "H" icon on phone.
* HSPA+ = Evolved High Speed Packet Access
* EVDO = EVolution Data optimized
    * Used in CSMA networks.
    * Equivalent in GMS/UMTS networks is HSPA.
* LTE = Long Term Evolution (of mobile networks)
    * 4G
* NR = New Radio
    * 5G


## SIM and Phone Identifiers
See [Difference Between IMEI, IMSI, ICCID And MSISDN Numbers](https://commsbrief.com/difference-between-imei-imsi-iccid-and-msisdn-numbers/) By Adnan Ghayas.

| Acronym | Meaning                                           | Linked to | Format                                                | Description                                                                                           |
|---------|---------------------------------------------------|-----------|-------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| IMEI    | International Mobile Equipment Identity           | Phone     |  15 numbers                                           | Unique identifier assigned to every cellular device for each of its SIM *slots*.                      |
| IMSI    | International Mobile Subscriber Identity          | SIM       |  15 numbers  (1)                                      | Unique identifier assigned to every SIM *card*.                                                       |
| ICCID   | Integrated Circuit Card Identifier                | SIM       | ~20 numbers  (2)                                      | Identifies the chip of each SIM card.                                                                 |
| MSISDN  | Mobile Station International Subscriber Directory | SIM       |                                                       | Full mobile number with country code and all prefixes.                                                |


(1) Format is `CCCNNIIIIIIIIII`, where `C` (the first 3 digits) are the mobile country code, `N` (the next 2 digits) are the mobile network code and the last 10 digits, `I`, are the Mobile Subscriber Identification Number. The <q>mobile network may use a temporary IMSI called TMSI (Temporary Mobile Subscriber Identity) instead of IMSI to ensure the subscriber's confidentiality</q>.

(2) Usually 19 or 20 digits. Format is similar to `IICCSSSSUUUUUUUUUUU`, where `I` is the industry code, `C` is the country code, `S` is the issuer's code, and `U` is the unique identifier for the SIM.


## Signal Strength
* See [[Ref]](https://www.metageek.com/training/resources/understanding-rssi/)

### RSSI
* A relative measure
* Values in range [0, 255], *however* each chipset vendor can choose their own maximum value within this range, so RSSI numbers between vendors *may not* be comparable!
* Use dBm for a comparable metric.

### dBm
* See [Electronics:decibels](electronics.html) for a definition.
    * Summary: dBm is gain relative to a reference power of 1mW. 10 dBm means the signal has a power x10 greater than 1mW.
* What dBm constitutes "good" or "bad" is rather dependent on the carrier - hence the number of bars meaning different things per carrier.
  Arbitrarily using this [[as a reference]](https://www.signalsolutions.co.uk/blog/when-the-bars-are-high-but-the-signal-is-low/):
      * -50 to -79 dBm = great signal, full bars (4 to 5 bars).
      * -80 to -89 dBm = good signal (3 to 4 bars).
      * -90 to -99 dBm = average signal (2 to 3 bars).
      * -100 to -109 dBm = poor signal (1 to 2 bars).
      * -110 to -120 dBm = very poor signal or not-spot (0 to 1 bar).


## AT Commands

### Standard

<table class="jehtable">
    <thread>
        <td>Command</td><td>Description</td>
    </thread>
    <tbody>
        <tr>
            <td><code></code></td>
            <td></td>
        </tr>

        <tr>
            <td><code>ATI0</code></td>
            <td>Module information: Module type number request</td>
        </tr>

        <tr>
            <td><code>ATI9</code></td>
            <td>Firmware information: Modem and application version request</td>
        </tr>

        <tr>
            <td><code>AT+CCID</code></td>
            <td>Returns the ICCID (Integrated Circuit Card ID) of the SIM-card. ICCID is a serial number identifying the SIM.</td>
        </tr>

        <tr>
            <td><code>AT+CRSM</code></td>
            <td>
                <p>Restricted SIM access: Allows easy access to the SIM database by sending SIM commands as defined in [ETSI TS 102221](https://www.etsi.org/deliver/etsi_ts/102200_102299/102221/15.00.00_60/ts_102221v150000p.pdf)
                </p>
                <p>For example, the command `AT+CRSM=176,28486,0,0,17` is a read binary command (176), reading elementary file (EF) identified by ID `28486 (0x6F46)` (EFs described in [3GPP TS 31.102](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=1803)). From the spec, on can see that `6F4F` is the service provider name (EF<sub>SPM</sub>). Both P1 and P2 are zero indicating no offset is applied.
                </p>
            </td>
        </tr>

        <tr>
            <td><code>AT+COPS</code></td>
            <td>Force an attempt to select and register with the GSM/LTE network operator or query network registered with.</td>
        </tr>
  
    </tbody>
</table>


### U-Blox

<table class="jehtable">
    <thread>
        <td>Command</td><td>Description</td>
    </thread>
    <tbody>
        <tr>
            <td><code></code></td>
            <td></td>
        </tr>

        <tr>
            <td><code>AT+UMNOPROF</code></td>
            <td>Set Mobile Network Operator (MNO) profile - i.e., select the MNO type to connect to.</td>
        </tr>

        <tr>
            <td><code>AT+UFACTORY=&lt;fs_op&gt;,&lt;nvm_op&gt;</code></td>
            <td>Restore factory configuration ... executed only at the next module boot</td>
        </tr>
    </tbody>
</table>