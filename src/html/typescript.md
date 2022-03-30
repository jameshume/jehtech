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

```
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

```
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
    constructor(private a: int, private b: int[], ...) {
        // With access modifiers the class member vars will be auto made for us...
        // ..note we dont define them in the class body - they're implicitly defined
        // for us now...
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
    [prop: string]: number;
    ^^^^^^^^^^^^^^  ^^^^^^
    ^^^^^^^^^^^^^^  2. And these properties all map to numbers
    1. Blah only has properties that are strings
}
```

Note, this use of square brackets in the interface is *not* the same as ES6 [*computed property names*](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Object_initializer#computed_property_names).

> Starting with ECMAScript 2015, the object initializer syntax also supports computed property names. 
> That allows you to put an expression in brackets [], that will be computed and used as the property name.

### Utility Types and `keyof`
* [See the docs for utility types](https://www.typescriptlang.org/docs/handbook/utility-types.html).
* TypeScript provides several utility types to facilitate common type transformations...
    * `Omit`, `Partial`, `Readonly`, `Exclude`, `Extract`, `NonNullable`, `ReturnType`.
* Example `Omit`:
    
    ```
    interface Book {
        author: string | null;
        numPages: number;
        price: number;
    }
    // Article is a Book without a Page
    type Article = Omit<Book, 'numPages'>;
    ```
* Example `Pick`:
  
    ```
    interface Todo {
        title: string;
        description: string;
        completed: boolean;
    }
        
    type TodoPreview = Pick<Todo, "title" | "completed">;
    
    const todo: TodoPreview = {
        title: "Clean room",
        completed: false,
    };
    ```

* [See the docs 4 mapped types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html).
* The **`keyof`** operator takes an object type and *produces a string or numeric literal union of its keys*:
    * Example:
  
    ```
    type Person = {
        name: string;
        surname: string;
        email: string;
    }
    
    type PersonKeys = keyof Person;
    // PersonKeys = 'name' | 'surname' | 'email'
    ```

    * Example use of `keyof` in `Pick` utlity type

        ```
        // Definition of Pick<Type, Keys>
        // Constructs a type by picking the set of properties Keys (string literal or union
        // of string literals) from Type...
        type Pick<T, K extends keyof T> = {
            [P in K]: T[P];
        };        
        
        // Using the example above of
        // type TodoPreview = Pick<Todo, "title" | "completed">;
        // keyof Todo == 'name' | 'surname' | 'email'
        // `K extends keyof T` means that the resulting type is the super set of 
        //   `'name' | 'surname' | 'email'`, but in the way this function is used, it just
        //    means that K is a selection of the keys of T... extends just allows us
        //    to say that K is of type "keyof Keys". Although K extends the union of the 
        //    types of T, anything "extra" on top of that union can never be picked from T 
        //    anway, so really its just a way of saying the picked keys are the keys in T.
        ```



### Mapped Types
TODO

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
* [Docs](https://www.typescriptlang.org/docs/handbook/generics.html)

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

Caution with Generics v.s. union types and the differences:
```
class MyClass<T extends number | string> {
    function somFunc(p1: T) { ... } //< When class is instantiatied T is ONE type: not either a num or str!
                                    //  Whereas, had a union type been used, it could be either.
}
```

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
```

#### Read Only Types

```
const junk: Readonly<int[]> = [1, 2]
junk.push(3); // TS will complain (JS will just do it - JS can freeze arrays!)
```


## Decorators
* In `tsconfig.json` make sure you have selected `es6` as the `target` and add/set `experimentalDecorators` to `true`.
* The `@` symber prefixes decorators, and a function name should follow it. The number of args the decorator function
  accepts depends on how it is used.
    * For *classes* the function should take one argument, the constructor function.
    * For class *properties* the function should take two arguments, the target of the property being decorated (receives the object prototype or the constructor function if it is a static class) and property name.
    * For *accessor* decorators, same as for properties but with a second as the name of the accessor/param, third parameter of type [`PropertyDescriptor`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty).
        * For *methods* its the same.
        * For *parameters* get target, name, and *position*
* Executors execute when the class is *defined*, not when it is instatiated!

```
function MyFirstDecorator(constructor: Function) {
    console.log("I decorated it");
}

@MyFirstDecorator
class MyClass {
    constructor() {
        console.log("Creating MyClass");
    }
}

// Output will be (because decorator runs at class definition):
// I decorate it
```

* A secorator *factory* is a function that returns a decorator and allows the returned decorator
  to thus be configured. 

```
function MyFirstDecoratorFACTORY(some_config: any) {
    return function(constructor: Function) {
        console.log(
            "I decorated it with " + some_config
        );
    }
}

@MyFirstDecoratorFACTORY("Example config")
class MyClass {
    constructor() {
        console.log("Creating MyClass");
    }
}

// Output will be (because decorator runs at class definition):
// I decorate it with Example config
```

* *Multiple* decorators can be added to a class. The execute in *bottom-ip* order: i.e. decorator closest to class definition first and
  the one furthest away last:

```
@This_Decorator_Executes_Last
...
@This_Decorator_Executes_Second
@This_Decorator_Executes_First
class MyCLass { ... }
```

### Decorators Returning Values
* Class decorators can return a *new constructor function* that will replace the old one.

```
function MyDecorator(orig_constructor: any) {
    ...
    return class extends orig_constructor { // Returning new class but remember class is SYNTACTIC 
                                            // SUGAR for a constructor function!
        constructor() {
            super(): // Construct the child!!
            // ... the replacement constructor, which because super() is called has all the
            // original functionality plus whatever we do here, and this log will only
            // execute when the class is instatiated.
        }
    }
}
```

* Method and accessor decorators can also return vales.
  * Return new [`PropertyDescriptor`s](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty).
    *  By default, values added using `Object.defineProperty()` are immutable and not enumerable.


* Any other decorators (properties and values) have their return values ignored.


### Example Class Function Decorator
* [See the docs](https://www.typescriptlang.org/docs/handbook/decorators.html#method-decorators)
* From the docs: 
  * The expression for the method decorator will be called as a function at runtime, with the following three arguments:
      1. Either the constructor function of the class for a static member, or the prototype of the class for an instance member.
      2. The name of the member.
      3. The Property Descriptor for the member.
* See also: [Medium article on PropertyDescriptor](https://medium.com/jspoint/a-quick-introduction-to-the-property-descriptor-of-the-javascript-objects-5093c37d079#:~:text=A%20property%20descriptor%20is%20a,value%20and%20other%20meta%2Ddata.&text=In%20the%20above%20example%2C%20we,with%20myPropOne%20and%20myPropTwo%20properties.)
  > When we create a JavaScript object ... and add some properties to it, each property (key) gets a default property descriptor. A property descriptor is a simple JavaScript object associated with each property of the object that contains information about that property such as its value and other meta-data.
  >
  > ...
  > The `value` property of the property descriptor is the current value of the property, `writable` is whether the user can assign a new value to the property, `enumerable` is whether this property will show up in enumerations like for in loop or for of loop or Object.keys etc. The `configurable` property tells whether the user has permission to change property descriptor ...
  >
  > ...
  > `get` (getter) and `set` (setter) for a property can also be set in property descriptor with these exact keys. But when you define a getter, it comes with some sacrifices. You can not have an initial value or `value` key on the descriptor at all because the getter will return the value of that property. You can not use `writable` key on descriptor as well, because your writes are done through the setter and you can prevent writes there.


```
function MyDecorator(target: any, name: string, descriptor: PropertyDescriptor) {
    // target is the class prototype 
    // name is the string "myFunction"
    // descriptor is the property descriptor for 
    console.log(target)
    console.log(name)
    console.log(descriptor)

    // descriptor.value == the original method
    // ^^ This is what lets you either replace the function completely or
    //    wrap it g(f(x)) style.

    // Create a new, ajusted descriptor to override/augment the function
    // being decorated.
}

// ...

class A {
    @MyDecorator
    myFunction(...) {
        ...
    }
}
//
// Outputs the following from the decorator:
//     V {constructor: ƒ, myFunction: ƒ}
//         V constructor: class A
//             length: 0
//             name: "A"
//         V prototype:
//             > constructor: class A
//             > myFunction: ƒ myFunction()
//             > [[Prototype]]: Object        
//             arguments: (...)
//             caller: (...)
//             [[FunctionLocation]]: VM124:19
//             > [[Prototype]]: ƒ ()
//             [[Scopes]]: Scopes[6]
//         > myFunction: ƒ myFunction()
//         [[Prototype]]: Object
//     
//     myFunction
//     
//     V {writable: true, enumerable: false, configurable: true, value: ƒ}
//         configurable: true
//         enumerable: false
//         V value: ƒ myFunction()         <<<< THIS IS THE FUNCTION ITSELF
//             length: 0
//             name: "myFunction"
//             arguments: (...)
//             caller: (...)
//             [[FunctionLocation]]: VM124:20
//             > [[Prototype]]: ƒ ()
//             > [[Scopes]]: Scopes[6]
//         writable: true
//         [[Prototype]]: Object
```

### Example Class property Decorator
* The expression for the property decorator will be called as a function at runtime, with the following two arguments:
    1. Either the constructor function of the class for a static member, or the prototype of the class for an instance member.
    2. The name of the member.
* See [this good example](https://dev.to/danywalls/using-property-decorators-in-typescript-with-a-real-example-44e)

    ```
    function(prototypeOrConstructor: Object, propertyKey: string) {
        // Can for example add a setter and getter to the property.
        Object.defineProperty(target, propertyKey, {
        get: () => { ... },
        set: () => { ... }
        }); 
    }
    ```