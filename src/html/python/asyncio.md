## Intro

Asyncio module runs a coroutine-based program and does the *cooperative* multitasking between tasks. It does this in te *event loop*, which is the thing that executes the asyncio program.

An event loop is started with `asyncio.run(<coroutine object>)`, which blocks current thread until the asyncio program completes.

A coroutine is a function that can *suspend* and *resume*. Coroutines are scheduled as *tasks*. Calling a coroutine does *not* execute it: it creates and returns an instance of a corouting object that can then be scheduled.

A *task* runs a co-routine in the background and is *independently* schedulable in the asyncio *event loop*. By executing in the background the calling coroutine can continue doing its own thing rather than waiting on the new tasks, for example. It can be queried and canceled, and results and excpetions can be retrieved. The task will execute regalrdless of what else happens in the coroutine that created it.

Tasks are created with `asyncio.create_task(<coroutine object>)`, registers coroutine in event loop's task queue.

In summary, *coroutines* are scheduled as *tasks* in the *event loop*. Tasks run until they hit an `await`, at which point control is *yielded* back to the *event loop*, which can then run *other* tasks. This is how concurrency is achieved without threads.

* `create_task()` registers coroutine in event loop's task queue.
* `await` yields control to event loop, allowing other tasks to run.
* Event loop "wakes up" tasks when they are ready.
* Tasks are scheduled *cooperatively*, not preemptively.

A *future* or *promise* is the handle returned when issuing an asynchronous function call. Can be used to check on the status of the call or get results.

Note the difference between coroutines and tasks. A task wraps a coroutine and will execute independently.

```python
import asyncio

async def myTask():
    print("myTask starts")
    await asyncio.sleep(10)
    print("myTask ends")


async def myFunc():
    print("Creating myTask")
    asyncio.create_task(myTask(), name='myTask')  ## 1 ##
    print("Created myTask")
    for i in range(10):
        print(i)
    ## 2 ##
asyncio.run(myFunc())

## Outputs:
##    Creating myTask
##    Created myTask
##    0
##    1
##    2
##    3
##    4
##    5
##    6
##    7
##    8
##    9
##    myTask starts
```
[[Run on Programiz]](https://www.programiz.com/online-compiler/78tFZeyQdDvla)

In the example above, notice that at point `## 1 ##`, the task is created and scheduled to run, but the coroutine that created it simply continues on its merry way. The `myTask` task doesn't get a chance to run until `myFunc` finishes. This happens because the event loop runs on a single thread and relies on cooperative scheduling. Since `myFunc` doesn't contain any `await` statements, it never yields control back to the event loop, preventing `myTask` from running until `myFunc` is done.

Another difference is that `await`ing on co-routines directly inside other coroutines, does not scheduling the called routine as a background task: instead, it will sequentially waiting for it to complete, whilst offering other tasks the chance to run.


## Task Status
* `task.done()`
* `task.cancelled()`

A task that has finished, either successfully or otherwise. The following situations cause a task to finish:

* Its coroutine finished normally and terminated.
* The coroutine returned deliberately and terminated.
* An exception was thrown and was not handled, terminating the coroutine.
* The task was canceled - `task.cancel('optional message')`. This raises `CancelledError` inside the coroutine, terminating it. However, note
  that if the task's coroutine handles the `CancelledError` it may not cancel.

Exceptions propogate out of an `await`. I.e., if you `await` on a coroutine and it suffers an exception,
that exception is thrown "out of" the `await`:

```python
try:
    await myCoroutine
except asyncio.CancelledError:
    ...
except Exception:
    # Other exceptions thrown by myCoroutine
    ...
```

## Task Results & Exceptions
* `task.result()` returns whatever the coroutine returned, or `None` if nothing was returned.
    * `task.result()` will re-raise the exception that caused the task to end, if it ended in this way.
* You can also check for exceptions in a task using `task.exception()`.
    * It does not return the `CancelledError` exception. It will throw that one!
    * If no exception was raised then it returns `None`.

Exceptions are propogated to the caller when:

* Caller awaits a task
* Caller gets results from task (`task.result()`)

