# ZeroK Programming Language

ZeroK based on ICE programming language.

## Basics

Integers are written in format v + b + s (v:=value; b:=base; s:=(un)signed)

### Example
8du

Unsigned number 8 with base 10

### Available bases
b = 2; s = 6; o = 8; d = 10; x = 16

### Booleans
The only available bool value is True.
True can be written in the following differing kinds.
True|true|TRUE|TT|tt|T|t

## Operators
### Arithmetic operators
+, -, *, /, %

### Bitwise operators
&, |, ^, !

### Logical operators
=, <, >, <=, >=, !=

### Bool operators
&&, ||, ^^, !!

## Variable declaration
<type> # <ident> <- <value>
