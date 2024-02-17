# quickinfo-parser

A Python script for reading *QuickInfo* formatted text files to a Python dictionary.

**QuickInfo format (.qi)**

A simplistic data storage format based off of key-value pairs.

**EXAMPLE:**

```
#/QUICKINFO - * Comments start with a '#' and can be placed before and after a file starts and ends. *

-                                        <-- * Start of readable area detected with a dash; *
welcome: hello world! Hello World!
i-am-a-key: i-am-a-value                 # Comments can be placed anywhere after values!
wow: 125                                 # Integers and floats can be converted
not wow: 95.23                           #
grouped: / abc, def, 12, 59.2, xyz \     # '/' can be used to start a list, and '\' to end a list, with commas separating values.
-                                        <-- * End of area to read denoted with a second dash; *
```

**RESULT**

Python dictionary:

```
{
   'welcome': 'hello world! Hello World!',
   'i-am-a-key': 'i-am-a-value',
   'wow': 125,
   'not wow': 95.23
   'grouped': ['abc', 'def', 12, 59.2, 'xyz']
}
```
