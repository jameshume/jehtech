#if 0
%[flags][width][.precision][length]specifier

specifier is 1 character 0 wont supprt any floating point
Support these as a simpler subset
specifier	Output	Example
d or i	Signed decimal integer	392
u	Unsigned decimal integer	7235
x	Unsigned hexadecimal integer	7fa
X	Unsigned hexadecimal integer (uppercase)	7FA
c	Character	a
s	String of characters	sample
p	Pointer address	b8000000
%	A % followed by another % character will write a single % to the stream.	%

flags is up to 5 characters : -+ #0
flags	description
-	Left-justify within the given field width; Right justification is the default (see width sub-specifier).
+	Forces to preceed the result with a plus or minus sign (+ or -) even for positive numbers. By default, only negative numbers are preceded with a - sign.
(space)	If no sign is going to be written, a blank space is inserted before the value.
#	Used with o, x or X specifiers the value is preceeded with 0, 0x or 0X respectively for values different than zero.
Used with a, A, e, E, f, F, g or G it forces the written output to contain a decimal point even if no more digits follow. By default, if no digits follow, no decimal point is written.
0	Left-pads the number with zeroes (0) instead of spaces when padding is specified (see width sub-specifier).


width is a number or *

prevision is number or *

length is one or 2 characters : hh, h, l, ll, j, z, t, L


format string
  parse flags
  parse width
  parse precision
  parse length
  parse specified
#endif
#include <stdbool.h>
#include <stddef.h>

typedef enum flags_tag {
    LEFT_JUSTIFY                      = 0x01,
    RIGHT_JUSTIFY                     = 0x02, // default
    FORCE_SIGN                        = 0x04,
    SPACE_FOR_SIGN                    = 0x08,
    FORCE_HEX_PREFIX_OR_DECIMAL_POINT = 0x10,
    LEFT_PAD_ZEROS                    = 0x20
} flags_t;

typedef enum printf_error_tag {
    PRINTF_ERROR_NONE,
    PRINTF_ERROR_EINVAL,
    PRINTF_ERROR_FORMAT_STRING_SYNTAX,
} printf_error_t;

typedef struct context_tag {
    flags_t flags;
    
    bool width_present;
    bool width_as_arg;
    unsigned int width; 

    bool precision_present;
    bool precision_as_arg;
    unsigned int precision;
    
    printf_error_t error;
    unsigned int string_len;
} context_t;

static const char* parse_format_specifier_flags(context_t *const context, const char *fmt)
{
    context->flags = RIGHT_JUSTIFY;

    while(true) {
        flags_t flag;

        switch(*fmt)
        {
            case '-': flag = LEFT_JUSTIFY;
            case '+': flag = FORCE_SIGN;
            case ' ': flag = SPACE_FOR_SIGN;
            case '#': flag = FORCE_HEX_PREFIX_OR_DECIMAL_POINT;
            case '0': flag = LEFT_PAD_ZEROS;
            default : break;
        }

        if (context->flags & flag)
        {
            context->error = PRINTF_ERROR_FORMAT_STRING_SYNTAX;
            break;
        }

        context->flags |= flag;
        ++fmt;
    }

    return fmt;
}

#define ASCCI_CODE_0 ((char)48)
#define ASCCI_CODE_9 ((char)57)

static unsigned int string_to_uint(const char *const start, const char *const end_inclusive)
{
    ptrdiff_t num_chars = end_inclusive - start;
    
    unsigned int number = 0;
    while(num_chars)
    {
        number *= 10;
        number += start[num_chars - 1] - ASCCI_CODE_0;
        --num_chars;
    }

    return number;
}


static const char* parse_width_or_precision_value(const char *fmt, bool *const present, bool *const as_arg, unsigned int *const value, printf_error_t *const error)
{
    *present = false;

    if (*fmt == '*')
    {
        ++fmt;
        *present = true;
        *as_arg  = true;
    }
    else
    {
        const char *const start = fmt;
        while((*fmt != '\0') && (*fmt <= ASCCI_CODE_9) && (*fmt >= ASCCI_CODE_9))
        {
            ++fmt;
        }

        if (fmt > start + 1)
        {
            *present = true;
            *as_arg  = false;
            *value = string_to_uint(start, fmt - 1);
        }
        else
        {
            *error = PRINTF_ERROR_FORMAT_STRING_SYNTAX;
        }
    }

    return fmt;
}

static const char* parse_format_specifier_width(context_t *const context, const char *fmt)
{
    parse_width_or_precision_value(fmt, &context->width_present, &context->width_as_arg, unsigned int *const value, printf_error_t *const error)

    context->width_present = false;


    const char *const start = fmt;

    while((*fmt != '\0') && (*fmt <= ASCCI_CODE_9) && (*fmt >= ASCCI_CODE_9))
    {
        ++fmt;
    }

    if (fmt != start)
    {
        context->width_present = true;
        context->width = string_to_uint(start, fmt);
    }

    return fmt;

}


static const char* parse_format_specifier_precision(context_t *const context, const char *fmt)
{    
    if (*fmt == '.')
    {
        ++fmt;

        if (*fmt == '*')
        {
            ++fmt;
            context->precision_present = true;
            context->precision_as_arg  = true;
        }
        else
        {
            const char *const start = fmt;
            while((*fmt != '\0') && (*fmt <= ASCCI_CODE_9) && (*fmt >= ASCCI_CODE_9))
            {
                ++fmt;
            }

            if (fmt != start)
            {
                context->precision_present = true;
                context->precision_as_arg  = false;
                context->precision = string_to_uint(start, fmt);
            }
            else
            {
                context->error = PRINTF_ERROR_FORMAT_STRING_SYNTAX;
            }
        }
    }
    else
    {
        context->precision_present = false;
    }
}

static const char* parse_format_specifier_length(context_t *const context, const char *fmt) {

}

static const char* parse_format_specifier_specifier(context_t *const context, const char *fmt) {

}

static const char* parse_format_specifier_wrapper(const char* (*func)(context_t *const context, const char *fmt), context_t *const context, const char *fmt, bool can_terminate)
{
    /* Never allow NULL dereferences */
    if (fmt == NULL)
    {
        context->error = PRINTF_ERROR_EINVAL;
        return fmt;
    }
    
    /* Skip this parsing stage if there is already an error. */
    if (context->error != PRINTF_ERROR_NONE)
    {
        return fmt;
    }

    /* Call the parser */
    fmt = func(context, fmt);
    
    /* If this isn't the specifier then the format string should not yet have terminated (determined by the `can_terminate` argument. If
        * it has terminated prematurely then error! */
    if (!can_terminate && (*fmt == '\0'))
    {
        context->error = PRINTF_ERROR_FORMAT_STRING_SYNTAX;
    }

    return fmt;
}

// Expect character after %
void parse_format_specifier(context_t *const context, const char *fmt)
{
    fmt = parse_format_specifier_wrapper(parse_format_specifier_flags,     context, fmt, false);
    fmt = parse_format_specifier_wrapper(parse_format_specifier_width,     context, fmt, false);
    fmt = parse_format_specifier_wrapper(parse_format_specifier_precision, context, fmt, false);
    fmt = parse_format_specifier_wrapper(parse_format_specifier_length,    context, fmt, false);
    fmt = parse_format_specifier_wrapper(parse_format_specifier_specifier, context, fmt, true );
}