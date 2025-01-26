## Logging

### Exceptions
```
import logging

logger = logging.getLogger("exception")

try:
    x = 10 / 0
except ZeroDivisionError:
    logger.exception("A divide by zero for some reason!")
```

Will log the exception *with* the traceback...

```
A divide by zero for some reason!
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```


### Log Handlers
Soecify where the logs go.

Common ones:

* `StreamHandler` - Write to stdout and other streams.
* `FileHandler`
* `RotatingFileHandler`
*  `TimedRotatingFileHandler`

If using thread or processes:

* `QueueHandler`
* `QueueListener`

#### Use `basicConfig`
Does basic configuration for the logging system by creating a StreamHandler or FileHandler with a default Formatter and adding it to the root logger.

```
import logging
logging.basicConfig(filename='mylogfile.txt', level=logging.DEBUG)
logging.debug(...)
```

#### Use One Or More Logging Handlers
Use when creating custom logger.
```
logger = logging.getLogger(name="test")
...
file_handler = logging.FileHandler("mylog.txt")
stream_handler = logging.StreamHandler()

logger.add_handler(file_handler)
logger.add_handler(stream_handler)

# The following logs to both a file and standard out
logger.debug(...)
```

Logging handlers provide the following methods to work with threads:

* `aquire()`
* `release()`

Can also use

* `flush()`
* `close()`

### Formatters
Responsible for converting a LogRecord to an output string to be interpreted by a human or external system.

```
logging.Formatter(
    fmt=None,      # Fornat string using the fiven style param for the logged output 
    datefmt=None,  # How to format dates 
    style='%',     # Determines how format string is interpolated
    validate=True, # If true incorrect fmt and style causes ValueError
    *, 
    defaults=None  # dict[str, Any] of default values for custom fields
)
```

```
import logging

logger = logging.getLogger(name=...)

file_handler = logging.FileHandler(...)
logger.add_handler(file_handler)

formatter = logging.Formatter(
    "%(asctime)s - %(names)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

logger.debug(...)
```

The special formatters like `asctime` are part of the `LogRecord` object that the
logger creates, that get passed to the formatters, which convert `LogRecords` to
output strings, consumed by the Handlers.

`LogRecords` have the following properties (taken from the docs):

* name (str) – The name of the logger used to log the event represented by this LogRecord. Note that the 
  logger name in the LogRecord will always have this value, even though it may be emitted by a handler 
  attached to a different (ancestor) logger.
* level (int) – The numeric level of the logging event (such as 10 for DEBUG, 20 for INFO, etc). Note that 
  this is converted to two attributes of the LogRecord: levelno for the numeric value and levelname for the 
  corresponding level name.
* pathname (str) – The full string path of the source file where the logging call was made.
* lineno (int) – The line number in the source file where the logging call was made.
* msg (Any) – The event description message, which can be a %-format string with placeholders for variable 
  data, or an arbitrary object (see Using arbitrary objects as messages).
* args (tuple | dict[str, Any]) – Variable data to merge into the msg argument to obtain the event description.
* exc_info (tuple[type[BaseException], BaseException, types.TracebackType] | None) – An exception tuple 
  with the current exception information, as returned by sys.exc_info(), or None if no exception information is available.
* func (str | None) – The name of the function or method from which the logging call was invoked.
* sinfo (str | None) – A text string representing stack information from the base of the stack in the current 
  thread, up to the logging call.

