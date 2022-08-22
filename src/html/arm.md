
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

## Programmers Model
* Explains the interface programmer must use to design their application on a specific processor.

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


## Cortext-Debug: VSCode Extension - JLINK
* VSCode would call `launchRequest()` in `gdb.ts`:
  * This does `launchAttachInit()` amd then `processLaunchAttachRequest()`, witch `attach=false`.
  * `processLaunchAttachRequest()`:
    * The session is started: this refers to starting GDB client and the server and starting a debug "session".
    * Symbols are loaded asynchronously
    * GDB is started asynchronously
    * TCP ports acquired then
      * Creates GDB Server and once it is started
        * Waits for GDB client to have finished launching
        * Waits for GDB server to have finished launching
        * Waits for symbol load to have completed
        * SENDS init commands
        * SENDS preLaunch commands
        * SENDS launch commands (or overridden version)
          * For JLink this is
            ```
            interpreter-exec console "monitor halt"     # Exec command in GDB CLI interpreter - monitor == send through as-is to server
            interpreter-exec console "monitor reset"    # Exec command in GDB CLI interpreter - monitor == send through as-is to server
            if no loadFiles                             # Reset for M0 will always leave CPU halted
              interpreter-exec console "monitor reset"
              target-download
            else if zero length loadFiles
              <nothing>
            else 
              interpreter-exec console "monitor reset"
              for each FILE:
                file-exec-file FILE                    # Specify the executable file to be debugged
                target-download                        # Loads the executable onto the remote target

            interpreter-exec console "monitor reset"
            ```
        * SENDS postLaunch commands
* See `restartRequest()` in `gdb.ts`. The restart command send to the server will be
  ```
  ...preRestartCommands
  interpreter-exec console "monitor halt"  } Or if overridden, block replaced with new commands.
  interpreter-exec console "monitor reset" } 
  ...postRestartCommands # All reset strateges halt the CPU after the reset, so CPU is HALTED here
  ```
  After reset all JLink reset strategies have halted the CPI. In `resetRequest()`, only after the
  restart commands (inc. pre and post) are sent, is there is stuff about a start sequence: 
  `finishStartSequence()`: `this.miDebugger.restart(commands).then(async (done) => {....`.
    * JLink reset command: https://wiki.segger.com/J-Link_GDB_Server#reset
    * JLink reset strategies: https://wiki.segger.com/J-Link_Reset_Strategies
    * All of them halt the CPU after the reset.
* Dissasembly. See `runDisasmRequest()` in `disasm.ts`.