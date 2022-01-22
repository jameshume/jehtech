## Overview
* Is JavaScript + a type system,
    * Compiles into "plain" JavaScript.
* To play: [www.typescriptlang.org/play/](www.typescriptlang.org/play/).
    * Fake JSON APIs: [jsonplaceholder.typicode.com](jsonplaceholder.typicode.com)
        * E.g. fetch `jsonplaceholder.typicode.com/todos` to get a JSON list of TODO items,
        * E.g. fetch `jsonplaceholder.typicode.com/todos/1` to get only first TODO item.
* Uses type annotations,
* Goals:
    * Catch errors during development,
    * Type annotations help analyze code,
    * Only active during development,
    * TS compiler does *not* optimize performance.
* **Install**
    * `npm install -g typescript ts-node`
        * `ts-node` is just a timesaver that combines the `tsc` and `node` commands used
          to compile and then run code into one command.
    * Run compiler: `tsc --help`. TSC = **T**ype**S**cript **C**ompiler

## Features & Syntax
### Types
For example, to make a dictionary/object type stricter by defining the members and
their types you can:

``` { .prettyprint .linenums}
inteface my_interface {
    property1: type1,
    ....
    propertyN: typeN
}

const my_variable = some_other_variable as my_interface
```

Or we can do

``` { .prettyprint .linenums}
// Simple types
const blah: number = 5; // However TS can infer this - dont 
                        // need to be so explicit in this ex because
                        // doing decl and init on *same* line!

// Arrays
const bar: number[] = [1,2,3]

// Objects / CLasses
const foo: Date = new Date();

// Object literal
const cartesian = { x: number; y : number } {
    x: 10,
    y: 100
}

// Function
const myFunc: (arg1: type1) => return_type = (arg1: type1) => {
    //        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    //        THis is the annotation even though it looks like the
    //        func defn - hard to read syntax
}

// Union types (best to avoid)
let oops: boolean | number = false;
...
boolean = 44;
```

Some examples of when type annotation is useful:

* Variables declared on one line but initialised later - TS can't infer here.
* WHen variable has type that cannot otherwise inferred
* When function returns 'any' type and it needs to be restricted/clarified

