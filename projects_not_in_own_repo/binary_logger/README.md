# Binary Logger

In a previous life a collegue had generated a binary logger. All C files were passed through a script that added a
unique tag to each log() call so that this tag could be written to the log, instead of a string, and then when the
log was ready back, the tags would be translated back into strings, with the attached data payload.

This worked really well. The only issue is that it requires a database to be associated with each binary compiled,
which could be hard to keep track of.

What would be really nice is if the ELF file contained everything needed and no pre-parsing of C code before
feeding it to the compiler was necessary.

Well... the latter part is possible, but is the former? How can the tag, whatever it is, be mapped to a string
in the the ELF without that string taking up actual memory in the program image. This would be like the.debug_info
section, which is emitted by the compiler but takes up no room in the program binary file - its in the ELF but
in the binary form is not used. These sections, in the ELF, have tahe SHF_ALLOC __removed__. Or someting like a
linker file variable that has an address but no memory behind it! Ie it has a symbol table entry but no memory
behind it. Can such things be created from C code? If we could then we could have an entry for each string and
just use its index in the log. I think this isn't possible.

So... can write the PC plus some user data to log. When parsing log pass PC to addr2line to get the file and
line number. But then how to get the debug string? Have to go back to the _source_ which is even worse than
needing a DB, so not sure how on earth can get away from needing a separate DB file. I think it is not
possible. So always will have the problem of a separate DB file.

Then the only question is how to generate the DB file. Either do it as described or sift though code to
find each output line.

Hmm... Id also like to be able to convert enums to their textual name etc. Do do that a source code
parse is needed.

So may as well use a pre parse coz then the debug index/tag may not have to be 32-bits wide as it would
if using the PC (on 32 bit target).

Could use google protobuf number format where MSB indicates if number continues...

So format of log is
ID,NUM_PARAMS,PARAMS....,ID...

An the index file maps ID to a string.
PARAM is just a binary blob formetted as per format string.
Format string could also indicate type for enums... then DB also needs enum type name to value-string map, which is doable.
Another useful thing would be masks.




