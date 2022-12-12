
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
  * R14 is the *Link Register* (LR)
    * Enables return from subroutines
    * Special function for exception handling
  * R15 is the *Program Counter* (PC): Points to the address of the code being **fetched** from memory at this moment.
    * When jumping +1 to address when executing Thumb-2 instructions (e.g. accessing 0x1000 warite 0x1001 to PC) - its a wierd ARM thing - because ARM has hijacked bit 0 of the instruction address bus internally within the core (externally always see addredd 0x1000) and used as a way to configure the execution state of the processor. Decides which instruction set the instruction belongs to - 32-bit ARM instructions or 16-bit Thumb-2 sintructions. Bit 0 of instruction address bus is connected to T-bit of the state control register - it tells the core what type of instruction it is decoding.
      > The CPSR register holds the processor mode (user or exception flag), interrupt mask bits, condition codes, and Thumb status bit. The Thumb status bit indicates the processor’s current state: 0 for ARM state (default) or 1 for Thumb. -- https://www.embedded.com/introduction-to-arm-thumb
    * Its of no use for Cortex-M processors as they only have Thumb-2, but, still need to jump with +1 on the address! Hey ho!
    * And then... M33 then the T-bit apparently has another meaning so gets more complicated?
  * Speical purpose
      * Processor status (xPSR) - Combined Program Status Register - contains, in one register, the following 3 "registers":
            * Indicate the state of the core right now.
            * APSR - Application Program Status Register - Only APSR flags can be uysed for confition execution (`BCC, `IT`).
              ```
              31                                                                             5              0
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              |N |Z |C |V |                                     Reserved                                      |
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              ```
            * FPSCR - Float flags (if FPU present).
              ```
              31                                                                       7  6  5  4  3  2  1  0
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              |N |Z |C |V |  |  |DN|FZ|     |                    Reserved             |  |     |  |  |  |  |  |                
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
                          |  |        vvvvv                                            | vvvvv  |  |  |  |  |
              Reserved ----+  |        RMode                                            |   |    |  |  |  |  +--- IOC
                      AHP ----+                                                         |   |    |  |  |  +------ DZC
                                                                                        |   |    |  |  +--------- OFC
                                                                                        |   |    |  +------------ UFC
                                                                                        |   |    +--------------- IXC
                                                                                        |   +-------------------- Reservered
                                                                                        +------------------------ IDC
              ```
            * IPSR - Contains interrupt/exception number.
              ```
              31                                                                             5              0
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              |                                 Reservered                                  |   ISR Number    |
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              ```
            * EPSR - Contains Execution Status.
              ```
              31                   24                                                                       0
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              |     Reservered     |T |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              ```
            * APSR/IPSR/EPSR accessed as one register via xPSR. For example
              when an interrupt occurs, the xPSR is one of the resisters that is auto stored on the stack and looks like this:
              ```
              31                 24                                                          5              0
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              |N |Z |C |V |xxxxx|T |                       Reserved                         |    ISR Number   |
              +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
              ```
      * CONTROL: Stacks and privilege.
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

  |          | Priv                                                          | User                                             |
  |----------|---------------------------------------------------------------|--------------------------------------------------|
  | Handler  | Interrupt handlers & OS code - MSP (R13) - Can*not* use PSP!  | Not allowed                                      |
  | Thread   | Any code - MSP (R13) *or* PSP (but not usually)               | Any code - MSP (R13) *or* PSP (but not usually)  |
  
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




