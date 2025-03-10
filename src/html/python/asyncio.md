A coroutine is a function that can *suspend* and *resume*.

Coroutines are scheduled as *tasks*.

Asyncio module runs a coroutine-based program and does the *cooperative* multitasking between tasks. It does this in te *event loop*, which is the thing that executes the asyncio program.

An event loop is started with `asyncio.run(<coroutine object>)`, which blocks current thread until the asyncio program completes.

Tasks are created with `asyncio.create_task(<coroutine object>)`, registers coroutine in event loop's task queue.

In summary, *coroutines* are scheduled as *tasks* in the *event loop*. Tasks run until they hit an `await`, at which point control is *yielded* back to the *event loop*, which can then run *other* tasks. This is how concurrency is achieved without threads.

* `create_task()` registers coroutine in event loop's task queue.
* `await` yields control to event loop, allowing other tasks to run.
* Event loop "wakes up" tasks when they are ready.
* Tasks are scheduled *cooperatively*, not preemptively.

