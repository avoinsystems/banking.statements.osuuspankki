banking.statements.osuuspankki
==============================

This is a plugin for use with ofxstatement package. It implements
parsers for different statement entry CSV formats that have been
used by Osuuspankki of Finland.

There is support for both personal and corporate CSV export formats.

How to use
==========

- install ofxstatement
- install this plugin
- `ofxstatement edit-config`

```
[Osuuspankki]
plugin = op
account = FIVVXXXXYYYYZZZZWW
currency = EUR
```
