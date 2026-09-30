# Future Unicode standardization

PCB.OTF currently uses the project-assigned Private Use Area range U+E100 onward.
Those codepoints are Unicode-encoded but are not official Unicode characters.

The canonical identity is always the hardware object ID, for example
`hardware:usb_c`. If an official character or sequence eventually exists, the
registry can map the stable object to both the PCB PUA character and the official
codepoint. No standardization effort is allowed to rename an object or recycle a
released PCB assignment.

`statistics.json` records current allocation and relation counts for future use.
