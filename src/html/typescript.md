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
type User = { 
    name: string;
    age: number 
};

// Or for a func...
type MyFunc = (a: int, b: string) => int[];
let myf: MyFunc;
...
mgf = (a: int, b: string) => {
    return [1,2,3];
}
</pre>

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
* A difference in TS is that you can specify, as a little improvement,  `this: <class type>` as a parameter for class methods to
allow TS to detect errors where `this` would not lexically scope as happens in JS.
* Class fields and methods can have `private`, `protected` and `public` (the default) modifiers. This will compile down to
  [private JS class fields](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_class_fields#specifications)
  if the compile-to version is modern enough, for example. If compile-to JS version not enough then not runtime enforced, only in TS.
  eg.

```
// Can do this
class A {
    private a: int;
    private b: int[] = [];
    ...
    
    constructor(a: int, b: int[]) {
        this.a = a;
        this.b = b;
        ...
    }
}

// And the SHORT CUT is this:
class A {
    private a: int;
    private b: int[] = [];
    ...
    
    constructor(private a: int, private b: int[], ...) {
        // With access modifiers the class member vars will be auto made for us...
    }
}
```

* Can make fields readonly after init. Only a TS fixture, does not exist in JS.
```
class A {
    private a: int;
    private b: int[] = [];
    ...
    
    constructor(private readonly a: int, private b: int[], ...) {
        //              ^^^^^^^^
        //              a will be read only after it is initialised
    }
}
```

* Getters and setters like in normal JS
```
class A {
    private a: int = 10

    get my_a() {
        return a; // But you'd use more complex logic!
    }

    set my_a(value: int) {
        this.a = value;
    }
}

const a = new A()
a.my_a; // returns 10
```

* Static properties and methods use `static` keyword

* In abstract classes can use `abstract` class functions using this keyword. They have no body and must define the return val.
```
abstract class A {
    abstract some_func(this: A, ...): void;
    //                                ^^^^^
    //                                Note return type and NO function body
}
```

* Create singletons using `private` constructors.

## Interfaces
* Describes a class/object members and functions. Use to type check objects.
* Classes can `implements` interfaces... just like in Java - the solved the multiple inhertiance virtual base class problem.
* TS only, doesn't exist in JS

```
interface A {
    var1: string;
    var2: string[];
    ...

    some_func(param: int, ...): int;
    ...
}

let myA: A;
...
...
myA = { // The following matches the interface so TS can typecheck this assignment because
        // it knows what `myA` should look like.
    var1: "JEH",
    var2: "Tech",
    some_func(param: int, ...) {
        ...
    }
}

// OR
class MyClass implements A[, B[, ...]] {
    ...
}
```

* Interfaces cannot have `public`, `protected`, `privated`.
* Interfaces CAN have `readonly` properties.
* Interfaces can `extends` interfaces. Inheritance for interfaces!
```
interface A extends B, C[, ...] { ... } 
```

* Optional parameters and properties (can do in classes too!):
```
interface A {
    optionalVariables?: int;
    //               ^
    //               Note the question mark - interface implementers can
    //               choose not to implement this.
}
```

## Advanced Types

### Intersection Types
* With a union type, can only access members that are *common* to all types in the union.
* An intersection type *combines* multiple types into one.
    * `type ALL = A & B & C`: `ALL` object has members of *all* three types!

```
type A = {
    a1: string;
    a2: int
}

type AA = {
    a1: string;
    a3: int[]
}

type AAA = A & AA;
// Has the type {
//     a1: string;
//     a2: int
//     a3: int[]
//}
```

But for primative types it is an intersection:
```
type A = number | string;
type B = number | boolean;
type C = A & B; // effective type is number string or boolean!
```

### Discrimated Union
* Give an interface a literal type and use it to distinguish between objects that object the interface.
* Feels a bit yuk - if/elses on types... hmmm.


### Type Casting
* Tell TS something is a certain type;
* E.g., getting a DOM element, or a property of an element, need to tell TS what the type is
```
// Method 1
const inputElement = <HTMLInputElement>document.getElementByID("some-id")!; //< Have to tell TS what type of DOM element this is!
//                   ^^^^^^^^^^^^^^^^^                                   ^
//                   ^^^^^^^^^^^^^^^^^                                   The EXCLAMATION mark tells TS this will not be null
//                   This is one way to type cast


// Method 2
const inputElement = document.getElementByID("some-id")! as HTMLInputElement; //< Have to tell TS what type of DOM element this is!
//                                                       ^^^^^^^^^^^^^^^^^^^
//                                                       The other way to type case (avoids it looking like React JSX)  
```

* Cannot type cast if the returned value could be null. Have to do this
```
const somethingThatCouldBeNull = ...;
if (somethingThatCouldBeNull) {
    (somethingThatCouldBeNull as HTMLInputElement).value = ...'
  // ^                         ^^^^^^^^^^^^^^^^^^^^
  // Need to wrap the variable in parenthesis and cast inside them like so. 
}
```

### Index Properties
* Define the types of properties in a class but not their actual names
```
// Don't know property count or names, jsut know they must all be strings and have values that 
// are also strings.
interface Blah {
    [prop: string]: string;
}
```


### Function Overloads
E.g. help typescript infer return type correctly when multiple possibilities exist.
```
type Combinable = string | number;

function add (a: number, b: number): number                 //<< Function override so that TS knows that adding a number...
function add (a: Combinable, b: Combinable): Combinable {   // ...and a number results in a number and not a Combinable
    ...
}
```

## Generics
* Kinda like templates in C++

### Built In
```
// E.g. Arrays:
const my_array: Array<string>;
const my_array: Array<string | number>; // etc etc

// Promise
const promise: Promise<what-it-resolves-to> = new Promise((resolve, reject) => {...});
// so more specifically...
const promise: Promise<string> = new Promise((resolve, reject) => {... resolve("result"); ...});
// now we know that
promise.then(data => ...) // that data is of type string - so better type safety here :)
```

### User defined generic function
```
// E.g.,
function myFunc<T, U>(p1: T, p2: U): T & U {
    ...
}

// Can call the function "bare" but can also specialise the template like this:
const a = myFunc<{p1: int}, {p2: string}>({p1: 1}, {p2: "james"});
// But shouldn't ordinarily need to do this ^^

// Can apply constraints to cover for JS silent fails:
function myOtherFunc<T>(p1: T); // T is *any*. May want to contrain it to be something...
// So do this:
function myOtherFunc<T extends SomeClassInterfaceOrType>(p1: T); 
//                     ^^^^^^
//                     Where you could extend an interface if you wanted, for example, to
//                     contrain the object to having a superset of certain keys, etc.

// Eg
type MyFunc = (a: int, b: string) => int[];
interface CanSpeak {
    speak: MyFUnc
}
function doSpeak<T extends CanSpeak>(p1: T): string;
//              ^^^
//              Will accept any type that has a speak member that is a function of type MyFUnc.

// Use `extends keyof` to say a param is a key of an object
```

### Generic classes
```
class MyClass<T> {
    function somFunc(p1: T) {
        ...
    }
    ...
    function otherFUnc<U>(p1: T, p2: U) {
        ...
    }
    ...
}
const myInstance = new MyClass<string>();
```

### Utility Types
* [The Docs](https://www.typescriptlang.org/docs/handbook/utility-types.html)

#### Partial Types
* Tell TS it will eventually be that full type, but we're going to build it up rather than define it in one go.
* Makes all members optional
```
interface Junk {
    a: int,
    b: int
}

const a: Partial<Junk> = {}; // Partial required here coz not initialising type in one go
a.a = 1;
a.b = 2;
const b: Junk = a as Junk;


#### Read Only Types
```
const junk: Readonly<int[]> = [1, 2]
junk.push(3); // TS will complain (JS will just do it - JS can freeze arrays!)
```

