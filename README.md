# quickinfo-parser

A Python script for reading *QuickInfo* formatted text files to a Python dictionary.

**QuickInfo format (.qi)**

A simplistic data storage format based off of key-value pairs.

**EXAMPLE:**

```
#/QUICKINFO - * Comments start with a '#' and can be placed before and after a file starts and ends. *

-                                        <-- * Start of readable area detected with a dash; *
welcome: hello world! Hello World!
key: value                             # Comments can be placed anywhere after values!
integers: 125                          # Integers and floats can be converted
floats: 95.23                          #
lists: / abc, def, 12, 59.2, xyz \     # '/' can be used to start a list, and '\' to end a list, with commas separating values.
nested_list: / a, b, / c, d \ e, f \   # Lists can be nested, however, individual elements after a nested list must not be preceded by a comma.
#                            ^
as_number: 500                         # By default, numbers are converted to their Python equivalents.
as_string: '500                        # If you want to denote the element as a string, use a ' directly before the number.
-                                        <-- * End of area to read denoted with a second dash; *
```

**RESULT**

Python dictionary:

```
{
   'welcome': 'hello world! Hello World!',
   'key': 'value',
   'integers': 125,
   'floats': 95.23
   'lists': ['abc', 'def', 12, 59.2, 'xyz'],
   'nested_list': ['a', 'b', 'e', 'f', ['c', 'd']],
   'as_number': 500,
   'as_string': '500'
}
```
