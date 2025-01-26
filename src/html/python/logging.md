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
