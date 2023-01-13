// Verbatim from https://github.com/eliben/code-for-blog/blob/master/2011/dwarf_get_func_addr.c
// Compile using gcc -I /usr/include/libdwarf dwarf_test_reader.c -ldwarf -o dwarf_reader
// Then added some debug

/* Code sample: Using libdwarf for getting the address of a function
** from DWARF in an ELF executable.
** Not much error-handling or resource-freeing is done here...
**
** Eli Bendersky (http://eli.thegreenplace.net)
** This code is in the public domain.
*/
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <dwarf.h>
#include <libdwarf.h>


void die(char* fmt, ...)
{
    va_list args;
    
    va_start(args, fmt);
    vfprintf(stderr, fmt, args);
    va_end(args);
    
    exit(EXIT_FAILURE);
}


/* List a function if it's in the given DIE.
*/

//Taken verbatim from libdwarf example `data` in docs.
/*  If there is no 'error' passed into a dwarf function
    and there is an error, and an error-handler like this
    is passed.  This example simply returns so we
    test how well that action works.  */
static void
simple_error_handler(Dwarf_Error error, Dwarf_Ptr errarg)
{
    Dwarf_Unsigned unused =  (Dwarf_Unsigned)errarg;
    printf("\nlibdwarf error detected: 0x%" DW_PR_DUx " %s\n", 
        dwarf_errno(error),dwarf_errmsg(error));
    return;
}

void list_func_in_die(Dwarf_Debug dgb, Dwarf_Die the_die)
{
    char* die_name = 0;
    const char* tag_name = 0;
    Dwarf_Error err;
    Dwarf_Half tag;
    Dwarf_Attribute* attrs;
    Dwarf_Addr lowpc, highpc;
    Dwarf_Unsigned attrcount;
    Dwarf_Signed i;
    int rc = dwarf_diename(the_die, &die_name, &err);

    if (rc == DW_DLV_ERROR)
        die("Error in dwarf_diename\n");
    else if (rc == DW_DLV_NO_ENTRY)
        return;

    if (dwarf_tag(the_die, &tag, &err) != DW_DLV_OK)
        die("Error in dwarf_tag\n");

    /* Only interested in subprogram DIEs here */
    if (tag != DW_TAG_subprogram)
        return;

    if (dwarf_get_TAG_name(tag, &tag_name) != DW_DLV_OK)
        die("Error in dwarf_get_TAG_name\n");

    printf("DW_TAG_subprogram: '%s' : '%s'\n", die_name, tag_name);

    Dwarf_Unsigned uval;

    /* Grab the DIEs attributes for display */
    if (dwarf_attrlist(the_die, &attrs, &attrcount, &err) != DW_DLV_OK)
        die("Error in dwarf_attlist\n");
    for (i = 0; i < attrcount; ++i) {
        Dwarf_Half attrcode;
        if (dwarf_whatattr(attrs[i], &attrcode, &err) != DW_DLV_OK)
            die("Error in dwarf_whatattr\n");

        /* We only take some of the attributes for display here.
        ** More can be picked with appropriate tag constants.
        */
        lowpc = 0xdeadbeef;
        highpc = 0xdeadbeef;
        if (attrcode == DW_AT_low_pc)
            dwarf_formaddr(attrs[i], &lowpc, 0);
        else if (attrcode == DW_AT_high_pc)
            dwarf_formaddr(attrs[i], &highpc, 0);
        else if(attrcode == DW_AT_decl_line) {
            
              dwarf_formudata(attrs[i],&uval, 0);
        }
    }

    printf("low pc  : 0x%08llx\n", lowpc);
    printf("high pc : 0x%08llx\n", highpc);
    printf("line: %u\n", (unsigned int)uval);
}


/* List all the functions from the file represented by the given descriptor.
*/
void list_funcs_in_file(Dwarf_Debug dbg)
{
    Dwarf_Unsigned cu_header_length, abbrev_offset, next_cu_header;
    Dwarf_Half version_stamp, address_size;
    Dwarf_Error err;
    Dwarf_Die no_die = 0, cu_die, child_die;
    int rval;

    /* Find compilation unit header */
    rval = dwarf_next_cu_header(
        dbg,
        &cu_header_length,
        &version_stamp,
        &abbrev_offset,
        &address_size,
        &next_cu_header,
        &err
    );
    if (rval == DW_DLV_NO_ENTRY)
        die("No CU header found\n");
    else if (rval != DW_DLV_OK)
        die("Error reading DWARF cu header: %s\n", dwarf_errmsg(err));

    /* Expect the CU to have a single sibling - a DIE */
    if (dwarf_siblingof(dbg, no_die, &cu_die, &err) == DW_DLV_ERROR)
        die("Error getting sibling of CU: %s\n", dwarf_errmsg(err));

    /* Expect the CU DIE to have children */
    if (dwarf_child(cu_die, &child_die, &err) == DW_DLV_ERROR)
        die("Error getting child of CU DIE\n");

    /* Now go over all children DIEs */
    while (1) {
        int rc;
        list_func_in_die(dbg, child_die);
        rc = dwarf_siblingof(dbg, child_die, &child_die, &err);

        if (rc == DW_DLV_ERROR)
            die("Error getting sibling of DIE\n");
        else if (rc == DW_DLV_NO_ENTRY)
            break; /* done */
    }
}


int main(int argc, char** argv)
{
    Dwarf_Debug dbg = 0;
    Dwarf_Error err;
    const char* progname;
    int fd = -1;

    if (argc < 2) {
        fprintf(stderr, "Expected a program name as argument\n");
        return 1;
    }

    progname = argv[1];
    if ((fd = open(progname, O_RDONLY)) < 0) {
        perror("open");
        return 1;
    }
    
    if (dwarf_init(fd, DW_DLC_READ, simple_error_handler, 0, &dbg, &err) != DW_DLV_OK) {
        fprintf(stderr, "Failed DWARF initialization\n");
        return 1;
    }

    list_funcs_in_file(dbg);

    if (dwarf_finish(dbg, &err) != DW_DLV_OK) {
        fprintf(stderr, "Failed DWARF finalization\n");
        return 1;
    }

    close(fd);
    return 0;
}