## GPIB / IEEE-448, USBTMC, VISA, SCPI... What Does It All Mean?

### References
* (GPIB Tutorial, NI)[http://lmu.web.psi.ch/docu/manuals/software_manuals/GPIB/GPIB_tutorial.pdf]
* (Making Sense of Test and Measurement Protocols)[https://tomverbeure.github.io/2020/06/07/Making-Sense-of-Test-and-Measurement-Protocols.html]
* (GPIB 101 - A Tutorial About The GPIB Bus)[https://www.icselect.com/pdfs/ab48_11%20GPIB-101.pdf]


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
<footer>-- (GPIB 101 - A Tutorial About The GPIB Bus)[https://www.icselect.com/pdfs/ab48_11%20GPIB-101.pdf]</footer>
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
<footer>-- (GPIB Tutorial, NI)[http://lmu.web.psi.ch/docu/manuals/software_manuals/GPIB/GPIB_tutorial.pdf]</footer>
</blockquote>
<p></p>

