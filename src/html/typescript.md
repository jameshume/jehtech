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


## TS Compiler Config
* Avoid continuall re-running `tsc` using watch mode: 
    * Specific file: `tsc <filename> --watch`
    * A project `tsc --init` (only once for project - be in root before running!)
        * Creates `tsconfig.json`
            * Non-compile Options:
                * `"exclude": [...list of more file names...]` (* and ** ok and "node_modules" excluded bu default)
                * `"include": [now only these files are compiled - must include everything]`
            * Compiler Options
                * `"target": "es5|es6|...` - which version of JavaScript you compile to.
                * `"lib": []` - spec library files to include, e.g. DOM model (is default known).
        * Now can just run `tsc --watch`
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

<pre>
<b>// Simple types</b>
const blah: number = 5; // However TS can infer this - dont 
                        // need to be so explicit in this ex because
                        // doing decl and init on *same* line!


<b>// Arrays</b>
const bar: number[] = [1,2,3]


<b>// Objects / Classes</b>
const foo: Date = new Date();


<b>// Object literal</b>
const cartesian = { x: number; y : number } {
    x: 10,
    y: 100
}


<b>// Functions</b>
// "Normal" functions
function myFunc(a: number, b: number) : number {
    //                                ^^^^^^^^
    //                                Return type
}

// Return type can be `void` if nothing returned
function myFunc(a: number, b: number) : void {    
}

// Function references
let myFuncRef: Function;
myFuncRef = myFunc

const myFunc: (arg1: type1) => return_type = (arg1: type1) => {
    //        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    //        This is the annotation even though it looks like the
    //        func defn - hard to read syntax
}


<b>// Union types (best to avoid)</b>
let oops: boolean | number = false;
...
boolean = 44;


<b>// Literals</b>
// Not just a type but the specific value, or subset of values, from the set of values the type supports!
// Just union of literals
someVar: 1 | 2 | 3 // Can only have literal values 1, 2, or 3


<b>// Alias</b>
// The `type` keyword is *not* JS, it is introduced by TS
type StringOrNumber = string | number;
type User = { name: string; age: number };
```

Some examples of when type annotation is useful:

* Variables declared on one line but initialised later - TS can't infer here.
* WHen variable has type that cannot otherwise inferred
* When function returns 'any' type and it needs to be restricted/clarified

#### Types Added By TypeScript

``` { .prettyprint .linenums}
//
// Tuples (Really fixed length arrays):
var_name: [number, string] 

// Note tuple length is contrained when creating them but unfortunately
// you can violate this with .push()


// Enums
enum { ENUM_1, ENUM_2, ... }  // Creates labels starting at 0
enum { ENUM_1 = 101, ENUM_2, ... }  // Creates labels starting at 101
// + Can assign to any/all of the enum members.
```
## Classes
