## Linker Files


### References
* [From Zero to main(): Demystifying Firmware Linker Scripts](https://interrupt.memfault.com/blog/how-to-write-linker-scripts-for-firmware)
* [The Most Thoroughly Commented Linker Script in The World](https://github.com/wntrblm/Castor_and_Pollux/blob/main/firmware/scripts/samd21g18a.ld)
* [Executable and Linking Format (ELF) Specification Version 1.2](https://refspecs.linuxbase.org/elf/elf.pdf)
* [ARM ELF File Format](https://developer.arm.com/documentation/dui0101/a/)
* [Basic Linker Script Concepts](https://sourceware.org/binutils/docs/ld/Basic-Script-Concepts.html)
* [LD docs](https://sourceware.org/binutils/docs/ld/index.html)


### Anatomy

LD files contain the following:

1. Memory layout: what memory is available and where. 
   
   ```
   MEMORY
   {
     name [(r|w|x|a)*] : ORIGIN = origin, LENGTH = len
     ...
   }
   ```

   For example, the Atmel SAM L21 memory map is defined on page 44 of the [datasheet](https://www.farnell.com/datasheets/2014285.pdf).

2. Section definitions: where different program sections (code and data) should be placed in memory.
   Convention: `.text` for code and constants, `.bss` for uninitialised data, `.stack` and `.data` for initialised data.
3. Options: commands for architecture, entry point etc.
4. Symbols: variables injected into program at link time.

### Sections

All of the object files contain various sections. These are the *input* sections.

The linker file defines a set of *output* sections that include arbirary *input* sections. I.e., the input sections are mapped to output sections, which are mapped to various physical memory locations.

To define and add a section to a memory region:

```
SECTIONS
{
    .output_section_name [address]: <-----------+
    {                                           |
        file_name(section_name_in_file) --------+  << Any filename and input section(s) within matching
    } [> memory_region_name] [AT> load_addr ]         these patterns get put into the .section_name section.
}
```

In the above, the files being linked are inputs and the sections they contain are *input sections*. The result of the linking, i.e., the single binary, also contains sections, sometimes called *output sections*

Every section has a *load address* (LMA) and a *virtual address* (VMA). The linker uses VMA addresses to resolve symbols.

> Every loadable or allocatable output section has two addresses. The first is the VMA, or virtual memory address. This is the address the section will have when the output file is run. The second is the LMA, or load memory address. This is the address at which the section will be loaded. In most cases the two addresses will be the same. An example of when they might be different is when a data section is loaded into ROM, and then copied into RAM when the program starts up (this technique is often used to initialize global variables in a ROM based system). In this case the ROM address would be the LMA, and the RAM address would be the VMA.


![Image describing the difference between the LMA and VMA of a section in a linker file](##IMG_DIR##/linker_file_vma_vs_lma.png)

Usually in LD files we will see sections that look something like the following (taken from LD file for STM32 app):

```
.text :
  {
    . = ALIGN(4);
    *(.text)           /* .text sections (code) */
    *(.text*)          /* .text* sections (code) */

    KEEP (*(.init))
    KEEP (*(.fini))

    . = ALIGN(4);
    _etext = .;        /* define a global symbols at end of code */
  } >FLASH
```

Of interest here is that wildcards (the asterisks (`*`)) are used.

In `*(.text*)`, the first asterisk selects all object files and the second is a wild card that means from all the selected object files the sections matching `.text*` are inclued. This means the sections `.text_some_name`, `.text_blahblahblah` etc would all be included in the `.text` section.

The `KEEP` directive is also interesting. This is used when the linker does *garbage collection of unused sections* and specifically tells the linker never to discard the sections annotated by `KEEP`.

So why are the following useful? One example use I had was using Ceedling. Ceedling outputs an absolute ton of mocked methods for unit tests, only a small fraction of which I actually used in my tests. When running on a memory contrained target this was a problem as including unused functions bloated the `.text` section size to the point that some tests would not fit in flash. How to overcome this? Get the linker to discard unused functions. The catch? The linker can only do things at the section level of granularity, so to work around this we must tell GCC to put each function in its own section using the `-ffunction-sections` command line option.


```
EXCLUDE_FILE (test_*.o) *(.text*)
KEEP(test_*.o(.text*))
```

The first line includes all `.text*` sections, except those sections found in files named `test_*.o`.

The second line - `test_*.o(.text*)` selects all `.text` sections from files matching the pattern `test_*.o` - the opposite of above. The `KEEP` specifier tells the linker that although it has been instructed to garbage collect unused sections, it may not garbage collect the `.text` sections from files matching the pattern `test_*.o`. The reason for this is that if we don't specify this it will garbage collect almost everything. The reason for this is that the main Ceedling test runner, runs the test functions by calling them through a function pointer. The linker cannot track this so the call graph it would otherwise generate would not include any tests... fun!

Therefore, what we're saying is that the linker is free to garbage collect everything it likes, except the test functions themselves - we force it to know something about the call graph it couldn't otherwise.

The compiler flags that were added to the target ceedling YAML are what enable the garbage collection by instructing the compiler to put every function in its own section, which is what then allows the linker to garbage collect, as it can only garbage collect by section.

In general:

### Referencing Linker Script Symbols From C Code
[See the docs](https://sourceware.org/binutils/docs/ld/Source-Code-Reference.html).

> You cannot access the *value* of a linker script defined symbol - it has no value - all you can do is access the *address* of a linker script defined symbol.

