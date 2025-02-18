## Comments
```
--Comment
--[[
This is a multi
line comment
]]
```

## Configure LUA To Use 32-bit Numbers!

See `LUA_32BITS` in file `luaconf.h`


## Command Line Options

```
% lua -i prog run chunk then interaction
```

Or use `dofile(<filename>)`


The `-e` option allows us to enter code directly into the command line, like here:
```
 % lua -e "print(math.sin(12))"
```

The `-l` option loads a library. A

## Globals
Global variables do not need declarations; we simply use them

## Conditionals
DIFFERENT FROM C-LIKE LANGUAGES:
Conditional tests (e.g., conditions in control structures) consider both the Boolean false and nil
as false and anything else as true. In particular, Lua considers both zero and the empty string as true in
conditional tests.


## Flow Control

### Ifs
```lua
if op == "+" then
    r = a + b
elseif op == "-" then
    r = a - b
else
    error("invalid operation")
end
```

### While
```lua
local i = 1
while a[i] do
    print(a[i])
    i = i + 1
end
```

### Repeat
```lua
repeat
    line = io.read()
until line ~= ""
```

### For
Numerical:

```lua
for var=start_exp,stop_exp,step_exp do
   something
end
```

Generic:

```lua
t = {10, print, x = 12, k = "hi"}
for k, v in pairs(t) do --< order that elements appear in a traversal is undefined.
   print(k, v)
end
```


## Strings

Strings in Lua are immutable values. We cannot change a character inside a string, as we can in C;

We can get the length of a string using the length operator (denoted by `#`):

```lua
 a = "hello"
 print(#a) --> 5
 print(#"good bye") --> 8
```

Concat with `..`:

```lua
> "Hello " .. "World" --> Hello World
> "result is " .. 3 --> result is 3
```

Long string literals:
```lua
longtext = [==[
            ^^
            Can add zero or more equals between brackets if we need to write a = b[c[1]], for example 
blah
blah
==]]
```

String library
`string.len(s) === #s`


## Tables
Only data structuring mechanism. They represent arrays, sets, records, and many other data structures. Just an associative array.

```lua
> a = {} -- create a table and assign its reference
> b = a -- 'b' refers to the same table as 'a'
```


Table fields evaluate to nil when not initialized.


`a.name` is syntactic sugar for `a["name"]`
### Constructing Tables
#### Tables As Lists
Indexing is 1 based not 0 based!!!

```lua
days = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"}
print(days[1]) --> Sunday
```


#### Record Style (Kinda Like A Struct)

```lua
a = {x = 10, y = 20}
-- Equivalent to
-- a = {}; a.x = 10; a.y = 20
```

#### Mix List and Record Style

```lua
polyline = {color="blue",
   thickness=2,
   npoints=4,
   {x=0, y=0},   -- polyline[1]
   {x=-10, y=0}, -- polyline[2]
   {x=-10, y=1}, -- polyline[3]
   {x=0, y=1}    -- polyline[4]
}
```

#### Square Bracket Init

```lua
opnames = {["+"] = "add", ["-"] = "sub",
 ["*"] = "mul", ["/"] = "div"}

 i = 20; s = "-"
 a = {[i+0] = s, [i+1] = s..s, [i+2] = s..s..s}

 print(opnames[s]) --> sub
 print(a[22]) --> ---
```

### Traversal
Use `pairs` iterator:

```lua
t = {10, print, x = 12, k = "hi"}
for k, v in pairs(t) do --< order that elements appear in a traversal is undefined.
   print(k, v)
end
```

Or for lists use `ipairs()` to ensure traversal order.

### Table Library
Functions to operate over lists and sequences.


## Functions
```lua
function functionName(param1, param2, …)
	return 1
end
```

Can call function with less params than defined with - those params are `nil`.

Functions can return multiple results:
```lua
	return 1,2,3
```

Function called as a statement - all returned results dropped
Function called as an expression - only the first result returned kept
Function is last or only expression in list of expressions - All results kept


