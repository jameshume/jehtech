## Overview
Protocol Buffers are a language-neutral, platform-neutral extensible mechanism for serializing structured data.

## Protoscope
[Protoscope](https://github.com/protocolbuffers/protoscope) is a useful tool to parse out a binary message into a more human readable form.

```
# Install
wget https://dl.google.com/go/go1.20.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.20.linux-amd64.tar.gz
go install github.com/protocolbuffers/protoscope/cmd/protoscope...@latest

# Use
xxd -r -ps hex.txt | ~/go/bin/protoscope
#          ^^^^^^^
#          File containing ASCII hex dump of message   
```

## NanoPB
[NanoPB](https://github.com/nanopb/nanopb) is a miniature C implementation of the Google's Protocol Buffer specification.

### Short Names For Enums
I really didn't like the way the Protobuf generator prefixes all of the enum names with the tag of the enum. Its a useful thing if you
need to guarantee unqiue names, which in a big project you might need to, but for smaller stuff, and for me just generally, I like
my enum names to be named exactly as I write them.

For example, the following definition:

```
// myenum.proto
enum MyEnum {
    VAL1 = 0;
    VAL2 = 1;
}
```

Generates the following C code:
```
// myenum.pb.h
typedef enum _MyEnum {
    MyEnum_VAL1;
    MyEnum_VAL2;
} MyEnum;
```

Whereas what I want is the same but without `MyEnum_` prefixed onto `VAL1` and `VAL2`. To accomplish
this one must use the NanoPB options file. Name it as per your definitions file but with the extension `.options`.
In this case `myenum.options`. It would have the following contents to achieve what we want here:

```
MyEnum long_names:false;
```

### Fixed Sized Arrays
#### Repeated Types
Lets say we have an array of 4 `MyEnum` (see above) values. To make NanoPB implement it as a fixed
size array, i.e., generate `MyEnum my_enum_values[4]` one needs to do this:

```
message MyMessage {
    repeated MyEnum my_enum_values = 1 [(nanopb).max_count = 4, (nanopb).fixed_count = true];
    //                                  ^^^^^^^^^^^^^^^^^^      ^^^^^^^^^^^^^^^^^^^^
    //                                  Will be implemented     The message will always contain
    //                                  as an array rather      4 values. If this was missing then
    //                                  than a callback         the array size could be set so &lt;= 4 values
    //                                                          could be transmitted in the message.
}
```

Or use the `.options` file:

```
MyMessage.my_enum_values max_count:4 fixed_count:4; // TODO - check syntax
```

#### Bytes and Strings
If you have a message containing bytes or strings, you will need to use a callback to populate those
fields. Can be a faff. If you just want to copy to an array you can set a maximum size. Then NanoPB
will generate an array of that size as part of the message. You then set the number of array elements
used and write to the array.... simpler than callback stuff.

```
// .proto file
message Blah {
  ...
  bytes payload = 3;
  ...
}


// .options file
Blah.payload max_size:512;


// Generated H file
typedef PB_BYTES_ARRAY_T(512) Blah_payload_t;

typedef struct _Blah {
    ...
    Blah_payload_t payload;
    ...
} Blah;
```

Where `Blah_payload_t` is a struct with the following structure:
```
typedef struct {
    pb_size_t size;
    pb_byte_t bytes[512];
} Blah_payload_t;
```

To initialise the message for encoding you just set `blah.payload.size` to the number of bytes actually
used and copy the same number of bytes into `blah.payload.bytes`. Much less faff than having to implement
a callback.


### Arduino and NanoPB
Assuming you're using the IDE and not you're own makefile, generate the C files as usual, except you
will need to use the `-L quote` and `-Q quote` `nanopb_generator.py` options and just copy them into your projects directory.
You will also need to copy `pb_common.[ch]`, `pb_decode.[ch]`, `pb_encode.[ch]` and `pb.h` into your project directory.

The tool `nanopb_generator.py` will need the `-L quote` and `-Q quote` arguments so that the C files include
the NanoPB headers and generated message headers with quotes rather than pointy backets, which the Arduino IDE
won't like you using.

For example, I used the following for generating files for a project I did recently, which had C
code on a little Arduino and a Python script communicating with the Arduino, piping Protobuf messages
between the PC and Ardunio:

```
python nanopb-0.4.7/generator/nanopb_generator.py -D myiarduino-project-directory -L quote -Q quote -I . -I nanopb-0.4.7/generator/proto *.proto
./nanopb-0.4.7/generator/protoc -I. -I nanopb-0.4.7/generator/proto --python_out=py *.proto
```

#### Arduino Reading And Writing Over Serial
Using the server example from the NanoPB repository it is pretty straight forward to implement on Arduino:

```
static bool read_callback(pb_istream_t *const stream, uint8_t *const buf, const size_t count)
{
    if (count == 0)
    {
        return true;
    }

    Stream &arduino_stream = *(Stream *)stream->state;
    const size_t num_bytes_placed_in_buf = arduino_stream.readBytes((char *)buf, count);
    if (num_bytes_placed_in_buf == 0)
    {
        stream->bytes_left = 0; /* EOF */
    }
    
    return num_bytes_placed_in_buf == count;
}

static pb_istream_t pb_istream_from_stream(Stream &arduino_stream)
{
    pb_istream_t stream = {&read_callback, (void*)&arduino_stream, SIZE_MAX};
    return stream;
}

static bool write_callback(pb_ostream_t *const stream, const uint8_t *const buf, const size_t count)
{
    Stream &arduino_stream = *(Stream *)stream->state;
    const size_t written = arduino_stream.write(buf, count);
    return written == count;
}

static pb_ostream_t pb_ostream_from_stream(Stream &arduino_stream)
{
    pb_ostream_t stream = {&write_callback, (void*)&arduino_stream, SIZE_MAX, 0, nullptr};
    return stream;
}
```

Then in functions that need to write a message over serial:

```
...
Stream &arduino_stream;
...
pb_ostream_t stream = pb_ostream_from_stream(arduino_stream);
pb_encode(&stream, ...);
```

And in functions that need to read a message over serial:

```
...
Stream &arduino_stream;
...
pb_istream_t stream = pb_istream_from_stream(arduino_stream);
pb_decode(&stream, ...);
```

#### Embedding Messages As Sub Messages
To do this you must use `pb_encode_submessage()` as this prefixes the message with a varint length
that is required for submessages. NOTE that this will **encode the submessage twice**, first to
calculate message size and then to actually write it out.

#### Embedding Messages As Bytes
I wanted to send any number of messages in the stream. To do this I borrow the idea of the `Any`
type, except that instead of using a string to identify the message I used an enum. An alternative
would have been to use the `oneof` union-like type... not sure if it would have been a better way
to go?

```
// .proto snippet
message MyMessage {
  MessageId_t id  = 1;
  bytes payload   = 2;
  uint32 crc      = 3;
}

// .options snipped
MyMessage.payload max_size:512;
```

In the above, `payload` will hold other message types. This is how to write embedded messages (note you
do not have to encode the `payload` as a sub message as its just a sequence of bytes from `MyMessage`'s point
of view:

```
static bool write_message_to_stream(
    Stream &arduino_stream,
    const MessageId_t id,
    const pb_msgdesc_t *const payload_fields,
    const void *const payload
)
{
    // Precond - assumes payload_fields and payload are not NULL. Could be made optional.
    MyMessage response;
    
    /* Encode the payload */
    response.has_payload = true;   
    pb_ostream_t payload_stream = pb_ostream_from_buffer(response.payload.bytes, sizeof(response.payload.bytes));
    if (!pb_encode(&payload_stream, payload_fields, payload)) {
        return false;
    }
    response.payload.size = payload_stream.bytes_written;

    /* Encode the rest of the message */
    response.id = id;
    response.crc = static_cast<uint8_t>(response.id);
    response.crc = update_crc_8(response.crc, response.payload.bytes, response.payload.size);

    /* Write out the message on the stream */
    pb_ostream_t response_stream = pb_ostream_from_stream(arduino_stream);
    
    // Use PB_ENCODE_DELIMITED in this scenario so that message prefixed with length over Serial
    // so Python script at other end can read it. See section "An annoyance with Python".
    return pb_encode_ex(&response_stream, ResponseMsg_t_fields, &response, PB_ENCODE_DELIMITED);
```

Then the encode function for messages to be wrapped inside of `MyMessage` become:

```
bool write_specific_msg(Stream &arduino_stream)
{
    MySpecificMessage wrapped;
    ... Construct MySpecficMessage ...

    return write_message_to_stream(
        arduino_stream, LED_TIMELINE_STOP_RSP_MSG_ID, MySpecficMessage_fields, (void *)&wrapped
    );   
}
```


### An Annoyance With Python
On the other end of your connection you might have a Python script doing some processing. The annoying thing
is that although the C implementation can read and write from streams, the Python implementation does not
support this. So annoyingly the only thing I could think of was to us `pb_encode_ex(..., PB_ENCODE_DELIMITED)`
so that the stream has the entire message len prepended as a varint [[Ref]](https://groups.google.com/g/protobuf/c/2m8ihEta1UU/m/0zj2XsTnW8cJ)[[Ref]](https://www.datadoghq.com/blog/engineering/protobuf-parsing-in-python/).

So the C code will do something like:

```
pb_encode_ex(&stream, MyMessage_fields, &my_message, PB_ENCODE_DELIMITED);
```

And the Python has to do something like:

```
MAX_VARINT_BYTES = 10
while True:
    buffer = ser.read(MAX_VARINT_BYTES)
    if len(buffer) > 0:
        break
message_size_bytes, new_pos = _DecodeVarint(buffer, 0)
buffer = buffer[new_pos:]
message_payload = ser.read(message_size_bytes - (MAX_VARINT_BYTES - new_pos))
buffer = buffer + message_payload
```

Probably a better way to do that?

