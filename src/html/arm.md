
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
  * R13 is *Stack Pointer* (SP)
    * There are two stack pointers.
      * Don't have to use both but can choose to use both.
      * MSP - Main Stack (R13)
      * PSP - Process Stack (priviledged)
  * R14 is the *Link Register* (LR)
  * R15 is the *Program Counter* (PC): Points to the address of the code being **fetched** from memory at this moment.
  * Processor status
    * Indicate the state of the core right now.
    * APSR - Program Status Register - Only APSR flags can be uysed for confition execution (`BCC, `IT`).
    * FPSCR - Float flags (if FPU present).
    * IPSR - Contains interrupt/exception number.
    * EPSR - Contains Execution Status.

* Modes, privilege and stacks
  * Handler Mode
    * Entered when taking any exception
    * Always privileged
    * Always uses main stack
  * Thread mode
    * Core enters thread mode out of reset
    * Typically used for user app code
    * Runs either priviliedged or unpriviliedged (should be configured by the reset handler)
    * Can use either main or process stack
    * Typically uses process stack if Thread mode is unpriviledged

  |          | Priv                                                          | User                           |
  |----------|---------------------------------------------------------------|--------------------------------|
  | Handler  | Interrupt handlers & OS code - MSP (R13) - Can*not* user PSP! | Not allowed                    |
  | Thread   | Any code - MSP (R13) *or* PSP (but not usually+)              | Any code - MSP (R13) *or* PSP  |
  
  + If we use PSP it is because we want to use it in user mode.



### Cortex-M4
* Processor modes:
    * Thread mode:
        * Execute applications.
        * Processor enters thread mode (priviledged) at startup.
        * CONTROL register controls whether executions is privileged or un privileged.
    * Handler mode:
        * Handles exceptions.
        * Processor returns to thread mode once exception processing finisshed.
        * Always priviledged.
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
