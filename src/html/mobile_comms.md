## Terminology

| Acronym | Meaning |
|---------|---------|
| GSM     | Global Systems for Mobile |
| GPRS    | General Packet Radio Service |
| EDGE    | Enhanced Data Rate for GSM Evolution |
| UMTS    | Universal Mobile Telecommunications System |
| HSPA    | High Speed Packet Access |
| HSPA+   | Evolved High Speed Packet Access |
| EVDO    | EVolution Data optimized |
| LTE     | Long Term Evolution (of mobile networks) |
| NR      | New Radio |
| MS      | Mobile Station: your phone |
| BTS     | Base Transceiver System - aka Base Station |
| IMEI    | International Mobile Equipment Identity - Think MAC address of slot SIM is inserted into |
| IMSI    | International Mobile Subscriber Identity - Unique identifier assigned to every SIM  |
| ICCID   | Integrated Circuit Card Identifier - Identifies the chip of each SIM card. |
| MSISDN  | Mobile Station International Subscriber Directory - Full mobile number with country code and all prefixes. |
| TAU     | Tracking Area Updating period |
| PSM     | Power Saving Mode |
| UE      | User Equipment |



## Different Mobile Comms Standards

|      | Standards                                | Technology | SMS | Voice Switching | Data Switching       | Data Rates                               |
|------|------------------------------------------|------------|-----|-----------------|----------------------|--------------                            |
| 1G   | AMPS, TACS                               | Analog     | No  | Circuit         | Circuit              | N/A                                      |
| 2G   | GSM, CDMA, EDGE, GPRS                    | Digital    | Yes | Circuit         | Circuit / Packet (1) | GSM ~22.8Kpbs<br>CDSM ~14.4 Kbps (single channel)<br> GRPS ~50Kbps<br>EDGE ~150Kbps |
| 3G   | UTMS, CDMA2k, HSPA, EVDO                 | Digital    | Yes | Circuit         | Packet               | UMTS/HSPA ~10Mbps<br> UMTS/HSPA+ ~20Mbps |
| 4G   | LTE, LTE advanced, IEEE 802.16 (WiMax)   | Digital    | Yes | Packet          | Packet               | LTE 20-50Mbps<br>LTE advanced ~1Gbps     |
| 4/5G | LTE-M (aka Cat-M1), NB-IoT (aka Cat-NB1) | Digital    | ?   | ?               | ?                    | ?                                        |
| 5G   |                                          | Digital    | Yes | Packet          | Packet               | ~20 Gbps                                 |
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
* EDGE = Enhanced Data Rate for GSM Evolution
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


* Uplink v.s. Downlink
    * Uplink is connection from Mobile Station (MS), i.e., your phone, to the Base Station, a.k.a. Base Transceiver System (BTS)
    * Downlink is BTS to MS comms.
    * MS uses full duplex comms.

* A combination of FDMA and TDMA is used to allow a BTS to communicate with many MS: The channels, split by frequency, are also time divided.

* FM Frequency Modulation was 1G. All later technologies used different methods.
* FSK - Frequency Shift Keying 
* PSK - Phase Shift Keying
* QPKS - Quadrature PSK
* QAM - Quadrature Amplitude Modulation - varies both amplitude and phase to get more bits per symbol.

European Commission has good infographic:
<img alt="European Commission has good infographic" src="https://ec.europa.eu/newsroom/dae/document.cfm?doc_id=4541" style="width: 50%"/>

### 1G
* 3 variants used:
    * Advanced Mobile Phone (AMP). USA.
    * Noridic Mobile Telephone (NMT). Scandinavia.
    * Total Access Communications (TAC). Europe.
* All used FDMA with analog FM.
* Weak security and no roaming.

### 2G
* GSM developed in 1991 by European Telecomms Standards Institute (ETSI).
    * Combination of FDMA and TDMA used.
* Ditigal AMP used in USA.
* Supported packet switching, roaming, encryption, SMS and data.

### 3G


## Network Architectures



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
These are just quick notes on some commands for quick reference. Not trying to duplicate the manual here so for details look at modem manual.

AT commands take the following format:



### Standard

<table class="jehtable">
    <thread>
        <td>Command</td><td>Description</td>
    </thread>
    <tbody>
<!--
        <tr>
            <td><code></code></td>
            <td><p></p></td>
        </tr>
-->
        
        <tr>
            <td><p><code>AT+CREG</code></p></td>
            <td><p>GSM network registration status/report.</p>
                <p>The <i>set</i> command configures whether URCs are emitted by the modem. E.g., the set command <code>AT+CREG=2</code> enables network registration URCs, which will include network cell ID data. An example of such a URC could be <code>+CREG: 5,"090C","0696",3</code>, where <code>5</code> is the status (in this case registered, roaming), 
                   <code>"090C"</code> is the Local Area Code (LAC) and `"0696"` is the Cell ID. `3` is the `AcTSatus` (a Ublox specific thing maybe?) and indicates that the
                   RAT being used is GSM/GPRS.
                </p>
                <p>The <i>read</i> command reports the current mode and network registration status.
                </p>
            </td>
        </tr>

        <tr>
            <td><p><code>AT+CGREG</code></p></td>
            <td><p>GPRS network registration status/report.</p>
                <p>Very similar to `AT+CREG` but for GRPS networks
            </td>
        </tr>


        <tr>
            <td><p><code>AT+CEREG</code></p></td>
            <td><p>LTE/EPS network registration status/report</p></td>
        </tr>

        <tr>
            <td><p><code>AT+CIMI</code></p></td>
            <td><p>Request the IMSI (International Mobile Subscriber Identity).</p></td>
        </tr>


        <tr>
            <td><p><code>AT+CPSMS</code></p></td>
            <td><p>Power Saving Mode (PSM) settings.</p>
                <blockquote>
                    <p>IoT devices typically send or receive data intermittently. Between periods of data transmission and reception, a device can sleep to minimize power consumption and maximize battery charge. The energy cost of completely detaching from the network at sleep, then re-attaching upon wake is high, so LTE allows the device to maintain its network attachment during sleep. However, the host network will periodically page the device, which needs to wake and respond. The device will then sleep again until it receives the next page or has to wake to send data.
                    </p>
                    <p>This wake-respond-sleep process consumes only a small amount of energy, but its cumulative energy consumption can become significant over the lifetime of a device. Power Save Mode addresses this by letting IoT devices agree to an extended sleep period with the network. During this time, the network doesn't page the device, which can then wake only when it needs to send data or when the sleep period expires.
                    </p>
                    <p>...
                    </p>
                    <p>In an active PSM period, the modem's radio is fully shut down and the device cannot send data or be reached. During development, you should be aware that the device's AT channel may also be closed down.
                    </p>
                    <p>Data intended for the sleeping device is buffered: 3GPP requirements mandate that data packets must be stored by the network. 
                    </p>
                    <footer>-- <a href="https://www.twilio.com/docs/iot/supersim/low-power-optimization-for-cellular-modules" target="_blank">Low-power Optimization for Cellular Modules</a>, Twilio.</footer>
                </blockquote>
                <p>They had en even better explanation in another of their blogs:</p>
                <blockquote>
                    <p>Power Saving Mode (PSM) - The PSM feature allows an IoT device to sleep for extended periods of time without being woken up by network paging. Typical cellular devices actively transition between two modes – IDLE and ACTIVE. When the device is not sending/receiving traffic it goes IDLE, which has a positive effect on battery life. If there are IP packets that need to be delivered to the device, the network pages for the device. The device must respond to the page and transition to ACTIVE mode to receive the traffic. This has an impact on IoT devices that are power-constrained. PSM allows these IoT devices to negotiate an extended sleep period (hours or days) with the network and avoid being paged during that sleep cycle. If there is any traffic that arrives for the device during the sleep period, the traffic is buffered in the network (at least the last 100 bytes) and delivered when the device becomes ACTIVE.</p>
                    <footer>-- <a href="https://www.twilio.com/blog/when-to-use-lte-cat-m" target="_blank">When to Use LTE Cat M for IoT Devices</a>Twilio blog.
                    </footer>
                </blockquote>
                <p></p>
            </td>
        </tr>

        <tr>
            <td><p><code>AT+CEDRXS</code></p></td>
            <td><p>
                    Use extended discontinuous reception (eDRX) parameters. EDRX is an extension of the DRX feature that is used by IoT devices to reduce power consumption. <q>DRX is a mechanism in which a device goes into sleep mode for a certain period and then wakes up after a fixed interval to receive signals. The basic principle for eDRX is to extend DRX cycles to allow a device to remain in a power-saving state for a longer period of time</q> -- <a href="https://www.everythingrf.com/community/what-is-edrx" target="_blank">[REF]</a>.
                </p>
                <p>
                    Twilio has the following to say about the difference between PSM and eDRX:
                </p>
                <blockquote>
                    <p>While not providing the same levels of power reduction as PSM, eDRX can offer a good compromise between device reachability and power consumption. eDRX can be used alongside PSM to obtain additional power savings, or it can be used on its own.
                    </p>
                    <p>PSM is more power efficient because PSM cycles are much longer than eDRX cycles. As a result, the device can enter into a deeper, lower power sleep state with PSM than it can with eDRX.
                    </p>
                    <footer>-- <a href="https://www.twilio.com/docs/iot/supersim/low-power-optimization-for-cellular-modules" target="_blank">Low-power Optimization for Cellular Modules</a>, Twilio.</footer>
                </blockquote>
                <p>Their blog also gives a nice little bit of extra detail:
                </p>
                <blockquote>
                    <p>PSM and eDRX are complementary and can both be used by a Cat M device. eDRX helps the device sleep a bit longer, wake up at fixed intervals, and generally reduce "chattiness" between the device and the network. PSM helps the device sleep for much longer - hours or days.</p>
                     <footer>-- <a href="https://www.twilio.com/blog/when-to-use-lte-cat-m" target="_blank">When to Use LTE Cat M for IoT Devices</a>Twilio blog.
                     </footer>
                </blockquote>
                <p></p>
            </td>
        </tr>


        <tr>
            <td><p><code>AT+CPSMS</code></p></td>
            <td><p>Power saving mode settings</p></td>
        </tr>

        <tr>
            <td><p><code>AT+CGDCONT</code></p></td>
            <td><p>Packet Data Protocol (PDP) context definition: Packet Data Protocol (PDP) context is a data structure that allows the device to transmit data using Internet Protocol. Eg APN name, IP address etc.</p></td>
        </tr>

        <tr>
            <td><p><code>ATI0</code></p></td>
            <td><p>Module information: Module type number request.</p></td>
        </tr>

        <tr>
            <td><p><code>ATI9</code></p></td>
            <td><p>Firmware information: Modem and application version request.</p></td>
        </tr>

        <tr>
            <td><p><code>AT+CCID</code></p></td>
            <td><p>Returns the ICCID (Integrated Circuit Card ID) of the SIM-card. ICCID is a serial number identifying the SIM.</p></td>
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
            <td><p><code>AT+COPS</code></p></td>
            <td><p>The `+COPS` command selects a Public Land Mobile Network (PLMN) automatically or manually, and reads and searches the current mobile network.</p></td>
        </tr>
  
    </tbody>
</table>


### U-Blox

<table class="jehtable">
    <thread>
        <td>Command</td><td>Description</td>
    </thread>
    <tbody>
<!--
        <tr>
            <td><code></code></td>
            <td></td>
        </tr>
-->

       

        <tr>
            <td><code>AT+UANTR</code></td>
            <td>Antenna detection: measure DC component of load of cellular antenna.</td>
        </tr>

        <tr>
            <td><code>AT+UAUTHREQ</code></td>
            <td></td>
        </tr>

        <tr>
            <td><code>AT+USIMSTAT</code></td>
            <td>Configure the SIM state reporting so that the unsolicited result code (URC) reports the (U)SIM toolkit REFRESH proactive command execution result</td>
        </tr>

        <tr>
            <td><code>AT+UMNOPROF</code></td>
            <td>Set Mobile Network Operator (MNO) profile - i.e., select the MNO type to connect to.</td>
        </tr>

        <tr>
            <td><code>AT+UFACTORY</code></td>
            <td>Restore factory configuration ... executed only at the next module boot</td>
        </tr>
    </tbody>
</table>


## TODOs
* SIM Toolkit https://www.techopedia.com/definition/30501/sim-toolkit-stk#techopedia-explains-sim-toolkit-stk
              https://web.archive.org/web/20061207010523/http://www.cellular.co.za/sim_toolkit.htm
              ***** https://www.etsi.org/deliver/etsi_ts/131100_131199/131111/13.03.00_60/ts_131111v130300p.pdf
* Proactive SIMs https://deepsec.net/docs/Slides/2021/Proactive_SIMs_David_Burgess.pdf
* FOTA - Frimware-Over-The_air https://www.soracom.io/iot-definitions/what-is-firmware-over-the-air-fota/