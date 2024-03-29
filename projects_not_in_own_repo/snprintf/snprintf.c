// A little bit of prating around making an snprintf function for cortex-m0. For some reason work didn't use
// nano newlib and found ee_sprintf which doesn't have the "n" variant so I wondered if I could write my own.
// Got some way there but then if you look at things like nano newlib its waaaaay way better so stopping here...
// was a bit of fun.
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stddef.h>
#include <stdint.h>

#include <stdarg.h>
//#define DEBUG(x) printf x
#define DEBUG(x)

/*
 * From https://cplusplus.com/reference/cstdio/printf/#compatibility:
 *
 *    Flags     Description
 *    --------|--------------------------------------------------------------------------------------------------------
 *    -       | Left-justify within the given field width; Right justification is the default (see width
 *            | sub-specifier).
 *    +       | Forces to precede the result with a plus or minus sign (+ or -) even for positive numbers. By default,
 *            | only negative numbers are preceded with a - sign.
 *    (space) | If no sign is going to be written, a blank space is inserted before the value.
 *    #       | Used with o, x or X specifiers the value is preceeded with 0, 0x or 0X respectively for values
 *            | different than zero.
 *            | Used with a, A, e, E, f, F, g or G it forces the written output to contain a decimal point even if no
 *            | more digits follow. By default, if no digits follow, no decimal point is written.
 *    0	      | Left-pads the number with zeroes (0) instead of spaces when padding is specified (see width
 *            | sub-specifier).
 */
typedef struct format_flags_tag
{
    bool left_justify;
    bool force_sign;
    bool no_sign;
    bool force_decimal_point_or_0x_prefix;
    bool left_pad_with_zeros;
} format_flags_t;

/*
 * From https://cplusplus.com/reference/cstdio/printf/#compatibility:
 *
 *    width description
 *    ---------|-------------------------------------------------------------------------------------------------------
 *    (number) | Minimum number of characters to be printed. If the value to be printed is shorter than this number,
 *             | the result is padded with blank spaces. The value is not truncated even if the result is larger.
 *    *        | The width is not specified in the format string, but as an additional integer value argument preceding
 *             | the argument that has to be formatted.
 */
typedef struct format_width_tag
{
    size_t minimum_number_of_characters;
    bool is_specified;
    bool as_extra_argument;
} format_width_t;

typedef struct print_buffer_tag
{
    const char *format;
    size_t size_bytes;
    size_t consumed_bytes;
    char *buffer;
} print_buffer_t;

typedef struct count_and_format_tuple_tag
{
    size_t count;
    const char *format;
} count_and_format_tuple_t;


/*
 * From https://cplusplus.com/reference/cstdio/printf/#compatibility:
 *
 *    .precision | description
 *    -----------|------------------------------------------------------------------------------------------------------
 *    .number    | integer specifiers (d, i, o, u, x, X): precision specifies the minimum number of digits to be
 *               | written. If the value to be written is shorter than this number, the result is padded with leading
 *               | zeros. The value is not truncated even if the result is longer. A precision of 0 means that no
 *               | character is written for the value 0.
 *               |
 *               | For a, A, e, E, f and F specifiers: this is the number of digits to be printed after the decimal
 *               | point (by default, this is 6).
 *               |
 *               | For g and G specifiers: This is the maximum number of significant digits to be printed.
 *               |
 *               | For s: this is the maximum number of characters to be printed. By default all characters are
 *               | printed until the ending null character is encountered. If the period is specified without an
 *               | explicit value for precision, 0 is assumed.
 *               |
 *    .*         | The precision is not specified in the format string, but as an additional integer value argument
 *               | preceding the argument that has to be formatted.
 */
typedef struct format_precision_tag
{
    size_t number_of_digits;
    bool is_specified;
    bool as_extra_argument;
} format_precision_t;


typedef enum format_length_tag
{
    FORMAT_LENGHT_NOT_SPECIFIED,
    FORMAT_LENGHT_H,
    FORMAT_LENGHT_HH,
    FORMAT_LENGHT_J,
    FORMAT_LENGHT_L_DBL,
    FORMAT_LENGHT_L,
    FORMAT_LENGHT_LL,
    FORMAT_LENGHT_T,
    FORMAT_LENGHT_Z,
} format_length_t;


typedef enum format_specifier_tag
{
    FORMAT_SPECIFIER_CHARACTER,
    FORMAT_SPECIFIER_ERROR,
    FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_DECIMAL,
    FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_HEXADECIMAL,
    FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_SCIENTIFIC,
    FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_SHORTEST,
    FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_DECIMAL,
    FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_HEXADECIMAL,
    FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_SCIENTIFIC,
    FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_SHORTEST,
    FORMAT_SPECIFIER_NOTHING,
    FORMAT_SPECIFIER_POINTER_ADDRESS,
    FORMAT_SPECIFIER_SIGNED_DECIMAL_INTEGER,
    FORMAT_SPECIFIER_STRING,
    FORMAT_SPECIFIER_UNSIGNED_DECIMAL_INTEGER,
    FORMAT_SPECIFIER_UNSIGNED_HEXADECIMAL_LOWER_CASE,
    FORMAT_SPECIFIER_UNSIGNED_HEXADECIMAL_UPPER_CASE,
    FORMAT_SPECIFIER_UNSIGNED_OCTAL,
} format_specifier_t;

typedef struct context_tag
{
    print_buffer_t pbuff;
    format_flags_t flags;
    format_width_t width_spec;
    format_precision_t precision_spec;
    format_length_t length_spec;
    format_specifier_t format_spec;
    va_list args;
} context_t;


bool write_character_to_print_buffer(print_buffer_t *const print_buffer, char character)
{
    if (print_buffer->consumed_bytes < print_buffer->size_bytes - 1) /* Make sure trailing '\0' is left */
    {
        print_buffer->buffer[print_buffer->consumed_bytes] = character;
        print_buffer->consumed_bytes += 1;
        print_buffer->buffer[print_buffer->consumed_bytes] = '\0'; /* Always terminate to be safe - could be overwritten if more is added. */
        return true;
    }

    return false;
}

bool write_string_to_print_buffer(print_buffer_t *const print_buffer, const char *const string, const size_t num_characters)
{
    bool rval = false;

    if (print_buffer->consumed_bytes < print_buffer->size_bytes)
    {
        const size_t space_remaining = print_buffer->size_bytes - 1 - print_buffer->consumed_bytes; /* -1 to leave space for trailing '\0' */
        if (space_remaining > 0)
        {
            const size_t bytes_to_write = num_characters > space_remaining ? space_remaining : num_characters;
            memcpy(&print_buffer->buffer[print_buffer->consumed_bytes], string, bytes_to_write);
            print_buffer->consumed_bytes += bytes_to_write;
            rval =  true;
        }
        print_buffer->buffer[print_buffer->consumed_bytes] = '\0'; /* Always terminate to be safe - could be overwritten if more is added. */
    }

    return rval;
}

static const char* chew_not_percent_chars(const char *format)
{
    char current_char;
    
    do 
    {
        current_char = *format++;
    } while(current_char != '\0' && current_char != '%');

    return format - 1;
}



static count_and_format_tuple_t chew_percent_chars(const char *_format)
{
    char current_char;
    count_and_format_tuple_t rval = { .format = _format, .count = 0};
    
    do
    {
        current_char = *rval.format++;
        ++rval.count;
    } while (current_char != '\0' && current_char == '%');

    rval.format -= 1;
    rval.count -= 1;
    return rval;
}

static const char* print_to_buffer_escaped_percents_until_next_specifier(const char *_format, print_buffer_t *const print_buffer)
{
    const char *previous_format;
    count_and_format_tuple_t rval = { .format = _format, .count = 0 };
    
    do 
    {
        if (*rval.format != '\0')
        {
            previous_format = rval.format;
            rval.format = chew_not_percent_chars(rval.format);
            write_string_to_print_buffer(print_buffer, previous_format, rval.format - previous_format);
            /* At this point `rval.format` points to a null character or the first '%' character found. */
        }

        if (*rval.format != '\0')
        {
            /* Have found the first '%'. Chew all consecutive '%' characters, counting the number chewed. */
            rval = chew_percent_chars(rval.format);
            /* At this point `rval.format` points to a null character or the first non-'%' character found. */

            /* Write the escaped '%%''s as single '%''s */
            for(size_t counter = 0; counter < (rval.count >> 1); ++counter) {
                write_character_to_print_buffer(print_buffer, '%');
            }

            if (*rval.format != '\0')
            {
                /* Found a non-'%' character following a sequence of '%' characters. */
                if ((rval.count & 0x1) == 1)
                {
                    /* The number of consecutive '%' characters was odd, therefore the last is not escaped
                     * and is therefore the start of a format specifier. */
                    return rval.format;
                }
                else
                {
                    /* The '%' sequence that was seen was of even length which means that each '%' is escaped and
                     * therefore this sequence contains no format specifier. Continue to chew non-'%' characters. */
                }
            }
            else
            {
                /* The '%' characters reach the end of the string so they cannot be a format specifier. 
                 * If there was an odd number of '%' characters then this could actually be an error but this
                 * is designed to fail silently for simplicity (and it's safe). */
            }
        }
        else
        {
            /* No percent chars found - end of string reached. */
        }
    } while(*rval.format != '\0');

    return rval.format;
}

static const char* parse_format__flags(const char* format, format_flags_t *const flags)
{
    bool no_flag_char_seen = false;
    memset(flags, 0, sizeof(*flags));

    while ((*format != '\0') && (!no_flag_char_seen))
    {
        switch(*format)
        {
            case '-': flags->left_justify = true;                      break;
            case '+': flags->force_sign = true;                        break;
            case ' ': flags->no_sign = true;                           break;
            case '#': flags->force_decimal_point_or_0x_prefix = true;  break;
            case '0': flags->left_pad_with_zeros = true;               break;
            default:  no_flag_char_seen = true;                        return format;
        }

        ++format;        
    }
    
}

static bool is_number_character(const char this_char)
{
    return (this_char >= '0') && (this_char <= '9');
}

static count_and_format_tuple_t parse_format__unsigned_int(const char* _format) {

    count_and_format_tuple_t rval = { .format = _format, .count = 0 };
    char this_char = *rval.format;
    while (is_number_character(this_char)) {
        rval.count *= 10;
        rval.count += (size_t)this_char - (size_t)'0';                    
        ++rval.format;
        this_char = *rval.format;
    }
    return rval;
}



static const char* parse_format__width(const char* format, format_width_t *width_spec)
{
    char this_char = *format;
    memset(width_spec, 0, sizeof(*width_spec));

    if (this_char == '*')
    {
        /* The width is not specified in the format string, but as an additional integer value argument preceding
         * the argument that has to be formatted. */
        width_spec->is_specified = true;
        width_spec->as_extra_argument = true;
        ++format;
    }
    else if (is_number_character(this_char))
    {
        /* Minimum number of characters to be printed. If the value to be printed is shorter than this number, the
         * result is padded with blank spaces. The value is not truncated even if the result is larger. */
        const count_and_format_tuple_t count_and_format = parse_format__unsigned_int(format);
        format = count_and_format.format;
        width_spec->is_specified = true;
        width_spec->minimum_number_of_characters = count_and_format.count;
    }
    else 
    {
        /* There is no width specifier present */
    }

    return format;
}

static const char* parse_format__precision(const char* format, format_precision_t *precision_spec)
{
    char this_char = *format;
    memset(precision_spec, 0, sizeof(*precision_spec));

    if (this_char == '.')
    {
        ++format;
        this_char = *format;

        if (this_char == '*')
        {
            /* The width is not specified in the format string, but as an additional integer value argument preceding
             * the argument that has to be formatted. */
             precision_spec->as_extra_argument = true;
        }
        else if(is_number_character(this_char))
        {
            /* Minimum number of characters to be printed. If the value to be printed is shorter than this number,
             * the result is padded with blank spaces. The value is not truncated even if the result is larger. */
            const count_and_format_tuple_t count_and_format = parse_format__unsigned_int(format);
            format = count_and_format.format;
            precision_spec->number_of_digits = count_and_format.count;
        }
        else
        {
            precision_spec->number_of_digits = 0;
        }

        precision_spec->is_specified = true;
    }
    else 
    {
        /* There is no precision specifier present */
    }

    return format;
}


static const char* parse_format__length(const char* format, format_length_t *length_spec)
{
    switch (format[0])
    {
        case 'h':
            ++format;
            if (format[1] == 'h') { *length_spec = FORMAT_LENGHT_HH; ++format; }
            else                  { *length_spec = FORMAT_LENGHT_H;            }
            break;
        case 'l':
            ++format;
            if (format[1] == 'l') { *length_spec = FORMAT_LENGHT_LL; ++format; }
            else                  { *length_spec = FORMAT_LENGHT_L;            }
            break;
        case 'j':
            ++format;
            *length_spec = FORMAT_LENGHT_J;
            break;
        case 'z':
            ++format;
            *length_spec = FORMAT_LENGHT_Z;
            break;
        case 't':
            ++format;
            *length_spec = FORMAT_LENGHT_T;
            break;
        case 'L':
            ++format;
            *length_spec = FORMAT_LENGHT_L_DBL;
            break;
        default:
            *length_spec = FORMAT_LENGHT_NOT_SPECIFIED;
            break;
    }

    return format;
}



const char* parse_format__specifier(const char* format, format_specifier_t *const format_spec) {
    switch (*format)
    {
        case 'd':
        case 'i': *format_spec = FORMAT_SPECIFIER_SIGNED_DECIMAL_INTEGER;                 break;
        case 'u': *format_spec = FORMAT_SPECIFIER_UNSIGNED_DECIMAL_INTEGER;               break;
        case 'o': *format_spec = FORMAT_SPECIFIER_UNSIGNED_OCTAL;                         break;
        case 'x': *format_spec = FORMAT_SPECIFIER_UNSIGNED_HEXADECIMAL_LOWER_CASE;        break;
        case 'X': *format_spec = FORMAT_SPECIFIER_UNSIGNED_HEXADECIMAL_UPPER_CASE;        break;
        case 'f': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_DECIMAL;      break;
        case 'F': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_DECIMAL;      break;
        case 'e': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_SCIENTIFIC;   break;
        case 'E': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_SCIENTIFIC;   break;
        case 'g': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_SHORTEST;     break;
        case 'G': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_SHORTEST;     break;
        case 'a': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_LOWER_CASE_HEXADECIMAL;  break;
        case 'A': *format_spec = FORMAT_SPECIFIER_FLOATING_POINT_UPPER_CASE_HEXADECIMAL;  break;
        case 'c': *format_spec = FORMAT_SPECIFIER_CHARACTER;                              break;
        case 's': *format_spec = FORMAT_SPECIFIER_STRING ;                                break;
        case 'p': *format_spec = FORMAT_SPECIFIER_POINTER_ADDRESS;                        break;
        case 'n': *format_spec = FORMAT_SPECIFIER_NOTHING;                                break;
        default:  *format_spec = FORMAT_SPECIFIER_ERROR;                                  break;
    }
    return format + 1;
}

static void print_unsigned_integer_to_buffer(context_t *const context) {
    char buffer[50];
    unsigned long long num = 1234567;

    /* Awful algorithm would divide by 10^n, 10^(n-1) and so on, but want to assume that there is no divide
     * instruction. So could subtract 10^n, 10^(n-1) and so on to get counts.*/


}

static void print_string_arg_to_buffer(context_t *const context)
{
    /* Must be careful to request parameters in the correct order. Before the string itself there may be a width
     * and then a precision value specified as extra arguments, in that order, that occur, before the string argument */
    const size_t width_extra_argument =
        ((context->width_spec.is_specified) && (context->width_spec.as_extra_argument))
            ? va_arg(context->args, unsigned int)
            : 0;

    const size_t precision_extra_argument =
        ((context->precision_spec.is_specified) && (context->precision_spec.as_extra_argument))
            ? va_arg(context->args, unsigned int)
            : 0;

    /* Having gotten potential width & prevision arguments, can get the string argument */
    char character_as_string[2] = {'\0' ,'\0'};
    const char * string;
    if (context->format_spec == FORMAT_SPECIFIER_STRING) {
        string = va_arg(context->args, char *);
    }
    else {
        character_as_string[0] = (char)va_arg(context->args, int);
        string = character_as_string;
    }
    const size_t string_length = strlen(string);

    /* Now the padding, alignment and max length can be figured out.
     * - A width could be specified to set a minimum string width.
     * - A precision could be specified to set a maximum string width.
     * - Both could be specified
     *    - Must expect precision >= width for the specification to make sense. If it wasn't then what should be done?
     *      Makes sense to reduce the width to the precision. */

    /* Print no more than `max_characters` not including the NULL sentinel */
    const size_t max_characters = 
        (context->precision_spec.is_specified)
            ? context->precision_spec.as_extra_argument
                ? precision_extra_argument
                : context->precision_spec.number_of_digits
            : string_length; 

    /* Pad with spaces if string less than minimum_number_of_characters, on left or right depending on flags */
    const size_t min_characters_intermediate =
        (context->width_spec.is_specified)
            ? context->width_spec.as_extra_argument
                ? width_extra_argument
                : context->width_spec.minimum_number_of_characters
            : string_length;

    const size_t min_characters =
        (context->precision_spec.is_specified)
            ? (min_characters_intermediate < max_characters)
                ? min_characters_intermediate
                : max_characters
            : min_characters_intermediate;


    if (string_length < min_characters)
    {
        /* The string must be padded */
        size_t number_of_padding_spaces = min_characters - string_length;
        if (context->flags.left_justify)
        {
            bool space_left = write_string_to_print_buffer(&context->pbuff, string, string_length);
            for(size_t count = number_of_padding_spaces; count != 0 && space_left; count--)
            {
                space_left = write_character_to_print_buffer(&context->pbuff, ' ');
            }
        }
        else
        {
            bool space_left = true;
            for(size_t count = number_of_padding_spaces; count != 0 && space_left; count--)
            {
                space_left = write_character_to_print_buffer(&context->pbuff, ' ');
            }
            if (space_left)
            {
                write_string_to_print_buffer(&context->pbuff, string, string_length);
            }
        }
    }
    else
    {
        const size_t characters_to_write = string_length > max_characters ? max_characters : string_length;
        write_string_to_print_buffer(&context->pbuff, string, characters_to_write);
    }
}

/*
 * The Cortex-M0 has no divide instruction and does not even have a CLZ instruction. One for future but looking at
 * GCC divide code, might be able to optimize the CLZ part of the divide as the same divisor is going to be used
 * in multiple locations and is known - it will be either 8, 10, or 16! Also numerator changes predictably... in each
 * subsequent divide, the MSB bits are dealth with by the previous divide.
 * 
 * Meh... nice little idea but a awful lot of work for not much more gain I suspect... and then we have to do the
 * whole thing again for signed stuff so meh!
 */
struct qr {
	unsigned q;		/* computed quotient */
	unsigned r;		/* computed remainder */
};
// see https://github.com/OP-TEE/optee_os/blob/master/lib/libutils/isoc/arch/arm/arm32_aeabi_divmod.c
static void mydivision_qr(unsigned n, unsigned p, struct qr *qr)
{
	unsigned i = 1, q = 0;
    /* We *know* the denominator so don't need to CLZ or check for zero div! */
    /* Counts the leading zeros in the denominator */
    if ((p >> 4) == 0) {
        i <<= 28;
        p <<= 28;
    }
    else {
        i <<= 27;
        p <<= 27;
    }


    /* TODO!!!! At each stage we can do less searching than the previous stage as we know the previous 2 MSBs have been
     * dealth with in the last iteration, 3 if base 16!*/
	while (i > 0) {
		q = q << 1;	/* write bit in q at index (size-1) */
		if (n >= p)
		{
			n -= p;
			q++;
		}
		p = p >> 1; 	/* decrease p */
		i = i >> 1; 	/* decrease remaining size in q */
	}
	qr->r = n;
	qr->q = q;
}

void num_to_str(unsigned long num, unsigned long base)
{
    // max ulong value is 4294967296 on 32-bit device, so need 11 characters including NULL terminator
    struct qr qr;
    char buffer[11];
    memset(buffer, 0, sizeof(buffer));
    unsigned int i = 0;
    while(num > 0)
    {  
        mydivision_qr(num, base, &qr);
        buffer[i++] = '0' + qr.r;
        num = qr.q;
        
    }
    buffer[i] = '\0';
    printf("%s\n", buffer);
}

static void print_decimal_arg_to_buffer(context_t *const context) {
    
    switch(context->length_spec)
    {
        /* All of the following would have been type promoted to an unsigned int */
        case FORMAT_LENGHT_H:
        case FORMAT_LENGHT_HH:
        case FORMAT_LENGHT_NOT_SPECIFIED:
            va_arg(context->args, unsigned int);
            break;

        case FORMAT_LENGHT_L:
            va_arg(context->args, unsigned long int);
            break;
        
        case FORMAT_LENGHT_LL:
            va_arg(context->args, unsigned long long int);
            break;

        case FORMAT_LENGHT_J:
            va_arg(context->args, uintmax_t);
            break;

        case FORMAT_LENGHT_T:
            va_arg(context->args, ptrdiff_t);
            break;

        case FORMAT_LENGHT_Z:
            va_arg(context->args, size_t);
            break;
    
        //FORMAT_LENGHT_L_DBL,
    }
}

static void print_arg_to_buffer(context_t *const context)
{
    unsigned int minimum_number_of_characters = 0;
    unsigned int number_of_digits = 0;

    switch(context->format_spec)
    {
        case FORMAT_SPECIFIER_STRING:                   print_string_arg_to_buffer(context);  break;
        case FORMAT_SPECIFIER_CHARACTER:                print_string_arg_to_buffer(context);  break;
        case FORMAT_SPECIFIER_UNSIGNED_DECIMAL_INTEGER: print_decimal_arg_to_buffer(context); break;
        default: break;
    }        
}





void mysnprintf(char *const buffer, const size_t size, const char *const format, ...)
{
    context_t context = {
        .pbuff = { .format = format, .size_bytes = size, .consumed_bytes = 0, .buffer = buffer },
    };

    va_start(context.args, format);

    DEBUG(("\n\n------- TESTING %s\n\n", format));

    const char *next_char = context.pbuff.format;
    do
    {
        next_char = print_to_buffer_escaped_percents_until_next_specifier(next_char, &context.pbuff);    
        if (*next_char == '\0') { break; }
        
        next_char = parse_format__flags(next_char, &context.flags);
        if (*next_char == '\0') { break; }
        
        next_char = parse_format__width(next_char, &context.width_spec);
        if (*next_char == '\0') { break; }

        next_char = parse_format__precision(next_char, &context.precision_spec);
        if (*next_char == '\0') { break; }

        next_char = parse_format__length(next_char, &context.length_spec);
        if (*next_char == '\0') { break; }

        if (*next_char != '\0') {
            next_char = parse_format__specifier(next_char, &context.format_spec);
            print_arg_to_buffer(&context);
        }

    } while(*next_char != '\0');
    printf("%s\n", context.pbuff.buffer);
    
    va_end(context.args);
}

int main(void) {

    num_to_str(42946, 10);

    #define SIZE 40
    char buffer[SIZE];
    memset(buffer, (int)'#', sizeof(*buffer));

    const char *ex1 = "abc%de";
    const char *ex2 = "abc%%de";
    const char *ex3 = "abc%%%de";
    const char *ex4 = "abc%%de%fg";
    const char *ex5 = "abc%%%%%%%%de%%%%fg%82732u";

    const char *ex6_1 = "abc%+uJames";
    const char *ex6_2 = "abc%+*uJames";
    const char *ex6_3 = "abc%+82732uJames";

    const char *ex7_1 = "abc%+ 123.66uJames";
    const char *ex7_2 = "abc%-*uJames";
    const char *ex7_3 = "aa_%-*s_bbb";
// %[flags][width][.precision][length]specifier

    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%-15s_bbb", "JamesHume");

    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%-*s_bbb", 15, "JamesHume");

    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%*s_bbb", 15, "JamesHume");

    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%15s_bbb", "JamesHume");

    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%.3s_bbb", "JamesHume");
    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%.8s_bbb", "JamesHume");
    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%.9s_bbb", "JamesHume");
    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%10.10s_bbb", "JamesHume");
    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%10.9s_bbb", "JamesHume");

    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%c_bbb", '!');
    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%-10c_bbb", '!');
    memset(buffer, (int)'#', sizeof(*buffer));
    mysnprintf(buffer, SIZE, "aa_%10c_bbb", '!');

    return 0;
}