<style>
    pre > code {
        border: 0;
        background-color: inherit;
        font-size: 90%;
    }
</style>

## Book
* The book [Mastering the FreeRTOS™ Real Time Kerne](https://www.freertos.org/Documentation/Mastering-the-FreeRTOS-Real-Time-Kernel.v1.0.pdf) is freely available.
* [MPU Support Chapter](https://www.freertos.org/MPU_Chapter.pdf)

## Naming Conventions

* `TickType_t` - Either a U16 or U32 based on FreeRTOS configuration settings.
* `BaseType_t` - U16 on 16-bit architechture, U32 on 32-bit architecture
* Variable prefixes:
    * `c` - char
    * `s` - short or U16
    * `l` - long or U32
    * `x` - `BaseType_t` or any other non-standard types like structures, task handlers etc etc.
    * `u` - unsigned
    * `p` - pointer
    * `v` - void
* Function prefixes:
    * return type letter (see variable prefixes) and then first word is filename, next works are function name:
        * `vTaskPrioritySet` - Function returning void, in `task.c`, function is `PrioritySet`.
* Macro names:
    * Prefix in lower case, giving macro definitions file.
    * Macro name is upper case
    * Examples
        * `portMAX_DELAY` - `port` indicates it is from `portable.h`, and the macro is `MAX_DELAY`.
        * `taskENTER_CRITICAL` - `task` indicates it is from `task.h`
        * `pdTRUE` - `pd` indicates it is from `projdefs.h`
        * `configUSE_PREEMPTION` - `config` indicates it is from `FreeRTOSConfig.h`

## Memory Allocation
I work in systems that generally don't want dynamic memory allocation, so to use static allocation set 
`configSUPPORT_STATIC_ALLOCATION` to `1` in `FreeRTOSConfig.h`.

All functions then need to be replaced with thair `...Static` counterparts:

* `xTaskCreateStatic`
* `xEventGroupCreateStatic`
* `xEventGroupGetStaticBuffer`
* `xQueueGenericCreateStatic`
* `xQueueGenericGetStaticBuffers`
* `xQueueCreateMutexStatic`
    *  if `configUSE_MUTEXES` is `1`
* `xQueueCreateCountingSemaphoreStatic`
    * if `configUSE_COUNTING_SEMAPHORES` is `1`
* `xStreamBufferGenericCreateStatic`
* `xStreamBufferGetStaticBuffers`
* `xTimerCreateStatic`
    * if `configUSE_TIMERS` is `1`
* xTimerGetStaticBuffer
    * if `configUSE_TIMERS` is `1`

If `configSUPPORT_STATIC_ALLOCATION` and `configUSE_TIMERS` are both enabled, the kernel will call
`vApplicationGetTimerTaskMemory()` to allow the application to create and return a memory buffer for the
timer task TCB and the timer task stack.

The `vApplicationGetIdleTaskMemory` function is called to allow the application to create the needed buffers
for the "main" idle task. 

## Tasks

States:

```
                          ┌─────────────────┐                                                       
                          │                 │                                                       
              ┌───────────►   Suspended     ◄───────────────────────┐                               
              │           │                 │                       │                               
              │           └───▲─────────┬───┘                       │                               
              │               │         │                           │ vTaskSusped()                 
              │ vTaskSuspend()│         │ vTaskResume()             │                               
              │               │         │                           │                               
              │               │         │                           │                               
              │           ┌───┴─────────▼───┐              ┌────────┴────────┐                      
              │    ┌┐     │                 ├──────────────►                 │                      
TaskSuspend() │    │┼─────►   Ready         │              │   Running       │                      
              │    └┘     │                 ◄──────────────┤                 │                      
              │           └────────▲────────┘              └────────┬────────┘                      
              │                    │                                │                               
              │                    │                                │                               
              │                    │Event                           │ Blocking API                  
              │                    │                                │ called, which blocks          
              │           ┌────────┴────────┐                       │                               
              │           │                 │                       │                               
              └───────────┤   Blocked       ◄───────────────────────┘                               
                          │                 │                                                       
                          └─────────────────┘                                                       
```

Many of the following functions can be included or excluded from the API definition using macros from `FreeRTOSConfig.h`, such as `INCLUDE_vTaskSuspend()` etc.

### Task Creation & Deletion & Priority
* `BaseType_t xTaskCreate(TaskFunction_t pvTaskCode, const char* pcName, uint16_t usStackDepth, void * pvParameters, UBaseType_t uxPriority, TaskHandle_t *pxCreatedTask)`
    * `x` means it returns `Basetype_t` or other non-standard type.
    * `Task` means it is found in `task.c`
    * Parameters:
        * `pvTaskCode` - Pointer to function that runs the task: `void MyTask(void *pvParameters)`
        * `pcName` - Pointer to string used to identify task during debugging
        * `usStackDepth` - Stack depth - duh
        * `pvParameters` - Pointer to task parameters. May be `NULL`. Opaque to FreeRTPS, just pass
                           a pointer to a `struct` or whatever you like in here.
        * `uxPriority` - Smaller the number the higher the priority. Tasks of equal priority run for a time quanta.
        * `pxCreatedTask` - Used to return the task handle. May be `NULL`.
* `vTaskStartScheduler()` - Once tasks created starts the scheduler.
* `vTaskPrioritySet(TaskHandle_t *pxCreatedTask, UBaseType_t uxPriority)` - 
  Set a task priority dynamically.
  Can use `NULL` task to set threads own priority.
* `uxTaskPriorityGet(TaskHandle_t *pxCreatedTask)` - Get task priority.
* `vTaskDelete(TaskHandle_t *pxCreatedTask)`

### Task State Modification
* `vTaskSuspend(TaskHandle_t *pxCreatedTask)` - Suspend a task. Shouldn't need to call this manually - use correct CRs and scheduling.
* `vTaskResume(TaskHandle_t *pxCreatedTask)` - Resume a task. Shouldn't need to call this manually - use correct CRs and scheduling.
* `vTaskDelay(TickType_t xTicksToDelay)` -
  Causes task to move to the blocked state for a number of ticks. Make sure `INCLUDE_vTaskDelay` is set to `1` in `FreeRTOSConfig.h`.
  Use `pdMS_TO_TICKS()`, e.g. `vTaskDelay(pdMS_TO_TICKS(...))`. See also `xTaskGetTickCount()`.
* `vTaskDelayUntil()`

### Idle Task
* There must be at least one task in the Running state, so the Idle task will run where there are no other tasks pending.
* It is created automatically when the scheduler is started.
* Has lowest priority (0) so that it can never prempt any other task.
* Can add functionality to the task using an Idle hook (Idle callback function), which is called
  automatically by the idle task once per iteration of the idle task loop.
  * See `configUSE_IDLE_HOOK` and `configIDLE_SHOULD_YIELD` in `FreeRTOSConfig.h`.
  * Override weakly linked function `void vApplicationIdleHook(void)`.
* Commonly used to put MCU to sleep - drawback is tick interrupt will cause continual enter/exit from this state!
    * To overcome, FreeRTOS tickless idle mode stops the periodic tick interrupt during idle periods.

### Ticks
* Tick hook (callback) can be overridden, but is must be AS QUICK AS POSSIBLE because it executes in interrupt context
  and must not call any API functions that do not end in `...FromISR()`.

### Context Switching
When a task calls an API function, if `configUSE_PREEMPTION` is set to `1` in `FreeRTOSConfig.h` then the
switch to the higher priority task occurs automatically within the API function, in other words, before the
API function has exited.

## IPC

### Queues
* Must `#include "queue.h"`.
* Finite FIFO buffers.
* Blocks on a read if no data is available, blocks on a write if no room in the queue is available.
* Functions: `xQueueCreate()`, `xQueueSend()`, `xQueueSendFromISR90`, `xQueueSendToFront()`, `xQueueSendToBack()`, `xQueueReceive()`.
    * `QueueHandle_t xQueueCreate(UBaseType_t uxQueueLength, UBaseType uxItemSize)`.
    * `BaseType_t xQueueSend(QueueHandle_t xQueue, const void *pvItemToQueue, TickType xTickToWait)`.
        * The item is queued by copy, not by reference.
    * `BaseType_t xQueueReceive(QueueHandle_t xQueue, void *pvbuffer, TickType xTickToWait)`.
        * The item is received by copy so a buffer of adequate size must be provided.
    * `xQueueSendFromISR()` 
        * Communicate from backend ISR to front end task. Note, of course, that this function cannot block so
         if the queue is full items will be dropped.
* Queue sets: A lot like `poll()` - task can receive data from many queues without having to poll each queue.
    * See `configUSE_QUEUE_SETS` in `FreeRTOSConfig.h`. If not present in file define it yourself and set value as 1.
    * `QueueSetHandle_t xQueueCreateSet(const UBaseType_t exEventQueueLength)`, where `exEventQueueLength` is the
       max number of queues that this set can hold.
    * `BaseType_t xQueueAddToSet(QueueSetMemberHandler_t xQueueOrSempahore, QueueSetHandler_t xQueueSet)`.
        * Note `xQueueOrSempahore` is so named because semaphores can also be added to queue sets.

```C
static QueueHandle_t q1, q2;
static QueueSetHandle_t qset;
...
   // Some init function
   q1 = xQueueCreate(1, sizeof(uint32_t));
   q2 = xQueueCreate(1, sizeof(uint32_t));

   xQueueAddToSet(q1, qset);
   xQueueAddToSet(q2, qset);

...
   // Some recever function
   while(true) {
      QueueHandle_t queue_with_data = (QueueHandle_t)xQueueSelectFromSet(qset, portMAX_DELAY); 
      xQueueReceive(queue_with_data, ...);
      // Do something with data ...
   }
```

### Synchronisation

* Binary Sempahores:
    * `SemaphoreHandle_t xSemaphoreCreateBinary(void)`
    * `BaseType_t xSemaphoreGive(SemaphoreHandle_t xSemaphore)`
    * `BaseType_t xSempahoreGiveFromISR(SempahoreHandle_t xSemaphore, BaseType_t pxHigherPriorityTaskWoken)`
    * `BaseType_t xSemaphoreTake(...)`
* Counting Sempahores:
    * Enable by defining `configUSE_COUNTING_SEMAPHORES` in `FreeRTOSConfig.h`
    * `xSemaphoreCreateCounting(uxMaxCount, uxInitialCount)`
* Mutexes:
    * Enable by defining `configUSE_MUTEXES` in `FreeRTOSConfig.h`
    * Mutexes are binary semaphores that include a priority inheritance mechanism.
    * Not recursive - must use recursive mutexes if you need this.


## Event Groups
* Event groups allow a task to wait in the Blocked state for a combination of one of more events to occur
* Event groups unblock all the tasks that were waiting for the same event, or combination of events, when
  the event occurs.
* Useful for 
    * synchronizing multiple tasks,
    * broadcasting events to more than one task,
    * allowing a task to wait in the Blocked state for any one of a set of events to occur, and
    * allowing a task to wait in the Blocked state for multiple actions to complete.
* `xEventGroupWaitBits()` to wait for any bit to be set and get a mask of all bits set.
* `xEventGroupSync()` to set a bit and wait for all or a selection of other bits to be set.
    *  The function allows a task to set one or more event bits in an event group, then wait 
       for a combination of event bits to become set in the same event group, as a single
       uninterruptable operation.

## Task Notifications
* Inter-task or ISR-task interaction and synchronisation without a communication object like
  a semaphore.
* Optional so must set `configUSE_TASK_NOTIFICATIONS` to `1` in `FreeRTOSConfig.h`.
* Much faster than using a queue, semaphore or event group.
* Requires significantly less RAM.
* `vTaskNotifyGiveFromISR()`

## Interrupt Management
* Never call a FreeRTOS API function that does not have `FromISR` in its name from an ISR.
* `xHigherPriorityTaskWoken`:
    * When an API is used that might cause a context switch, the switch cannot happen in
      the ISR, thus all interrupt safe API functions have a param `xHigherPriorityTaskWoken`.
    * Set `xHigherPriorityTaskWoken` to false before the API call, then if it is true
      after, `portYIELD_FROM_ISR()` needs to be called with the value of `xHigherPriorityTaskWoken`.
      If it is false no context switch is requested, otherwise one is requested.
* *Deferred interrupt processing*: An interrupt service routine must record the cause of
  the interrupt, and clear the interrupt. Any other processing necessitated by the interrupt
  can often be performed in a task, allowing the interrupt service routine to exit as quickly
  as is practical. 

## Software Timers
* Set `configUSE_TIMERS` to `1` in `FreeRTOSConfig.h`.
* Set `configTIMER_TASK_PRIORITY` to desired priority of timer service task.
* Set `configTIMER_QUEUE_LENGTH` for max number of unprocessed commands that timer command queue can hold.
* Set `configTIMER_TASK_STACK_DEPTH` to define stack size for timer service task.
* Timer callback prototype: `void ATimerCallback( TimerHandle_t xTimer )`.
* Timer callbacks must NOT enter blocked state!
* All callback execute in context of timer service task, aka "RTOS daemon task".
* APIs: `xTimerCreate`, `xTimerStart`, `xTimerChangePeriod` ...
