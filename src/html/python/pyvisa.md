## GPIB / IEEE-448, USBTMC, VISA, SCPI... What Does It All Mean?

### References
* (GPIB Tutorial, NI)[http://lmu.web.psi.ch/docu/manuals/software_manuals/GPIB/GPIB_tutorial.pdf]
* (Making Sense of Test and Measurement Protocols)[https://tomverbeure.github.io/2020/06/07/Making-Sense-of-Test-and-Measurement-Protocols.html]

### GPIB


GPIB is an old standard for *test and measurement equipment* interfaces, which was standardised by the IEEE as
IEEE-448.1 and IEEE-448.2.

IEEE-448.1 is a physical layer specification that sought to make common the physical interfaces between test and
measurement devices so that users could more easily communicate with different bits ok kit.

IEEE-448.2 is a command specification whose goal was to make the control of different instruments more portable. So,
for example, if you had programmable power supply from vendor A and switched to an equally capable supply from vendor B,
you should be able to port your software - there should be less difference in command structures and data formats between
IEEE-488.2 compliant devices.

IEEE-488.2 defines the following mandator common commands:

| Mnemonic | Group            | Description                       |
|----------|------------------|-----------------------------------|
| *IDN?    | System Data      | Identification query              |
| *RST     | Internal         | Operations Reset                  |
| *TST?    | Internal         | Operations Self-test query        |
| *OPC     | Synchronization  | Operation complete                |
| *OPC?    | Synchronization  | Operation complete query          |
| *WAI     | Synchronization  | Wait to complete                  |
| *CLS     | Status and Event | Clear status                      |
| *ESE     | Status and Event | Event status enable               |
| *ESE?    | Status and Event | Event status enable query         |
| *ESR?    | Status and Event | Event status register query       |
| *SRE     | Status and Event | Service request enable            |
| *SRE?    | Status and Event | Service request enable query      |
| *STB?    | Status and Event | Read status byte query            |

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

