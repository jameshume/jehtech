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

Every section as a *load address* (LMA) and a *virtual address* (VMA). The linker uses VMA addresses to resolve symbols.

> Every loadable or allocatable output section has two addresses. The first is the VMA, or virtual memory address. This is the address the section will have when the output file is run. The second is the LMA, or load memory address. This is the address at which the section will be loaded. In most cases the two addresses will be the same. An example of when they might be different is when a data section is loaded into ROM, and then copied into RAM when the program starts up (this technique is often used to initialize global variables in a ROM based system). In this case the ROM address would be the LMA, and the RAM address would be the VMA.


### Source Code Reference
[See the docs](https://sourceware.org/binutils/docs/ld/Source-Code-Reference.html).

> You cannot access the *value* of a linker script defined symbol - it has no value - all you can do is access the *address* of a linker script defined symbol.

