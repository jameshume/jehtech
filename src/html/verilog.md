* Try out https://edaplayground.com/
* See [FPGAs For Dummies](https://www.stepfpga.com/doc/_media/fpgasfordummiesebook.pdf)
* Unlike "normal" software programming languages like "C", which is sequention, 
  HDL statements are executed in *parallel* and continually execute (*always*) for
  a specified number of times or times.

<blockquote>
    <p>
        Modern FPGAs consist of mixes of configurable static random
        access memory (SRAM or Flash), high-speed input/output pins
        (I/Os), logic blocks, and routing. More specifically, an FPGA
        contains programmable logic elements called, naturally,
        logic elements (LEs), as well as a hierarchy of reconfigurable
        interconnects that allow the LEs to be physically connected to
        one another. You can configure LEs to do complex functions
        or simply perform basic logic gates, such as AND and OR.
        Most FPGAs also contain memory blocks ...
    </p>
    <p>
        ... The core of an FPGA is simply an array of these logic gates and
        wires etched into an integrated circuit in a way that allows you
        to reconfigure them ...
    </p>
    <footer>--<a href="https://www.stepfpga.com/doc/_media/fpgasfordummiesebook.pdf">FPGAs for Dummies</a></footer>
</blockquote>

## Small Example Of Parallel Execution

```
//        +-----+
// A -----| NOR |----+
// B --+--|     |    |   D +-----+
//     |  +-----+    +-----| OR  |----- Q
//     |             +-----|     |
//     |  +-----+    |   E +-----+
//     +--| AND |----+
// C -----|     |
//        +-----+

`timescale 1 ns/1 ps
module smallExample (A,B,C,Q);

    input A,B,C; // Inputs
    output Q;    // Outputs
    wire D,E;    // Internmediate signals internal to FPGA

    always @(A,B,C,D,E)     // always @(<sensitivity-list>). Could also be written always@(*)
                            // where the @(*) syntax is a shorthand for specifying sensitivity
                            // to all signals in this block.
                            // "," means AND. To or replace "," with " or ".
        begin
            D <= A nor B;   // "<=" means PARALLEL EXECUTION
            E <= B and C;
            Q <= D or E;
        end

endmodule

```

In the above the execution of the logic is done in *parallel*, as noted by the use of the `<=` operator.
The `always @(*)`` construct is typically used in combinational logic, where the output is purely a
*function of the inputs* and *doesn't depend on any internal state*. 

Where `=` to be used then the execution would be sequential. In sequential logic, where the output
depends on the current state and inputs, you might use `always @(posedge clk or posedge rst)` to
trigger the block on positive clock edges or resets.

The `always` block is continuously executed, triggered on changes to any of the signals in the
sensitivity list.

At the start of the example we see ``timescale 1 ns/1 ps`, which is used to specify the time unit and
precision for the simulation: ``timescale time_unit / time_precision`. 

## Levels Of Descriptions
1. Behavioural model: Design based on truth table.
2. Data flow model: Design based on boolean equations.
3. Gate level model: Design based on gates.

E.g. 2x1 MUX, inputs D0 and D1, select pin S and output Y:

### Behavioural
```
module mux(
    input D0,
    input D1,
    input S,
    output Y
);

    always @(D0 or D1 or S)
    begin
        if (S)
            Y = D1;
        else
            Y = D0;            
    end

endmodule
```

### Dataflow
```
module mux(
    input D0,
    input D1,
    input S,
    output Y
);

    assign Y = S ? D1: D0;

endmodule
```

### Gate Level
```
module mux(
    input D0,
    input D1,
    input S,
    output Y
);

    wire T1, T2, Sbar;

    and (T1, D1, S);
    and (T2, D0, Sbar);
    not (SBar, S);
    or(Y, T1, T2);

endmodule
```

## Verilog Constructs and Datatypes
* Comments: Just Like C/C++ comments
* Number specification: `(Size)'(Radix)(Value)`. E.g. `4'b100` is a 4 bit binary value,
                        `4'd9` is a 4 bit decimal value, `4'hF` is a 4 bit hexadecimal value.
* Data types:
    * Logic values: `1`, `0`, `x`, `z`.
      `x` means "don't care" and `z` means "high impedance".
    * `wire` (nets): 
        * Wires are used for connecting different elements. They can be treated
          as physical wires.
        * They can be read or assigned.
        * No values get stored in them.
        * They need to be driven by either continuous assign statement or from a port of a module. [[Ref]](https://stackoverflow.com/a/33462996).
        * By default they are 1-but wide, i.e, they are *scalar*. A vector is required to hold values other than 0 or 1 (see later).
    * `reg` (registers): 
        * Use when you want to represent a piece of storage.
        * Drive from an `always` block.
        * Contrary to their name, regs don't necessarily correspond to physical registers. They represent
            data storage elements in Verilog/SystemVerilog. They retain their value until the next value is assigned
            to them (not through an `assign` statement). They can be synthesized to FF, latch or combinatorial
            circuits. [[Ref]](https://stackoverflow.com/a/33462996).
        * Put another way, "a register remembers a piece of information until it is told to remember something else"
          [[Ref]](https://www.stepfpga.com/doc/_media/fpgasfordummiesebook.pdf).
    * integer
    * real
    * string
    * time (current time is `$time`)
    * parameter: same as `const` in C
    * vectors
    * arrays

### Assignment
A brief not on assignment operators [[Ref]](https://stackoverflow.com/a/27435773):

* `<=` is non-blocking and is performed on every positive edge of clock. These are evaluated in parallel so
   no guarantee of order. An example of this would be a register.
* `assign` is continual assignment to wire outside an always statement. value of LHS is updated when RHS changes.
* `=` is blocking assignment, inside always statements enforces sequential order.

Both `<=` and `=` *must be used within an `initial` or `always` block*.

Delayed assignment can be done using the `#` oerator. E.g.

```
always
begin
    #(cycle/2)
```

### Vectors
Wires and registers are, by default, *scalar*. I.e., they are 1-bit wide and can hold the numbers 0 or 1. To hold
larger numbers a vector is required. Note, they can also hold `z` - high impedance and `x` - don't care.

Vectors are *declared* as `type [upper:lower] name;`, so for example:

```
wire [7:0] an_8_bit_wire;
reg  [7:0] an_8_bit_reg;
```

In verilog it is *easy to mismatch vectors* and silenty discard bits! So **use a linter**!, e.g. Verilator.

### Arrays
Arrays are similar to C arrays - they are a repetition of a type. So,

```
reg my_reg1[0:11];      // is an array of 12 1-bit register variables
reg [7:0]my_reg2[0:11]; // is an array of 12 8-bit register variables - an array of vectors, known as a MEMORY ARRAY.
```



## Compiler Directives.
Directives are compile time macros that execute during compilation.

All compiler directives begin with a `` ` `` and take the format `` ` ```<keyword> ...`.

* `` ` ```define <macro-name> <value>`: Defines a text macro that is substitutes the text of the macro
  when ever it enounters the macro name. This is analogous to the C `#define`.
* `` ` ```include <filename>`: Just like C's `#include`.
* `` ` ```timescale <time_unit> / <time_precision>`:
* `` ` ```ifdef <define_name>`:
* `` ` ```else`:


## Behavioural Modeling
Keywords include `if`-`else`, `case`, which are synthesizable statements, and `while`, `for`, `forever`, `repeat`, `fork`-`join`, which are not syntheziable and are only really used in the test bench.

Assignment statements such as `=` and `<=` should only be written within a procedural block: `initial` or `always`. Writing
assignment statements outside of a precedural block is an error.

The *initial block* is only executed once and starts at time 0. Useful, for example, initialising variables.

The *always block* is repeatedly executed in a never ending loop and starts after the intial block.

```
module module_name(...);

    initial
    begin
        ...
    end

    always
    begin
        ...
    end

endmodule
```

## Parameterized Verilog Modules
Instantiation parameters can be added to modules to make them analogous to C++ templates. This is done with the pound (`#`) symnbol.

```
module my_module #(paremeter WIDTH) (
    input  [WIDTH-1:0] A,
    output [WIDTH-1:0] A,
);
    ... do stuff ...
endmodule
```

The above decalares what is like a module template... when instantiated with a concrete value for `WIDTH`, a module instance with
`WIDTH` replaced by its value is created:

```
my_module #( .WIDTH(8) ) instance_name (
    .input(...),
    .output(...)
);
```
