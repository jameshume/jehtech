## REPL Files
### EXTI
Taken from the `stmh743.repl` file one can see the following:

```
exti: IRQControllers.STM32H7_EXTI @ sysbus 0x58000000
    [0-4] -> nvic@[6-10]
    [5-9] -> nvicInput23@[0-4]
    [10-15] -> nvicInput40@[0-5]
    [16-19] -> nvic@[1, 41, 2, 3]
    [20, 21] -> nvicInput137@[0-1]
    [22-24] -> nvic@[31, 33, 72]
    ...
```

It has the format \[exti event number\] -> nvic@\[nvic position\].

From RM0433 Rev 8, under section "19.1.2 Interrupt and exception vectors" we get:

![](##IMG_DIR##/stm32h7_exti_to_nvic_map.jpg)