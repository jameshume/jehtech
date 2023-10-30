## Useful
* [Proceedure Call Standard for the Arm(R) Architecture](https://github.com/ARM-software/abi-aa/blob/2982a9f3b512a5bfdc9e3fea5d3b298f9165c36b/aapcs32/aapcs32.rst#procedure-call-standard-for-the-arm-architecture)
* [Cortex-M4 Devices Generic User Guide](https://developer.arm.com/documentation/dui0553/latest/)
* [Cortex-M4 Technical Reference Manual](https://documentation-service.arm.com/static/5f19da2a20b7cf4bc524d99a)
* [ARM Cortex-M RTOS Context Switching](https://interrupt.memfault.com/blog/cortex-m-rtos-context-switching)
* [GitHub Project - minimal-c-cortex-m: A minimal Arm Cortex-M example, including semihosting...](https://github.com/noahp/minimal-c-cortex-m)
* [CPUlator](https://cpulator.01xz.net/?sys=arm-de1soc)

## Intro

* Main ARM series: R for **R**eal-time processors, A for **A**pplication processors, M for **M**icrocontroller processors.
    * Pipelines: A has long, R long/medium, M short.
    * M is ultra low power and deterministic.
        * MPU, NVIC, Wakeup Interrup Contrller WIC, ARM TrustZone security extensions.
        * Cortex-M0(+) - Smallest most energy efficient processors. M0+ has vector relocation feature and single cycle I/O interface.
            * Cortext-M23 - Similar to M0+. Better engergy efficiency and supports TrustZone extension.
            * Uses the ARM-v6-M architecture.
        * Cortex-M4 - Small but powerful for low-power ucontrollers. Has hardware divider and MAC instructions. Debug and trace features. DSP. SIMD instruction. Option hardware single precision float support. Uses ARM-v7-M architecture.
        * Cortext-M7 - High performance. Supports double precision floating point standard. Cache and TCM.
        * Instructions sets
            * 32-bit ARM
            * 16-bit Thumb. Introducedin 1995 as 32-bit instructions took more space and power. Both 16-bit and 32-bit instructions sets supported. 16-bit had oood code density. Supporting both impacted performance.
            * 16-bit and 32-bit Thumb-2
                * Introduced in 2003. Keeps the code density of the Thumb instruction set and the performance of the 32-bit set. Most processors now only support the Thumb-2 instruction set (>= M0).

* CortexM's all use Thumb-2 instruction set.
    * NO ARM instruction set support
    * No Coprocessor 15: The coprocessor was used to configure the main processor. Cortex-M devices do not have this. Instead all the registers are memory-mapped to reserved regions of memory.
    * Vector table is a set of addresses, *not* instructions.
        * Typical ARM vector tables would be a table of jump instructions.
* Cortex-M23/M33 : ARMv8.
* Cortex-M3      : ARMv7-M, 3-stage pipeline.
    * Mosty 32-bit instructions
* Cortex-M7      : ARMv7-M, 6 stage pipeline.
    * Mosty 32-bit instructions
* Cortex-M0+     : Less than 12k gates (what the M0 "should have been").
    * ARM-v6-M architecture (16-bit Thumb, except system instructions). Majority 16-bit instructions, some 32-bit instructions like `BL`, for example.
    * 2-stage pipeline (M0 has 3-stage)
    * Optional User/priviledged support
    * Optional MPU with 8 regions.
    * AHB-Lite master interface
    * Optional low-latency I/O port. Read and writes are done in a *single cycle*. Address and data in one cycle. All other ARM protocols use a minimum of two cycles. Typically used for GPIO operations.
    * Optional support for a WIC controller for increased power saving.
* Cortex-M0/M0+  : Designed for LOW POWER.
    * Majority 16-bit instructions, some 32-bit instructions like `BL`, for example.
    * M0's are aimed at replacing PICs in the market place.
    * No hardware divide.
    * Hardware multiplier is optional.
    * M0+ only: uTrace: use internal SRAM as a trace buffer - record the execution of the program into the trace buffer and then use debugger to access buffer.
    * Von-Neumann architecture (Other Cortex-Ms use Harvard achitecture.)
* Cortex-M chips use Thumb-2 instruction set *only*.
* v6-M --> V7-M : ~50 instructtions --> ~200 instructions - sizeable increase.
* M4 is like an M3 with instructions for DSP - SIMD and a single-precision FPU optionally. Some operator improvement for efficiency.
* No instruction cache (except M7)

## Programmers Model
* Explains the interface programmer must use to design their application on a specific processor.
* Registers:
    * General Pupose
        * R0-R7: Accessible to all instrunctions
        * R8-R12: Accessible to a few 16-bit instructions and all 32-bit instuctions
    * R13 is *Stack Pointer* (SP)
        * Armv7-M cores have two banked versions. There are two stack pointers.
            * Don't have to use both but can choose to use both.
            * MSP - Main Stack (R13) (Out of reset MSP is active)
            * PSP - Process Stack (priviledged)
        * Points to the last entry in the stack, going down in the address range.
        * R13 is an alias for the *currently active* stack. So if MSP is currently activated, R13 references the MSP, but if PSP is activated then R13 references the PSP. To activate one or the other, use the CONTROL register.
      * Stack pointer **must be 8 or 4 byte aligned**. I.e. can only stack words or double words. But when you **call** a function the SP should be **8 byte aligned**!
      * SP points to the top of the stack.
      * Stack **grows downwards (full descending)**, i.e. the bottom of the stack is at address X and the top of the stack is at address X - STACK_SIZE. So, grows downwards means grows into lower/smaller address values as items are pushed.
          * E.g. If SRAM is 0x2000_0000 to 0x2000_7FFF then at start SP is 0x2000_8000, so that the first push will be to 0x2000_7FFC (remember SP must be at least word aligned).
      * Passing parameters by stack is inefficient (if more that 4 parameters to a function). Accessing stack memory, because most Cortex-M have no cache, involves memory access - costly in time and power consumption as outside bus is used.
            * If at all possible on your architecture, cache the stack memory!
    * R14 is the *Link Register* (LR)
        * Enables return from subroutines
        * Special function for exception handling
    * R15 is the *Program Counter* (PC): Points to the address of the code being **fetched** from memory at this moment.
        * When jumping +1 to address when executing Thumb-2 instructions (e.g. accessing 0x1000 warite 0x1001 to PC) - its a wierd ARM thing - because ARM has hijacked bit 0 of the instruction address bus internally within the core (externally always see addredd 0x1000) and used as a way to configure the execution state of the processor. Decides which instruction set the instruction belongs to - 32-bit ARM instructions or 16-bit Thumb-2 sintructions. Bit 0 of instruction address bus is connected to T-bit of the state control register - it tells the core what type of instruction it is decoding.
            > The CPSR register holds the processor mode (user or exception flag), interrupt mask bits, condition codes, and Thumb status bit. The Thumb status bit indicates the processor’s current state: 0 for ARM state (default) or 1 for Thumb. -- https://www.embedded.com/introduction-to-arm-thumb
        * Its of no use for Cortex-M processors as they only have Thumb-2, but, still need to jump with +1 on the address! Hey ho!
        * And then... M33 then the T-bit apparently has another meaning so gets more complicated?
    * Special purpose
        * Processor status (xPSR) - Combined Program Status Register - contains, in one register, the following 3 "registers":
              * Indicate the state of the core right now.
              
              * APSR - Application Program Status Register - Only APSR flags can be used for condition execution (`BCC`, `IT`). In original ARM instruction set almost all instructions could be issued conditionally based on contents of APSR, but in Thumb-2 conditional execution is only supported using 16-bit branch instructions `B<c> addr`.
                ```
                             Not on M0
                31           |                                                                 5              0
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                |N |Z |C |V |Q |                                  Reserved                                      |
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                 |  |  |  |  |
                 |  |  |  |  Cumulative saturation
                 |  |  |  Overflow
                 |  |  Carry
                 |  Zero
                 Negative                              
                ```
              * FPSCR - Float flags (if FPU present).
                ```
                31                                                                       7  6  5  4  3  2  1  0
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                |N |Z |C |V |  |  |DN|FZ|     |                    Reserved             |  |     |  |  |  |  |  |                
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                            |   |        vvvvv                                            | vvvvv  |  |  |  |  |
                Reserved ----+  |        RMode                                            |   |    |  |  |  |  +--- IOC
                        AHP ----+                                                         |   |    |  |  |  +------ DZC
                                                                                          |   |    |  |  +--------- OFC
                                                                                          |   |    |  +------------ UFC
                                                                                          |   |    +--------------- IXC
                                                                                          |   +-------------------- Reservered
                                                                                          +------------------------ IDC
                ```
              * IPSR - Contains interrupt/exception number of the current ISR.
                ```
                31                                                                             5              0
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                |                                 Reservered                                  |   ISR Number    |
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                ```
              * EPSR - Contains Execution Status.
                  * M0
                  ```
                   31                   24                                                                       0
                  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                  |     Reservered     |T |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
                  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                  ```
                  * M4
                  ```
                   31                   24                         15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
                  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                  |  Reservered  |     |T |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
                  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                                  |||||                            |||||||||||||||||
                                  ICI/IT                                ICT/IT
                  ```

                The EPSR is not directly accessible. Two events can modify the EPSR:
                   1. an interrupt occurring during an LDM or STM instruction
                   2. execution of the If-Then instruction.

              * APSR/IPSR/EPSR accessed as one register via xPSR. For example
                when an interrupt occurs, the xPSR is one of the resisters that is auto stored on the stack and looks like this:
                ```
                31                 24                                                          5              0
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                |N |Z |C |V |xxxxx|T |                       Reserved                         |    ISR Number   |
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                ```
        * CONTROL: Stacks and privilege.
                ```
                31                                                                                            0
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                |                                       Reservered                                        |  |  |
                +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                                                                                                            |  |
                                                                                     SPEL (stack def) ------+  |
                                                                                                    nPRIV -----+

                ** Note **: A change requires an ISB!
                ```
        * PRIMASK (only Arm-v7), FAULTMASK (only Arm-v7), BASEPRI: Exception handling.
            * PRIMASK is a 1 bit register that when set blocks all interrupts other than the NMI and hard fault.
        * In unprivileged mode all special registers are read only except for the APSR. The EPSR is not accessible (reads zero) in all modes.  IPSR is always RO.


## Architecture
An *architecture* defines <q>how the program execution should behave and how the debuggers interact with the processor</q>.

A *micro-architecture* defines <q>the exact implementation details of the processor, e.g. how many pipeline stages ... etc</q>.

* Modes, privilege and stacks
    * Handler Mode
        * Entered when taking any exception.
        * Always privileged.
        * Always uses main stack.
        * OS can run here.
        * Handles exceptions.
        * Processor returns to thread mode once exception processing finished.
        * Always priviledged.
    * Thread mode
        * Execute applications.
        * Processor enters thread mode (priviledged) at startup.
        * CONTROL register controls whether executions is privileged or un privileged.
        * Core enters thread mode out of reset.
        * Typically used for user app code.
        * Runs either priviliedged or unpriviliedged (should be configured by the reset handler).
        * Can use either main or process stack.
        * Typically uses process stack if Thread mode is unpriviledged.
        * User "apps" can run here.
        * On reset processor runs in thread mode.

![Table showing privilege levels v.s use of MSP and PSP](##IMG_DIR##/arm_priv_mode.png)

![State transistion for privilege and stack pointer selection](##IMG_DIR##/arm_sp_selection_and_priv_state_selection.png)
  
  + If we use PSP it is because we want to use it in user mode. MSP is meant to be used by an operating system. On a simple system that does not have such a separation it would probably just use the MSP.

* Priviledge levels:
    * Unprivileged:
        * Limited access to MSR (move general register to program status register (PSR)) and MRS (copy PSR to general register) instructions.
        * Cannot use change-process-state (CPS) instruction.
        * Cannot access sys timer, NVIC, or system control block.
        * Restricted access to peripherals.
        * Must use SVC instruction to make supervisor call to transfer priviledge levels.
    * Privileged:
        * Can use all instrutions and resources.
        * Can write to CONTROL register to change privilege level.
        * Out of reset you are in privileged mode.

* Interrupts and Exceptions
    * Optimized for low latency and good interrupt performance.
        * Auto save and restore of processor registers.
        * Implements all ARMv7-M low latency features - this is available on the M0(+) devices too.
            * Late arrival, tail-chaining, lazy FPU stacking, ICI bits for load/store multiple operations.
        * Aggressive fliushing of multi-cycle operations in pipeline.
            * To enable interrupt processing to start quickly.
            * Applies to all DEV/SO loads/stores that have bit vee started on the bus.
        * Avoids bursts on the bus for DEV/SO load/store multiples - may reduce bus performance.
    * Core includes Nested Vectored Interrupt Controller (NVIC).
    * Interrupt latency:
        * Typically 12 cycles.
        * 15+ cycles for M0.
  
* Power Management
    * Mostly SoC dependant.
    * Sleep modes:
        * SLEEPING.
        * DEEPSLEEP.
            * Controlled by system control reigsters.
            * Is software programmable (just states an intention - the job to actually go deep sleep is left to the SoC implementor to do).
        * WIC-based DEEPSLEEP.
        * 2 outputs: 1 to say "I am sleeping" and 1 to say "I am DEEP sleeping" so the SoC can see its state.
    * WFI, WFE and SEV instructions (wait fo rinterrupt/event and send event).
        * If you execute these the core goes into standby state an asserts the sleep signals so the SoC can see its state.
    * Sleep On Exit.
        * Sleep immediately on return from last ISR.
    * System clock is gated in sleep modes.
        * Sleep signal is exported allowing external systemn to be block gated.
        * NVIC interrupt interface stays awake.
    * Wake-Up Interrupt Controller (WIC).
        * Optional external wak-up detector allows core to be fully powered down.
        * Effecting with State-Retention Power Gating (SRPG) methodology.

## ABI

From []`aapcs32/aapcs32.rst``](https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst):

### Core Registers

<table class="jehtable">
    <thread>
        <tr>
            <td>Register</td> <td>Special</td> <td>Role in the procedure call standard</td>
        </tr>
    </thread>
    <tbody>
        <tr>r15</td> <td></td>   <td>PC      </td> <td>The Program Counter.</td></tr>
        <tr>r14</td> <td></td>   <td>LR      </td> <td>The Link Register.</td></tr>
        <tr>r13</td> <td></td>   <td>SP      </td> <td>The Stack Pointer.</td></tr>
        <tr>r12</td> <td></td>   <td>IP      </td> <td>The Intra-Procedure-call scratch register.</td></tr>
        <tr>r11</td> <td>v8</td> <td>FP      </td> <td>Frame Pointer or Variable-register 8.</td></tr>
        <tr>r10</td> <td>v7</td> <td>        </td> <td>Variable-register 7.</td></tr>
        <tr>r9 </td> <td>v6</td> <td>SB<br>TR</td> <td> Platform register or Variable-register 6.<br>The meaning of this register is defined by the platform standard.</td></tr>
        <td>r8 </td> <td>v5</td> <td>        </td> <td>Variable-register 5.</td></tr>
        <td>r7 </td> <td>v4</td> <td>        </td> <td>Variable-register 4.</td></tr>
        <td>r6 </td> <td>v3</td> <td>        </td> <td>Variable-register 3.</td></tr>
        <td>r5 </td> <td>v2</td> <td>        </td> <td>Variable-register 2.</td></tr>
        <td>r4 </td> <td>v1</td> <td>        </td> <td>Variable-register 1.</td></tr>
        <td>r3 </td> <td>a4</td> <td>        </td> <td>Argument / scratch register 4.</td></tr>
        <td>r2 </td> <td>a3</td> <td>        </td> <td>Argument / scratch register 3.</td></tr>
        <td>r1 </td> <td>a2</td> <td>        </td> <td>Argument / result / scratch register 2.</td></tr>
        <td>r0 </td> <td>a1</td> <td>        </td> <td>Argument / result / scratch register 1.</td></tr>
    </tbody>
</table>

### Stack

The ARM stack is <b>fully descending</b>. Descending means that it starts at a high address and each push <b>decrements</b> the stack pointer.

In a Full stack, <b>the stack pointer points to the topmost item in the stack, i.e.,the last item pushed into it</b>.
When pushing data into a Full stack, the stack pointer is first adjusted to reflect its new location and then
the data is stored in the stack at the address in the stack pointer.

The stack pointer must normally be 4-byte aligned, except at a "public interface", when it should be 8 byte, or double-word, aligned.
A "public interface" consists of the externally accessible functions offered by a library or component.

The stack frame is described in Figure B1-3 of the Armv7 Exception Model like so (when no FP registers saved):

![ArmV7 Stack Frame](##IMG_DIR##/../armv7_stack_layour_no_fp_regs.png)


## Instruction Set
* WARNING: `nop` not guaranteed to waste a cycle!!!! use `mv r0, r0` instead.
TODO
* Sync
    * WARNING DMB only works for one bus - 2 load/stores on 2 different busses do not have order of execution segregated by DMB as it only focuses on one bus and does not work across busses.
    * DSB is stricter than DMB - not just load/stores but intructions too - no futher instructions may complete execution or change interrupt masks until the Memory Barrier instruction completes. Including *implicit* operations - e.g. a cache controller refreshing its contents etc. Applies to *multiple* busses and *broadcasts to other cores in the cluster*.
    * See https://developer.arm.com/documentation/dai0321/a/?lang=en


## Setup GCC (Ubuntu)

* Download the toolchain from the [ARM website](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads). The the time of writing (Dec 2022) I downloaded 11.3.Rel1 as `arm-gnu-toolchain-11.3.rel1-x86_64-arm-none-eabi.tar.xz`.
* Extract this to a directory of your choice. You could use `/usr/share`, or `/opt/gcc-arm-none-eabi` for example. The following instructions were taken
  from [here](https://lindevs.com/install-arm-gnu-toolchain-on-ubuntu).
    ```
    sudo mkdir /opt/gcc-arm-none-eabi
    sudo tar xf arm-gnu-toolchain-11.3.rel1-x86_64-arm-none-eabi.tar.xz --strip-components=1 -C /opt/gcc-arm-none-eabi
    echo 'export PATH=$PATH:/opt/gcc-arm-none-eabi/bin' | sudo tee -a /etc/profile.d/gcc-arm-none-eabi.sh
    source /etc/profile
    ```
* Add the `bin` folder under your installation directory to the `PATH` environment variable.
* If you see the following when running GDB, install ncurses using `sudo apt install -y libncursesw5`.
    ```
    opt/gcc-arm-none-eabi/bin/arm-none-eabi-gdb: error while loading shared libraries: libncursesw.so.5: cannot open shared object file: No such file or directory
    ```
* If after installing ncurses it moans about Python, you don't have Python (3.8) installed! On Linux, Arm GNU toolchain provides GDB with Python support. It requires installation of Python 3.8 [[Ref]](https://lindevs.com/install-arm-gnu-toolchain-on-ubuntu). To install Python 3.8 specifically:
    ```
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt install -y python3.8
    ```

