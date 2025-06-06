## Command Cheat Sheet
### Process control

| Command     | Description                                              |
| ----------- | -------------------------------------------------------- |
| `run`       | Starts (or restarts) the program from the entry point.   |
| `interrupt` | Halts the program (like Ctrl-C in the terminal).         |
| `kill`      | Terminates the current debugging session.                |
| `step`      | Runs one source line, stepping into functions.           |
| `next`      | Runs one source line, stepping over functions.           |
| `finish`    | Runs until the current function returns.                 |
| `continue`  | Resumes execution after a stop (like after `interrupt`). |


### Remote control
The `monitor` commands send raw commands directly to the remote target—often through a GDB server like OpenOCD.

| Command                        | Description                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------- |
| `target extended-remote :3333` | Connects GDB to a remote target via a GDB server (like OpenOCD) on port 3333. |
| `monitor reset halt`           | Sends the reset and halt command to the remote target.                        |
| `monitor reset run`            | Sends the reset and run command to the remote target.                         |
| `monitor halt`                 | Stops (halts) the target immediately.                                         |
| `monitor reset`                | Resets the target (may halt or run depending on default behavior).            |


### Info

| Command                 | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| `info registers`        | Shows the current contents of CPU registers.               |
| `disassemble 0xADDRESS` | Shows the assembly code around the given address.          |
| `info symbol 0xADDRESS` | Shows the nearest symbol and offset for the given address. |
| `bt`                    | Shows the backtrace (call stack).                          |
| `info threads`          | Lists all threads (if applicable, like in an RTOS).        |
| `thread <N>`            | Switches context to thread number `<N>`.                   |
| `info locals`           | Displays local variables in the current frame.             |
| `info frame`            | Shows detailed info about the current stack frame.         |


### Code navigation

| Command  | Description                                      |
| -------- | ------------------------------------------------ |
| `step`   | Runs one source line; steps into function calls. |
| `next`   | Runs one source line; skips over function calls. |
| `finish` | Runs until the current function returns.         |
| `stepi`  | Steps one assembly instruction.                  |
| `nexti`  | Steps over one assembly instruction.             |


### Breakpoints

| Command                        | Description                                                      |
| ------------------------------ | ---------------------------------------------------------------- |
| `break filename:linenumber`    | Sets a breakpoint at the given file and line number.             |
| `break function_name`          | Sets a breakpoint at the start of a function.                    |
| `delete breakpoint_number`     | Deletes the breakpoint with the given number.                    |
| `delete`                       | Deletes **all** breakpoints and watchpoints.                     |
| `info breakpoints`             | Lists all current breakpoints and watchpoints.                   |
| `disable breakpoint_number`    | Disables the breakpoint but does not remove it.                  |
| `enable breakpoint_number`     | Enables a previously disabled breakpoint.                        |
| `watch *(uint32_t*)0xADDRESS`  | Sets a watchpoint to stop when the value at the address changes. |
| `rwatch *(uint32_t*)0xADDRESS` | Stops when the value at the address is **read**.                 |
| `awatch *(uint32_t*)0xADDRESS` | Stops when the value at the address is **read or written**.      |


### Examining Memory

| Command                                                          | Description                                                |
| ---------------------------------------------------------------- | ---------------------------------------------------------- |
| `dump binary memory <filename> <start_address> <end_address>`    | Saves the memory range to a binary file.                   |
| `dump ihex memory <filename> <start_address> <end_address>`      | Saves the memory range as an Intel HEX file.               |
| `dump intel-hex memory <filename> <start_address> <end_address>` | Alternate name for `ihex` format.                          |
| `x /Nxf ADDRESS`                                                 | Displays memory in hex (not to a file; prints to console). |
| `x /Nxb ADDRESS`                                                 | Displays memory in binary (not to a file).                 |


#### Log Buffer In Memory
For really simple logging, a small, wrapping, buffer in memory with a size will do the job. The buffer is just a set of NULL terminated strings.

```cpp
#define MYLOG_SIZE 512
char mylog[MYLOG_SIZE];
size_t mylog_next_free;
```

Assuming that the buffer hasn't wrapped, to get a nice print out of the entries use:

```
x/100s mylog
```

And up the size (`100`) as the buffer grows.

I want to figure out a way to pass `mylog_next_free` as the size, but haven;t yet...