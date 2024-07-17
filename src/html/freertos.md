<style>
    pre > code {
        border: 0;
        background-color: inherit;
        font-size: 90%;
    }
</style>

# FreeRTOS

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

### Ticks
* Tick hook (callback) can be overridden, but is must be AS QUICK AS POSSIBLE because it executes in interrupt context
  and must not call any API functions that do not end in `...FromISR()`.


## IPC

### Queues
* Must `#include "queue.h"`.
* Finite FIFO buffers.
* Blocks on a read if no data is available, blocks on a write if no room in the queue is available.
* Functions: `xQueueCreate()`, `xQueueSend()`, `xQueueSendToFront()`, `xQueueSendToBack()`, `xQueueReceive()`.
    * `QueueHandle_t xQueueCreate(UBaseType_t uxQueueLength, UBaseType uxItemSize)`.
    * `BaseType_t xQueueSend(QueueHandle_t xQueue, const void *pvItemToQueue, TickType xTickToWait)`.
        * The item is queued by copy, not by reference.
    * `BaseType_t xQueueReceive(QueueHandle_t xQueue, void *pvbuffer, TickType xTickToWait)`.
        * The item is received by copy so a buffer of adequate size must be provided.
* Queue sets: A lot like `poll()` - task can receive data from many queues without having to poll each queue.
    * See `configUSE_QUEUE_SETS` in `FreeRTOSConfig.h`. If not present in file define it yourself and set value as 1.
    * `QueueSetHandle_t xQueueCreateSet(const UBaseType_t exEventQueueLength)`, where `exEventQueueLength` is the
       max number of queues that this set can hold.
    * `BaseType_t xQueueAddToSet(QueueSetMemberHandler_t xQueueOrSempahore, QueueSetHandler_t xQueueSet)`.
        * Note `xQueueOrSempahore` is so named because semaphores can also be added to queue sets.
    * ```
    Example
    some thigns
    here
```