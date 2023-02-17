#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>

#include "dwarf.h"
#include "libdwarf.h"

#define READ_FROM_DEBUG_INFO_SECTION  true


static int get_next_cu_die(Dwarf_Debug dbg, Dwarf_Die *const cu_die)
{
    Dwarf_Unsigned cu_header_length;
    Dwarf_Half     version_stamp;
    Dwarf_Unsigned abbrev_offset;
    Dwarf_Half     address_size;
    Dwarf_Half     offset_size;
    Dwarf_Half     extension_size;
    Dwarf_Sig8     signature;
    Dwarf_Unsigned typeoffset;
    Dwarf_Unsigned next_cu_offset;
    Dwarf_Half     header_cu_type;
    Dwarf_Error error;
    int res = 0;

    /* Get the next compilation unit HEADER. The source indicates that the parameters are checked
     * for NULL before assigning but if they are NULL I get a segfault, so passing all in and
     * using none, except for the error! */
    res = dwarf_next_cu_header_d(
        dbg,
        READ_FROM_DEBUG_INFO_SECTION, /*< Don't care about DWARF 4 - assume DWARF 5 */
        &cu_header_length,
        &version_stamp,
        &abbrev_offset,
        &address_size,
        &offset_size,
        &extension_size,
        &signature,
        &typeoffset,
        &next_cu_offset,
        &header_cu_type,
        &error
    );

    if (res != DW_DLV_OK) {
        /* Either failed or there are no more CUs to read. Caller must handle. */
        if (res == DW_DLV_ERROR) {
            fprintf(stderr, "Error: Failed to read a CU header because '%s'\n", dwarf_errmsg(error));
        }
        return res;
    }

    /* The CU will have a single sibling, a cu_die. */
    res = dwarf_siblingof_b(
        dbg,
        NULL,    /* Immediately after calling dwarf_next_cu_header_d pass in NULL to retrieve the CU DIE */
        true,    /* Only considering .debug_info sections */
        cu_die,  /* Returns the DIE */
        &error   /* Returns error info, if any */
    );

    if (res == DW_DLV_ERROR) {
        fprintf(stderr, "Error: Failed to read a CU header because '%s'\n", dwarf_errmsg(error));
        return DW_DLV_ERROR;
    }
    else if (res == DW_DLV_NO_ENTRY) {
        /* It should not be possible that a CU header exists without a CU DIE */
        fprintf(stderr, "Error: CU header found without associated DIE\n");
        return DW_DLV_ERROR;
    }

    /*  Found what we looked for */
    return DW_DLV_OK;
}

static int search_enumerations(Dwarf_Debug dbg, Dwarf_Die cu_die)
{
    Dwarf_Error error;
    int rc = DW_DLV_OK;
    Dwarf_Die current_die = cu_die;

    while (rc == DW_DLV_OK)
    {
        Dwarf_Half tag = 0;
        rc = dwarf_tag(current_die, &tag, &error);
        if (rc == DW_DLV_OK)
        {
            printf("TAG IS %u\n", (unsigned int)tag);
            if (tag == DW_TAG_enumeration_type)
            {
                char *die_name = NULL;
                rc = dwarf_diename(current_die, &die_name, &error);
                if (rc == DW_DLV_OK)
                {
                    printf("\tENUMERATION TYPE IS %s\n", die_name);
                    dwarf_dealloc(dbg, die_name, DW_DLA_STRING);
                }
                else
                {
                    fprintf(stderr, "Error: Could not read TAG name because '%s'\n",  dwarf_errmsg(error));        
                }  
            }
            else
            {
                char *die_name = NULL;
                rc = dwarf_diename(current_die, &die_name, &error);
                if (rc == DW_DLV_OK)
                {
                    printf("\tPOO TYPE IS %s\n", die_name);
                    dwarf_dealloc(dbg, die_name, DW_DLA_STRING);
                }
                else
                {
                    fprintf(stderr, "Error: Could not read TAG name because '%s'\n",  dwarf_errmsg(error));        
                }  
            }
        }
        else
        {
            fprintf(stderr, "Error: Could not TAG because '%s'\n",  dwarf_errmsg(error));
        }

        if (rc == DW_DLV_OK) {
            Dwarf_Die sibling_die = NULL;
            rc = dwarf_siblingof_b(dbg, current_die, READ_FROM_DEBUG_INFO_SECTION, &sibling_die, &error);
            if (rc == DW_DLV_OK) {
                current_die = sibling_die;
            }
            else if (rc == DW_DLV_ERROR) {
                fprintf(stderr, "Error: Could not get sibling because '%s'\n",  dwarf_errmsg(error));
            }
        }
    }
}

static int print_enumerations_for_cu(Dwarf_Debug dbg, Dwarf_Die cu_die)
{
    int rc;
    Dwarf_Die child_die = 0;
    Dwarf_Error error;

    /* Get the first child and all of its siblings to view the first level of the tree */
    rc = dwarf_child(cu_die, &child_die, &error);
    if(rc == DW_DLV_ERROR) {
        fprintf(stderr, "Error: Could not get child because '%s'\n",  dwarf_errmsg(error));
    }
    else if (rc == DW_DLV_OK) {
        rc = search_enumerations(dbg, child_die);
    }

    return rc;
}

static int print_enumerations(Dwarf_Debug dbg)
{
    int rc = DW_DLV_OK;
    Dwarf_Error error;
    Dwarf_Die cu_die;
    Dwarf_Die child_die = 0;

    while(rc == DW_DLV_OK) {
        /* For each compilation unit... */
        rc = get_next_cu_die(dbg, &cu_die);
        if (rc == DW_DLV_OK) {
            rc = print_enumerations_for_cu(dbg, cu_die);
            if (rc != DW_DLV_OK) {
                printf("BUGGER\n");
            }
        }
    }

    return rc;    
}

int main(int argc, char *argv[])
{
    int res;
    int fd;
    Dwarf_Debug dbg;
    Dwarf_Error error;

    if (argc != 2) {
        fprintf(stderr, "Error: Wrong number of arguments. Saw %d, expected 1", argc - 1);
        return EXIT_FAILURE;
    }

    const char *const filename = argv[1];

    if ((fd = open(filename, O_RDONLY)) < 0) {
        fprintf(stderr, "Error: Failed to open '%s'", filename);
        return EXIT_FAILURE;
    }

    res = dwarf_init(fd, DW_DLC_READ, NULL, 0, &dbg, &error);
    if(res == DW_DLV_OK) {
        res = print_enumerations(dbg);

        res = dwarf_finish(dbg, &error);
        if(res != DW_DLV_OK) {
            fprintf(stderr, "Error: Failed to de-initialise DWARF: %s\n", dwarf_errmsg(error));
        }   
    }
    else {
        fprintf(stderr, "Error: Failed to initialise DWARF: %s", dwarf_errmsg(error));
    }

    close(fd);

    return res == DW_DLV_OK ? EXIT_SUCCESS : EXIT_FAILURE;
}