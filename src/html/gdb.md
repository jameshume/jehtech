## Examining Memory

### Log Buffer In Memory
For really simple logging, a small, wrapping, buffer in memory with a size will do the job. The buffer is just a set of NULL terminated strings.

```
#define MYLOG_SIZE 512
char mylog[MYLOG_SIZE];
size_t mylog_next_free;
```

Assuming that the buffer hasn't wrapped, to get a nice print out of the entries use:

```
x/100s mylog
```

And up the size (`100`) as the buffer grows.

I want to figure out a way to pass `mylog_next_free` as the size, but haven;t yet...