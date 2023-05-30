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

#### An Annoyance With Python
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

