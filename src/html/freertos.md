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
* `BaseType_t xTaskCreate(TaskFunction_t pvTaskCode, const char* pcName, uint16_t usStackDepth, void * pvParameters, UBaseType_t uxPriority, TaskHandle_t *pxCreatedTask)`
    * `x` means it returns `Basetype_t` or other non-standard type.
    * `Task` means it is found in `task.c`
    * Parameters:
        * `pvTaskCode` - Pointer to function that runs the task: `void MyTask(void *pvParameters)`
        * `pcName` - Pointer to string used to identify task during debugging
        * `usStackDepth` - Stack depth - duh
        * `pvParameters` - Pointer to task parameters. May be `NULL`. Opaque to FreeRTPS, just pass
                           a pointer to a `struct` or whatever you like in here.
        * `uxPriority` - Smaller the number the higher the priority.
        * `pxCreatedTask` - Used to return the task handle. May be `NULL`.
* Tasks of equal priority run for a time quanta.
* `vTaskStartScheduler()` - Once tasks created starts the scheduler.
* `vTaskPrioritySet(TaskHandle_t *pxCreatedTask, UBaseType_t uxPriority)` - 
  Set a task priority dynamically.
  Can use `NULL` task to set threads own priority.
* 

