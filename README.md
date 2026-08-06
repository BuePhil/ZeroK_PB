<<<<<<< HEAD
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
=======
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
```python
<type> # <ident> <- <value>
```

## Arrays
```python
<type>[<size>] # <ident>
<ident>[<index>]
```

## Lists
```python
list with <type> # <ident>
<ident>.get(<index>)
```

### Statements
Every Statement end with ';'

## Conditional statements
```python
if (<cond>) do
  <block>
elif (<cond>) do
  <block>
else do
  <block>
done;
```
elif and else blocks aren't required.

## Iteration
```python
until (<cond>) do
  <block>
done;
```
Until the condition becomes True, the loop will continue
```python
do
  <block>
done
until(<cond>);
```
>>>>>>> 7352c6309e7986dbf434c3b382a8602d3cea2b6c
