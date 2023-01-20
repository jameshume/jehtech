## References
* [DWARF Debugging Information Format, Version 5, February 13, 2017](https://dwarfstd.org/doc/DWARF5.pdf)
* [How debuggers work: Part 3 - Debugging information](https://eli.thegreenplace.net/2011/02/07/how-debuggers-work-part-3-debugging-information)
* [Introduction to the DWARF Debugging Format] (https://dwarfstd.org/doc/Debugging%20using%20DWARF-2012.pdf)
* [Some things I learned about libdwarf, Kamal Marhubi](https://kamalmarhubi.com/blog/2016/07/25/some-things-i-learned-about-libdwarf/)

## Acronyms
| Acronym | Meaning |
|---------|---------|
| DIE     | Debugging Information Entries |
| CU      | Compilation Unit |



## Intro

DWARF (5) is standard that specifies a format for describing programs such that debugging is possible. I.e., it provides a way to describe a program so that things like function symbols, global variables etc can be mapped to addresses, stacks can be unwound and so on.

DWARF tries to be both architecture and language agonistic. It can support many different languages, including C and C++ to name the ones I use, at least.

The debugging information entries are contained in the `.debug_info` section of an object file.

A DWARF blob is a series of **Debugging Information Entries (DIEs)** that are arranged as a tree flattened in prefix order:

```
DIE {
    identifying tag;
    attributes = [
        {
            attribute name,
            ... data ...
        },
        ...
    ];
}
```

The top level DIEs should be Compilation Units (CUs):

> For each compilation unit compiled with a DWARF producer, a contribution is
> made to the .debug_info section of the object file. Each such contribution
> consists of a compilation unit header ... followed by a single `DW_TAG_compile_unit`
> or `DW_TAG_partial_unit` debugging information entry, together with its children ...
>
> -- [DWARF Debugging Information Format, Version 5, February 13, 2017](https://dwarfstd.org/doc/DWARF5.pdf)

DIEs can own other DIEs to form a tree structure so that program constructs like block structures
can be described:

> A variety of needs can be met by permitting a **single debugging information entry to
> "own" an arbitrary number of other debugging entries** and by permitting the same
> debugging information entry to be one of many owned by another debugging information
> entry. This makes it possible, for example, to describe the static block structure within a
> source file, to show the members of a structure, union, or class, and to associate
> declarations with source files or source files with shared object files.
>
> The ownership relationship of debugging information entries is achieved
> naturally because the **debugging information is represented as a tree**.
>
> ...
>
> The **tree itself is represented by flattening it in prefix order**.
>
> -- [DWARF Debugging Information Format, Version 5, February 13, 2017](https://dwarfstd.org/doc/DWARF5.pdf) (emphasis mine)

One should use existing libraries to access DWARF debug information (e.g. `libdwarf`, used on FreeBSD or `libbfd`, as used by GNU binutils) and as such the unit header isn't important, but understanding that the structure is a CU DIE followed by children and siblings is important when using some of the APIs (I'm thinking `libdwarf` here that has functions like `dwarf_siblingof()`, `dwarf_child()` etc - I've not looked at `libbfd` (yet)).

The `libdwarf` library does have some oddities, for example the `_a`, `_b`, etc function suffixes for API upgrades etc.
There are other alternatives to `libdwarf`, including:

1. `libbfd`
2. `liblibdw` from `elfutils`
3. [Gimli](https://users.rust-lang.org/t/gimli-a-blazing-fast-parser-for-dwarf-debugging-information/7348) (written in Rust).

