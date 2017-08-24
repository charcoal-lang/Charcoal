# Charcoal
<!-- TODO: make this better -->
Want to be able to write basic Charcoal quickly? Then read on. If you came here looking for help, scroll to the bottom for the FAQ.

## Example REPL session

To use the REPL, simply invoke with `./charcoal.py`, `python charcoal.py` or `python3 charcoal.py`.

    Charcoal> Hello, World!  
    Hello, World!
    Charcoal> ^C
    Cleared canvas

## Literals
There are two basic types of literals: strings and numbers. A string is just a run of printable ASCII, and a number is just a run of the superscript digits `⁰¹²³⁴⁵⁶⁷⁸⁹`.

Examples:
`foo` is equivalent to `"foo"`.  
`foo¶bar` is the same as `"foo\nbar"`.  
`¹²³⁴` is `1234`.  

## Printing
In a Charcoal program, expressions are implicitly printed. Numbers print a line, and arrows can be used to specify a direction.

Examples:
`foo` prints `foo`  
`foo⁴` prints `foo----`  
`foo↖⁴` prints:  
```
\   
 \  
  \ 
foo\
```

## FAQ
- When I run Charcoal it throws some errors about UTF-8 characters and exits.
	- Maybe you don't have Python 3 installed. Try installing Python 3 from [here](https://www.python.org/downloads/).
- When I run Charcoal it throws some errors and exits.
	- If the message comes with a stack trace, it looks like you have found a bug. File a bug report [here](https://github.com/somebody1234/Charcoal/issues), and we'll come back to you as soon as we can.

<!-- TODO: set up issue template -->
