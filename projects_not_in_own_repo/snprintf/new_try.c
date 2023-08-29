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
#include <stdint.h>

#define FMT_FLAG_NONE                               0x0000
#define FMT_FLAG_LEFT_JUSTIFY                       0x0001
#define FMT_FLAG_RIGHT_JUSTIFY                      0x0002
#define FMT_FLAG_FORCE_SIGN                         0x0004
#define FMT_FLAG_SPACE_FOR_SIGN                     0x0008
#define FMT_FLAG_FORCE_HEX_PREFIX_OR_DECIMAL_POINT  0x0010
#define FMT_FLAG_LEFT_PAD_ZEROS                     0x0020
#define FMT_FLAG_MASK                               0x003F
#define FMT_FLAG_SET(flag, ctx)                     (ctx)->err_args_flags_bitmask |= (flag)
#define FMT_FLAG_CLEAR(flag, ctx)                   (ctx)->err_args_flags_bitmask &= ~(flag)
#define FMT_FLAG_IS_SET(flat, ctx)                  ((ctx)->err_args_flags_bitmask & (flag))

#define ARG_PRESENT_WIDTH                           0x0040
#define ARG_WIDTH_AS_ARG                            0x0080
#define ARG_PRESENT_PRECISION                       0x0100
#define ARG_PRECISION_AS_ARG                        0x0200
#define ARG_MASK                                    0x03C0
#define ARG_SET(flag, ctx)                          (ctx)->err_args_flags_bitmask |= (flag)
#define ARG_CLEAR(flag, ctx)                        (ctx)->err_args_flags_bitmask &= ~(flag)
#define ARG_IS_SET(flat, ctx)                       ((ctx)->err_args_flags_bitmask & (flag))

#define PRINTF_ERROR_NONE                           0x0400
#define PRINTF_ERROR_EINVAL                         0x0800
#define PRINTF_ERROR_FORMAT_STRING_SYNTAX           0x1000
#define PRINTF_ERROR_MASK                           0x1C00
#define PRINTF_ERROR_SET(err, ctx)                  do { (ctx)->err_args_flags_bitmask &= ~PRINTF_ERROR_MASK; (ctx)->err_args_flags_bitmask |= (err); } while(0)
#define PRINTF_ERROR_CLEAR(err, ctx)                (ctx)->err_args_flags_bitmask &= ~(err)
#define PRINTF_ERROR_IS_SET(flag, ctx)              ((ctx)->err_args_flags_bitmask & (flag))

#define LENGTH_SUB_SPECIFIER_HH                     0x2000
#define LENGTH_SUB_SPECIFIER_H                      0x4000
#define LENGTH_SUB_SPECIFIER_LL                     0x6000
#define LENGTH_SUB_SPECIFIER_L                      0x8000
#define LENGTH_SUB_SPECIFIER_J                      0xA000
#define LENGTH_SUB_SPECIFIER_Z                      0xC000
#define LENGTH_SUB_SPECIFIER_T                      0xE000
#define LENGTH_SUB_SPECIFIER_MASK                   0xE000
#define LENGTH_SUB_SPECIFIER_SET(spec, ctx)         do { (ctx)->err_args_flags_bitmask &= ~LENGTH_SUB_SPECIFIER_MASK; (ctx)->err_args_flags_bitmask |= (spec); } while(0)
#define LENGTH_SUB_SPECIFIER_GET(ctx)               (((ctx)->err_args_flags_bitmask & LENGTH_SUB_SPECIFIER_MASK) >> 13)

#define SPECIFIER_UINT                              0x1
#define SPECIFIER_INT                               0x2
#define SPECIFIER_OCTAL                             0x3
#define SPECIFIER_HEX_LOWER                         0x4
#define SPECIFIER_HEX_UPPER                         0x5
#define SPECIFIER_CHAR                              0x6
#define SPECIFIER_STRING                            0x7
#define SPECIFIER_POINTER                           0x8
#define SPECIFIER_NOTHING                           0x9
#define SPECIFIER_PERCENT                           0xA

#define ASCCI_CODE_0                                ((char)48)
#define ASCCI_CODE_9                                ((char)57)

typedef struct context_tag {
    uint16_t err_args_flags_bitmask;  
    uint16_t width; 
    uint16_t precision;
    uint16_t string_len;
    uint8_t  specifier;
} context_t;

#define CONTEXT_INIT_ZERO { 0, 0, 0, 0, 0}

static const char* parse_format_specifier_flags(context_t *const context, const char *fmt)
{
    uint16_t flag;
    
    FMT_FLAG_SET(FMT_FLAG_RIGHT_JUSTIFY, context);

    do {
        flag = FMT_FLAG_NONE;

        switch(*fmt)
        {
            case '-': FMT_FLAG_CLEAR(FMT_FLAG_RIGHT_JUSTIFY, context);
                      flag = FMT_FLAG_LEFT_JUSTIFY;                      break;
            case '+': flag = FMT_FLAG_FORCE_SIGN;                        break;
            case ' ': flag = FMT_FLAG_SPACE_FOR_SIGN;                    break;
            case '#': flag = FMT_FLAG_FORCE_HEX_PREFIX_OR_DECIMAL_POINT; break;
            case '0': flag = FMT_FLAG_LEFT_PAD_ZEROS;                    break;
            default :                                                    break;
        }

        if (FMT_FLAG_IS_SET(flag, context))
        {
            PRINTF_ERROR_SET(PRINTF_ERROR_FORMAT_STRING_SYNTAX, context);
            break;
        }

        if (flag != FMT_FLAG_NONE)
        {
            FMT_FLAG_SET(flag, context);
            ++fmt;
        }
    } while (flag != FMT_FLAG_NONE);

    return fmt;
}



static uint16_t string_to_uint16(const char *const start, const char *const end_inclusive)
{
    const ptrdiff_t num_chars = end_inclusive - start;

    unsigned int number = 0;
    for(ptrdiff_t idx = 0; idx < num_chars; ++idx)
    {
        number *= 10;
        number += start[idx] - '0';
    }

    return number;
}


static const char* parse_width_or_precision_value(
        const char *fmt, uint16_t *const value, const uint16_t present_bitmask,
        const uint16_t as_arg_bitmask, context_t *const context)
{
    if (*fmt == '*')
    {
        /* The value is not part of the format string. It is provided as a parameter */
        ++fmt;
        ARG_SET(present_bitmask, context);
        ARG_SET(as_arg_bitmask, context);
    }
    else
    {
        /* The value is part of the format string. Parse it out. */
        const char *const start = fmt;
        while((*fmt != '\0') && (*fmt <= '9') && (*fmt >= '0'))
        {
            ++fmt;
        }

        if (fmt > start)
        {
            ARG_SET(present_bitmask, context);            
            *value = string_to_uint16(start, fmt);
        }
        else
        {
            /* The field is not present */
        }
    }

    return fmt;
}

static const char* parse_format_specifier_width(context_t *const context, const char *fmt)
{
    return parse_width_or_precision_value(
        fmt, &context->width, ARG_PRESENT_WIDTH, ARG_WIDTH_AS_ARG, context);
}


static const char* parse_format_specifier_precision(context_t *const context, const char *fmt)
{    
    if (*fmt == '.')
    {
        ++fmt;

        fmt = parse_width_or_precision_value(
            fmt, &context->precision, ARG_PRESENT_PRECISION, ARG_PRECISION_AS_ARG, context);

    }
    return fmt;
}

static const char* parse_format_specifier_length(context_t *const context, const char *fmt)
{
    // length is one or 2 characters : hh, h, l, ll, j, z, t
    // because doubles not supported "L" is not supported
    switch (*fmt)
    {
        case 'h':
            ++fmt;
            if (*fmt == 'h')
            {
                ++fmt;
                LENGTH_SUB_SPECIFIER_SET(LENGTH_SUB_SPECIFIER_HH, context);
            }
            else
            {
                LENGTH_SUB_SPECIFIER_SET(LENGTH_SUB_SPECIFIER_H, context);
            }
            break;

        case 'l':
            ++fmt;
            if (*fmt == 'l')
            {
                ++fmt;
                LENGTH_SUB_SPECIFIER_SET(LENGTH_SUB_SPECIFIER_LL, context);
            }
            else
            {
                LENGTH_SUB_SPECIFIER_SET(LENGTH_SUB_SPECIFIER_L, context);
            }
            break;

        case 'j':
            ++fmt;
            LENGTH_SUB_SPECIFIER_SET(LENGTH_SUB_SPECIFIER_J, context);
            break;

        case 'z':
            ++fmt;
            LENGTH_SUB_SPECIFIER_SET(LENGTH_SUB_SPECIFIER_Z, context);
            break;

        case 't':
            ++fmt;
            LENGTH_SUB_SPECIFIER_SET(LENGTH_SUB_SPECIFIER_T, context);
            break;
    }

    return fmt;
}

static const char* parse_format_specifier_specifier(context_t *const context, const char *fmt)
{
    // because floats not supported only supported specifiers are d i u o x X c s p n %
    switch (*fmt)
    {
        case 'd':
        case 'i': context->specifier = SPECIFIER_INT;                          break;
        case 'u': context->specifier = SPECIFIER_UINT;                         break;
        case 'o': context->specifier = SPECIFIER_OCTAL;                        break;
        case 'x': context->specifier = SPECIFIER_HEX_LOWER;                    break;
        case 'X': context->specifier = SPECIFIER_HEX_UPPER;                    break;
        case 'c': context->specifier = SPECIFIER_CHAR;                         break;
        case 's': context->specifier = SPECIFIER_STRING;                       break;
        case 'p': context->specifier = SPECIFIER_POINTER;                      break;
        case 'n': context->specifier = SPECIFIER_NOTHING;                      break;
        case '%': context->specifier = SPECIFIER_PERCENT;                      break;
        default:  PRINTF_ERROR_SET(PRINTF_ERROR_FORMAT_STRING_SYNTAX, context); break;
    }

    if (!PRINTF_ERROR_IS_SET(PRINTF_ERROR_NONE, context))
    {
        ++fmt;
    }

    return fmt;
}

static const char* parse_format_specifier_wrapper(
        const char* (*func)(context_t *const context, const char *fmt), context_t *const context,
        const char *fmt, bool can_terminate)
{
    /* Never allow NULL dereferences */
    if (fmt == NULL)
    {
        PRINTF_ERROR_SET(PRINTF_ERROR_EINVAL, context);
        return fmt;
    }
    
    /* At this point the string should not yet have terminated */
    if (*fmt == '\0')
    {
        PRINTF_ERROR_SET(PRINTF_ERROR_FORMAT_STRING_SYNTAX, context);
        return fmt;
    }

    /* Call the parser */
    fmt = func(context, fmt);
    
    /* If this isn't the specifier then the format string should not yet have terminated (determined
     * by the `can_terminate` argument. If it has terminated prematurely then error! */
    if (!can_terminate && (*fmt == '\0'))
    {
        PRINTF_ERROR_SET(PRINTF_ERROR_FORMAT_STRING_SYNTAX, context);
    }

    return fmt;
}

// Expect character after %
static void parse_format_specifier(context_t *const context, const char *fmt)
{
    /* Parse the flags, if any */        
    if (!PRINTF_ERROR_IS_SET(PRINTF_ERROR_NONE, context))
    {
        fmt = parse_format_specifier_wrapper(parse_format_specifier_flags, context, fmt, false);
    }

    /* Parse the width specifier, if any */
    if (!PRINTF_ERROR_IS_SET(PRINTF_ERROR_NONE, context))
    {
        fmt = parse_format_specifier_wrapper(parse_format_specifier_width, context, fmt, false);
    }
    
    /* Parse the precision specified, if any */
    if (!PRINTF_ERROR_IS_SET(PRINTF_ERROR_NONE, context))
    {
        fmt = parse_format_specifier_wrapper(parse_format_specifier_precision, context, fmt, false);
    }

    /* Parse the length specifier, if any */
    if (!PRINTF_ERROR_IS_SET(PRINTF_ERROR_NONE, context))
    {
        fmt = parse_format_specifier_wrapper(parse_format_specifier_length, context, fmt, false);
    }
    
    /* Parse the type specifier */
    if (!PRINTF_ERROR_IS_SET(PRINTF_ERROR_NONE, context))
    {
        fmt = parse_format_specifier_wrapper(parse_format_specifier_specifier, context, fmt, true);
    }
}

#include <stdio.h>
void iterate_over_format_string(const char *fmt)
{
    char c;
    while ((c = *fmt) != '\0')
    {
        if (c == '%')
        {
            ++fmt;

            context_t context = CONTEXT_INIT_ZERO;
            parse_format_specifier(&context, fmt);
            printf("context.err_args_flags_bitmask : 0x%X\n", context.err_args_flags_bitmask);
            printf("   errors : 0x%X\n", context.err_args_flags_bitmask & PRINTF_ERROR_MASK);
            printf("context.width                  : %u\n", context.width);
            printf("context.precision              : %u\n", context.precision);
            printf("context.specifier              : %u\n", context.specifier);
            printf("context.string_len             : %u\n", context.string_len);
        }
        else
        {
            ++fmt;
        }
    }
}

int main(int argc, char *argv[])
{
    iterate_over_format_string(argv[1]);
}