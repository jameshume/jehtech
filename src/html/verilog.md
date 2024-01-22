## Resources
* Try out https://edaplayground.com/
* See 
    * [FPGAs For Dummies](https://www.stepfpga.com/doc/_media/fpgasfordummiesebook.pdf)
    * [Verilog Pro](https://www.verilogpro.com/)
    * [Nand Land Verilog Tutorials](https://nandland.com/learn-verilog/)
    * [FPGA Architectures: An Overview](https://cse.usf.edu/~haozheng/teach/cda4253/doc/fpga-arch-overview.pdf)
    * [Advanced Verilog - ECS 270 v10/23/0](https://www.eecs.umich.edu/courses/eecs270/270lab/270_docs/Advanced_Verilog.pdf)
    * [IEEE Standard for Verilog(R) Hardware Description Language](https://www.eg.bucknell.edu/~csci320/2016-fall/wp-content/uploads/2015/08/verilog-std-1364-2005.pdf)
* Unlike "normal" software programming languages like "C", which is sequention, 
  HDL statements are executed in *parallel* and continually execute (*always*) for
  a specified number of times or times.

## Quick Looks At FPGAs
<p></p>
<blockquote>
    <p>
        Field programmable Gate Arrays (FPGAs) are pre-fabricated silicon devices that can
        be electrically programmed in the field to become almost any kind of digital circuit
        or system. For low to medium volume productions, FPGAs provide cheaper solution
        and faster time to market as compared to Application Specific Integrated Circuits
        (ASIC) which normally require a lot of resources in terms of time and money to
        obtain first device
    </p>
    <p>
        Normally FPGAs comprise of:
    </p>
    <ul>
        <li>Programmable logic blocks which implement logic functions.</li>
        <li>Programmable routing that connects these logic functions.</li>
        <li>I/O blocks that are connected to logic blocks through routing interconnect and that make off-chip connections.</li>
    </p>
    <footer>-- <a href="">https://cse.usf.edu/~haozheng/teach/cda4253/doc/fpga-arch-overview.pdf</a></footer>
</blockquote>
<p></p>

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
<p></p>



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
        D <= A nor B;       // "<=" means PARALLEL EXECUTION
        E <= B and C;
        Q <= D or E;
    end

endmodule

```

The above is an example of combinatorial logic: logic that does not require a clock to operate.

In the above, the execution of the logic is done in *parallel*, as noted by the use of the `<=` operator.

Where `=` to be used, then the execution would be sequential. In sequential logic, where the output
depends on the current state and inputs, you might use something like `always @(posedge clk or posedge rst)` to
trigger the block on positive clock edges or resets.

The `always` block is continuously executed, triggered on changes to any of the signals in the
sensitivity list.

Note that the following assignments in the `always` block shown are identical to continuous assignments
outside of a block:

```
always @(A,B,C,D,E)
begin
    D <= A nor B;
    E <= B and C;
    Q <= D or E;
end
```

Is identical to:

```
assign D = A nor B;
assign E = B and C;
assign Q = D or E;
```

Because there is no clock being used.

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
        * Wires are used for connecting different elements. They can be treated as physical wires - they are a type of net.
        * They can be read or assigned, but only by continuous assignment can they be assigned. I.e. use of `assign` statement
          outside of an `always` block or driven directly from an output port.
        * No values get stored in them: teh value is derived from what is being driven from its drivers.
        * They need to be driven by either continuous assign statement or from a port of a module. [[Ref]](https://stackoverflow.com/a/33462996).
        * By default they are 1-but wide, i.e, they are *scalar*. A vector is required to hold values other than 0 or 1 (see later).
    * `reg` (registers): 
        * Use when you want to represent a piece of storage.
        * Can only be assigned using proceedural statements, I.e., drive from an `always`/`initial` block.
        * Contrary to their name, regs don't necessarily correspond to physical registers. They represent
            data storage elements in Verilog/SystemVerilog. They retain their value until the next value is assigned
            to them (not through an `assign` statement). They can be synthesized to FF, latch or combinatorial
            circuits. [[Ref]](https://stackoverflow.com/a/33462996).
        * Put another way, "a register remembers a piece of information until it is told to remember something else"
          [[Ref]](https://www.stepfpga.com/doc/_media/fpgasfordummiesebook.pdf).
    * `reg` v.s. `wire`
        * See also
            * [Verilog reg, Verilog wire, SystemVerilog logic. What’s the difference? by Jason Yu](https://www.verilogpro.com/verilog-reg-verilog-wire-systemverilog-logic/)
        * For `wire` vs `reg`, Jason Yu (see link above) has some good rule's of thumb:
            1. Use Verilog `reg` when you want to represent a piece of storage, and use Verilog `wire`
            when you want to represent a physical connection.
            2. Drive a Verilog `wire` with `assign` statement or port output
            3. Drive a Verilog `reg` from an `always` block. If you want to drive a physical connection with
               combinatorial logic inside an `always@(*)` block, then you have to declare the physical
               connection as Verilog `reg`.
    * integer
    * real
    * string
    * time (current time is `$time`)
    * parameter: same as `const` in C
    * vectors
    * arrays
* Operators
    * Conacatenation `{}` [[Ref]](https://nandland.com/concatenation-operator-2/).
        * Can concatenate two more more types/signals (not necessarily the same).
        * Examples:
            * `wire [7:0] C = {A, B}`, where `A = 4'b0111` and `B=4'b1100`, results in `C=8'01111100` or `0x7C`.
            * `wire [15:0] C = {A, B}`, where `A = 4'b0111` and `B=4'b1100`, results in
              `C=8'0000000001111100` or `0x007C`. This demonstrates padding.
            * `r_SHIFT_REG[7:0] <= {r_SHIFT_REG[6:0], r_SHIFT_REG[7]};` demonstrates a circular rotation of a buffer.
    * Replication `{}`.
        * `<repition count>{<thing-to-replicate>}`
        * The repetition multiplier must be a constant.
        * Example, if `reg [3:0] V = 4'b0111;`:
            * `3{V}` results in `12b011101110111`.            


### Assignment
#### Proceedural Assignment
<p></p>
> Procedural assignments update the value of variables under the control of the procedural flow
> constructs that surround them.

> ...procedural assignments put values in variables. The assignment does not have duration; instead,
> the variable holds the value of the assignment until the next procedural assignment to that
> variable.
>
> Procedural assignments occur within procedures such as always, initial (see 9.9), task, and function (see
> Clause 10) and can be thought of as "triggered" assignments...


A brief note on assignment operators [[Ref]](https://stackoverflow.com/a/27435773):
* `<=` is **non-blocking** and is performed on every positive edge of clock. These are evaluated in parallel so
   no guarantee of order. An example of this would be a register.
* `=` is **blocking** assignment, which should only be used inside `always` statements and enforces sequential order.

Both `<=` and `=` *must be used within an `initial` or `always` block*.

Delayed assignment can be done using the `#` operator. E.g.

```
always @(*)
begin
    #(cycle/2) ... this is done on every cycle/2-th period
end
```
Be warned: [Nonblocking Assignments in Verilog Synthesis, Coding Styles That Kill!](http://www.sunburst-design.com/papers/CummingsSNUG2000SJ_NBA.pdf).

##### Blocking Proceedural Assignment
> A blocking procedural assignment statement shall be executed before the execution of the statements that
> follow it in a sequential block ... A blocking procedural assignment statement shall not prevent the
> execution of statements that follow it in a parallel block ... [[Ref]](https://www.eg.bucknell.edu/~csci320/2016-fall/wp-content/uploads/2015/08/verilog-std-1364-2005.pdf)

In other words:
> A blocking assignment gets its name because a blocking assignment must evaluate the RHS arguments 
> and complete the assignment without interruption from any other Verilog statement. The assignment
> is said to "block" other assignments until the current assignment has completed [[Ref]](http://www.sunburst-design.com/papers/CummingsSNUG2000SJ_NBA.pdf)

##### Non-Blocking Proceedural Assignment
<p></p>
> The nonblocking procedural assignment allows assignment scheduling without blocking the procedural
> flow. The nonblocking procedural assignment statements can be used whenever several variable assignments
> within the same time step can be made without regard to order or dependence upon each other. [[Ref]](https://www.eg.bucknell.edu/~csci320/2016-fall/wp-content/uploads/2015/08/verilog-std-1364-2005.pdf)

If there is no timing control in the block in which the `<=` is being used, then the order of
evalulation of the expressions is not specified - i.e., no particular ordering is guaranteed.

However, if timing control is specified, then evaluation occurs in two steps:

1. At the trigger the RHS of the nonblocking assignments are evaluated, but the updates are
   secheduled for "later" in a second phase, the "nonblocking assign update events".
2. In the nonblock assign update event the RHS values that were evaluated and remembered in
   step one are assigned to the LHS.

The specification [[Ref]](https://www.eg.bucknell.edu/~csci320/2016-fall/wp-content/uploads/2015/08/verilog-std-1364-2005.pdf)
gives this example:

```
init begin
    a = 0;
    b = 1;
end

always @(posedge c) begin
    a <= b;
    b <= a;
end
```

As `<=` does not block, the only way these two statements could execute concurrently and not
involve a race condition is by using the above strategy. That is why the output of the
above is deterministic and after the first clock edge `a` will be `1` and `b` will be `0`.

As another example, the following creates a race condition because the two `always` blocks execute simultaneously:

```
always @(posedge clk)
    a = b;

always @(posedge clk)
    b = a;
```

This is a race condition because both equations are scheduled to execute in the same simulation time step,
and when blocking assignments are scheduled to execute in the same time step, the order execution is
unknown [[Ref]](http://www.sunburst-design.com/papers/CummingsSNUG2000SJ_NBA.pdf). 

> A Verilog race condition occurs when two or more statements that are scheduled to execute in
> the same simulation time-step, would give different results when the order of statement
> execution is changed, as permitted by the IEEE Verilog Standard. [[Ref]](http://www.sunburst-design.com/papers/CummingsSNUG2000SJ_NBA.pdf)

However, if non-blocking assignment is used the race condition is removed.

```
always @(posedge clk)
    a <= b; // No race condition any more

always @(posedge clk)
    b <= a; // No race condition any more
```

This is because for non-blocking assignment, as we saw, on the rising edge the LHS of all of the `<=`
expressions will be evaluated and the assigned in the next "phase" (but obs on the same rising edge).

##### Blocking v.s. Non-Blocking Guidelines
Taken verbatim from [[Ref]](http://www.sunburst-design.com/papers/CummingsSNUG2000SJ_NBA.pdf).

1. When modeling sequential logic, use nonblocking assignments.
2. When modeling latches, use nonblocking assignments.
3. When modeling combinational logic with an always block, use blocking assignments.
4. When modeling both sequential and combinational logic within the same always block, use nonblocking assignments.
5. Do not mix blocking and nonblocking assignments in the same always block.
6. Do not make assignments to the same variable from more than one always block.
7. Use $strobe to display values that have been assigned using nonblocking assignments.
8. Do not make assignments using #0 delays. 


#### Continual Assignment
The keyword `assign` is used for continual assignment to a `wire` outside an `always` statement.
The value of LHS is updated when RHS changes.

> Continuous assignments drive nets and are evaluated and updated whenever an input operand
> changes value. 

> Assignments on nets shall be continuous and automatic. In other words, whenever an operand in
> the righthand expression changes value, the whole right-hand side shall be evaluated. If the
> new value is different from the previous value, then the new value shall be assigned to the left-hand side. 

Continual assignment is done using the `assign` keyword and must be done *outside* a block. It is limited to basic boolean
and ternary-if (`bool ? do-if-true : do-if-false`) operators.


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

Verilog arrays can only be reference one element at a time.

### Always Blocks
See [Tutorial – Sequential Code on your FPGA -- Using Process (in VHDL) or Always Block (in Verilog) with Clocks](https://nandland.com/tutorial-sequential-code-on-your-fpga/).

Not usually used to combinatorial logic as the same effect can be achieved with `assign`, outside of a block.

The NANDLAND author gives the following two, almost equivalent pieces of code:

```
always @ (*)
  begin
    and_gate <= input_1 & input_2;
  end
```

... and ...

```
// Taken from https://nandland.com/tutorial-sequential-code-on-your-fpga/
always @ (posedge i_clock)
  begin
    and_gate <= input_1 & input_2;
  end
```

They look almost identical, except that the first uses *combinatorial* logic and the latter *sequential* logic. Why? In the
first `and_gate` is *immediately updated* whenever any of its inputs change. In the latter, `and_gate` is *not immediately* updated
whenever an input changes... it has to wait for the next rising clock edge!

The author also gives the following example:

```
// Taken from https://nandland.com/tutorial-sequential-code-on-your-fpga/
reg test1 = 1'b1;
reg test2 = 1'b0;
reg test3 = 1'b0;
reg test4 = 1'b0;
 
always @ (posedge i_clock)
  begin
    test2 <= test1;
    test3 <= test2;
    test4 <= test3;
  end
```

On each rising clock edge *all* of the lines are executed in parallel -- at the same time.

The main point of this example is that although `test4` may go high on the 3rd clock edge
it is not valid until the fourth clock cycle due to *propogation time*. This is the case
for all the clock cycles: `testX` will go high, but its not until the next clock cycle
that it is valid and can be clocked by the next flip-flop as it propogates somewhere
between the current and before the next clock edge.

This chimes well with an interesting post I found on reddit: [When to use continuous vs procedural assignment?](https://www.reddit.com/r/FPGA/comments/av739x/when_to_use_continuous_vs_procedural_assignment/).

When using continuous asignments one has to think about *propogation* delay because it
can restrict the clock frequency.

Its replicated here:

The guys code was:

```
...
assign next_test = ((a + b) > 4'hF) ? 4'h0 : (a + b);

always @(posedge clk)
begin
    if(next_test == 4'hF) begin
        test <= 4'h0;
    end 
    else begin
        test <= next_test
    end
end
...
```

The question is should `next_test` be assigned in the `always` block rather than continuously
assigned.

One commenators has the following to say:

> You can stack any number of continuous assignments on top of each other. But it means that
> the entire pipeline would have to fit the timing constraints. As it is coded, your software
> will try to get from the values of 'a' and 'b' to the value of 'test' in one clock. Along the
> way, it needs to calculate a+b, compare it with 0, do conditional assignment, etc., etc. That's
> a long path with multiple chained operations, each of which incurs some propagation delay, which
> brings down the maximum clock rate at which the design can run.
> 
> If you calculate 'next_test' procedurally, you need one clock to get from 'a' and 'b' to 'next_test'
> and a second clock to get from 'next_test' to 'test'. You use more registers and you have higher latency,
> but the maximum achievable clock rate is higher.
>
> Incidentally, your code seems wrong. If a, b, and next_test are all 4-bit, I think that the result
> of ((a+b)>4'hF) is always false, because (a+b) is going to be 4-bit too. You'd need something like
> 
> wire [4:0] temp;
> assign temp = a+b;
> assign next_test=temp>5'hF ? 4'h0 : temp[3:0];

#### Scope
The `always` block does not have scope like one might expect in an actual software (i.e., hot hardware) language like C.
And because all of the `always` blocks in a module (program?) execute CONCURRENTLY, the following should throw an error because
`var` can't get two values concurrently!

```
always @(posedge clk)
    ...
    var1 = ....;
    ...
end

...

always @(posedge clk)
    ...
    var1 = ....;
    ...
end
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
