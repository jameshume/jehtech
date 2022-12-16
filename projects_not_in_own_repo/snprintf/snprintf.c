#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stddef.h>

#define DEBUG(x) printf x

typedef struct print_buffer_tag
{
    const char *format;
    size_t size_bytes;
    size_t consumed_bytes;
    char *buffer;
} print_buffer_t;


void write_character_to_print_buffer(print_buffer_t *const print_buffer, char character)
{
    if (print_buffer->consumed_bytes < print_buffer->size_bytes - 1) /* Make sure trailing '\0' is left */
    {
        print_buffer->buffer[print_buffer->consumed_bytes] = character;
        print_buffer->consumed_bytes += 1;
        print_buffer->buffer[print_buffer->consumed_bytes] = '\0'; /* Always terminate to be safe - could be overwritten if more is added. */
    }
}

void write_string_to_print_buffer(print_buffer_t *const print_buffer, const char *const string, const size_t num_characters)
{
    if (print_buffer->consumed_bytes < print_buffer->size_bytes)
    {
        const size_t space_remaining = print_buffer->size_bytes - 1 - print_buffer->consumed_bytes; /* -1 to leave space for trailing '\0' */
        if (space_remaining > 0)
        {
            const size_t bytes_to_write = num_characters > space_remaining ? space_remaining : num_characters;
            memcpy(&print_buffer->buffer[print_buffer->consumed_bytes], string, bytes_to_write);
            print_buffer->consumed_bytes += bytes_to_write;
        }
        print_buffer->buffer[print_buffer->consumed_bytes] = '\0'; /* Always terminate to be safe - could be overwritten if more is added. */
    }
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

typedef struct count_and_format_tuple_tag
{
    size_t count;
    const char *format;
} count_and_format_tuple_t;

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

static const char* find_next_specifier(const char *_format, print_buffer_t *const print_buffer)
{
    const char *previous_format;
    count_and_format_tuple_t rval = { .format = _format, .count = 0 };
    
    do 
    {
        previous_format = rval.format;
        rval.format = chew_not_percent_chars(rval.format);
        write_string_to_print_buffer(print_buffer, previous_format, rval.format - previous_format);
        /* At this point `rval.format` points to a null character or the first '%' character found. */

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


typedef struct format_flags_tag
{
    bool left_justify;
    bool force_sign;
    bool no_sign;
    bool force_decimal_point_or_0x_prefix;
    bool left_pad_with_zeros;
} format_flags_t;

static void dump_format_flags(const format_flags_t *const flags)
{
    DEBUG(("Flags:\n"));
    DEBUG(("   left_justify: %u\n", (unsigned int)flags->left_justify));
    DEBUG(("   force_sign: %u\n", (unsigned int)flags->force_sign));
    DEBUG(("   no_sign: %u\n", (unsigned int)flags->no_sign));
    DEBUG(("   force_decimal_point_or_0x_prefix: %u\n", (unsigned int)flags->force_decimal_point_or_0x_prefix));
    DEBUG(("   left_pad_with_zeros: %u\n", (unsigned int)flags->left_pad_with_zeros));
}

static const char* parse_format__flags(const char* format, format_flags_t *const flags)
{
    bool no_flag_char_seen = false;
    memset(flags, 0, sizeof(*flags));

    while ((*format != '\0') && (!no_flag_char_seen))
    {
        DEBUG(("Flags looking at '%c'\n", *format));
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

typedef struct format_width_tag
{
    size_t minimum_number_of_characters;
    bool is_specified;
    bool as_extra_argument;
} format_width_t;

static const char* parse_format__width(const char* format, format_width_t *width_spec)
{
    char this_char = *format;
    memset(width_spec, 0, sizeof(*width_spec));

    if (this_char == '*')
    {
        /* The width is not specified in the format string, but as an additional integer value argument preceding
         * the argument that has to be formatted. */
        DEBUG(("Width wildcard found\n"));
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
        DEBUG(("Width of %zu found\n", width_spec->minimum_number_of_characters));
    }
    else 
    {
        /* There is no width specifier present */
        DEBUG(("No width specifier found\n"));
    }

    return format;
}

static void dump_format_width(const format_width_t *const width_spec)
{
    DEBUG(("Width Spec:\n"));
    DEBUG(("   minimum_number_of_characters: %zu\n", width_spec->minimum_number_of_characters));
    DEBUG(("   is_specified: %u\n", (unsigned int)width_spec->is_specified));
    DEBUG(("   as_extra_argument: %u\n", (unsigned int)width_spec->as_extra_argument));
}

typedef struct format_precision_tag
{
    size_t number_of_digits;
    bool is_specified;
    bool as_extra_argument;
    bool error;
} format_precision_t;

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
             precision_spec->is_specified = true;
             precision_spec->as_extra_argument = true;
        }
        else if(is_number_character(this_char))
        {
            /* Minimum number of characters to be printed. If the value to be printed is shorter than this number,
             * the result is padded with blank spaces. The value is not truncated even if the result is larger. */
            const count_and_format_tuple_t count_and_format = parse_format__unsigned_int(format);
            format = count_and_format.format;
            precision_spec->is_specified = true;
            precision_spec->number_of_digits = count_and_format.count;
        }
        else
        {
            precision_spec->error = true;
        }
    }
    else 
    {
        /* There is no precision specifier present */
    }

    return format;
}

static void dump_format_precision(const format_precision_t *const prec_spec)
{
    DEBUG(("number_of_digits: %u", prec_spec->number_of_digits));
    DEBUG(("is_specified: %u", prec_spec->is_specified));
    DEBUG(("as_extra_argument: %u", prec_spec->as_extra_argument));
    DEBUG(("error: %u", prec_spec->error));

}

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
}


typedef enum format_specifier_tag
{
    FORMAT_SPECIFIER_CHARACTER,
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
    FORMAT_SPECIFIER_UNSIGNED_HEX_LOWER_CASE,
    FORMAT_SPECIFIER_UNSIGNED_HEX_UPPER_CASE,
    FORMAT_SPECIFIER_UNSIGNED_OCTAL,
} format_specifier_t;

const char* parse_format__specifier(const char* format) {
    switch (*format)
    {
        case 'd':
        case 'i':
            break;

        case 'u':
            break;
        
        case 'o':
            break;
        
        case 'x':
            break;
        
        case 'X':
            break;
        
        case 'f':
            break;
        
        case 'F':
            break;
        
        case 'e':
            break;
        
        case 'E':
            break;
        
        case 'g':
            break;
        
        case 'G':
            break;
        
        case 'a':
            break;
        
        case 'A':
            break;

        case 'c':
            break;

        case 's':
            break;

        case 'p':
            break;

        case 'n':
            break;

        default:
            // Error
            break;
    }
}

const char* parse_format(const char* format) {
    // %[flags][width][.precision][length]specifier
    

}




void mysnprintf(const char *const format, size_t size, char *buffer)
{
    print_buffer_t pbuff = { .format = format, .size_bytes = size, .consumed_bytes = 0, .buffer = buffer };

    printf("\n\n------- TESTING %s\n\n", format);

    const char *next_char = find_next_specifier(pbuff.format, &pbuff);    
    if (*next_char != '0') {
        format_flags_t flags;
        next_char = parse_format__flags(next_char, &flags);
        dump_format_flags(&flags);
    }

    if (*next_char != '0') {
        format_width_t width_spec;
        next_char = parse_format__width(next_char, &width_spec);
        dump_format_width(&width_spec);
    }

    if (*next_char != '0') {
        format_precision_t precision_spec;
        next_char = parse_format__precision(next_char, &precision_spec);
    }

    if (*next_char != '0') {
        format_length_t length_spec;
        next_char = parse_format__length(next_char, &length_spec);
    }

    printf("%s\n", pbuff.buffer);

}

int main(void) {
    #define SIZE 6
    char buffer[SIZE];

    const char *ex1 = "abc%de";
    const char *ex2 = "abc%%de";
    const char *ex3 = "abc%%%de";
    const char *ex4 = "abc%%de%fg";
    const char *ex5 = "abc%%%%%%%%de%%%%fg%82732u";

    const char *ex6_1 = "abc%+uJames";
    const char *ex6_2 = "abc%+*uJames";
    const char *ex6_3 = "abc%+82732uJames";

    const char *ex7_1 = "abc%+ *uJames";
    const char *ex7_2 = "abc%-*uJames";
    const char *ex7_3 = "abc% 82732uJames";


    mysnprintf(ex7_1, SIZE, buffer);
    //mysnprintf(ex7_2, SIZE, buffer);
    //mysnprintf(ex7_3, SIZE, buffer);

    return 0;
}