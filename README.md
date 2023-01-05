# quickinfo-parser

A Python script for reading *QuickInfo* formatted text files to a Python dictionary.

**QuickInfo format (.qi)**

A simplistic data storage format based off of key-value pairs.

**EXAMPLE:**

```
#/QUICKINFO - *comments start with a '#' and can be placed before and after a file starts and ends.*

-           <-- *Start of readable area detected with a dash;*

welcome: hello world! Hello World!
i am a key: i am a value
wow: not wow

-           <-- *End of area to read denoted with a second dash;*
```

**RESULT**

Python dictionary:

```
{
   'welcome': 'hello world! Hello World!',
   'i am a key': 'i am a value',
   'wow': 'not wow'
}
```


