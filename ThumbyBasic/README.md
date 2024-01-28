# Thumby BASIC

Thumby BASIC is a simple programming language designed to run on the [Thumby](https://thumby.us/), a compact and portable gaming console. Thumby BASIC allows you to create text-based programs and games on the Thumby device. This README.md provides an introduction to the syntax, compatibility, limitations, and details about various language components.

## Syntax Overview

Thumby BASIC uses a straightforward syntax with line-numbered statements that is meant to closely mirror other BASIC implementations for compatability. Each line consists of a line number followed by a space and a statement. Statements are separated by newlines. Here's an overview of the language components:

### Input and Output

- `PRINT`: Used to display text on the screen.
  ```
  10 PRINT "Hello Thumby"
  ```

- `INPUT`: Accepts user input and stores it in a variable.
  ```
  20 INPUT X
  ```

### Variables

- Variables are used to store values and can be assigned using the `=` symbol.
  ```
  30 A = 5
  40 B = "Thumby"
  ```

- Variable names are limited to letters (A to Z).

### Logic

- `IF`: Used for conditional logic, allowing you to make decisions based on variable values.
  ```
  50 IF A = 5 THEN GOTO 100
  ```

### Control Flow

- `GOTO`: Used for branching to different parts of the program based on conditions or for creating loops.
  ```
  60 GOTO 30
  ```

## Input and Output

Thumby BASIC supports basic input and output operations:

### `PRINT` Statement

The `PRINT` statement is used to display text on the screen. It can display both constant text and the values of variables. Text to be displayed should be enclosed in double quotes.

Example:
```basic
10 PRINT "Welcome to Thumby BASIC"
20 PRINT "The value of A " + A
```

### `INPUT` Statement

The `INPUT` statement is used to accept user input and store it in a variable. It prompts the user to enter a value.

Example:
```basic
30 INPUT A
40 PRINT "You entered " + A
```

## Variables

Variables in Thumby BASIC are used to store values temporarily. Variable names are single uppercase letters (A to Z). You can assign values to variables using the `=` symbol.

Example:
```basic
50 A = 5
60 B = "Thumby"
```

## Logic

Thumby BASIC provides basic conditional logic using the `IF` statement. You can use it to create conditional branches in your programs.

Example:
```basic
70 IF A = 5 THEN GOTO 100
80 PRINT "A is not equal to 5"
90 GOTO 110
100 PRINT "A is equal to 5"
110 PRINT "End of program"
```

## Control Flow

Control flow in Thumby BASIC is primarily managed using line numbers and the `GOTO` statement. You can use `GOTO` to jump to different parts of the program based on conditions or create loops.

Example:
```basic
120 IF B = "Thumby" THEN GOTO 140
```

## Compatibility

Thumby BASIC is designed specifically for the Thumby gaming console. It may not be compatible with other systems or devices, although it does support running programs on a PC with Python.

## Limitations

Thumby BASIC has several limitations:
- Thumby has severe RAM memory limitations. We recommend reducing nested expressions so the parser doesn't crach from OOM errors
- Designed for simple text-based games and programs.
- No support for functions or complex data structures.

Please refer to the Thumby documentation and examples for more information on the capabilities and limitations of the Thumby device and Thumby BASIC.