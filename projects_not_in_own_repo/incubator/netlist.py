import re

with open("../../src/images/jeh-tech/electronics_common_emitter_amplifier.net") as fh:
    lines = [x.strip() for x in fh.readlines()]


# Skip the file Header: The File Header includes 8 entries, each written as a single line of text
lines = lines[8:]

# Skip any blank lines
line_index = 0
while lines[line_index] == "":
    line_index += 1

# Part IDs Table: The Part IDs Table is a list of Part IDs and their values.
# The table begins with the line of text "Part IDs Table", followed by one line for each entry in the table. 
# Each entry includes these three fields:
#   • Part ID: String 
#   • Part Name: String 
#   • Package Name: String - Current not used and should be: ""
assert lines[line_index] == '"Part IDs Table"'
line_index += 1

part_id_table = []
while lines[line_index] != "":
    part_id, part_name, _ = re.match(r'"(.*)"\s*"(.*)"\s*"(.*)"', lines[line_index]).groups()
    part_id_table.append((part_id, part_name))
    line_index += 1
    
# Skip any blank lines
while lines[line_index] == "":
    line_index += 1

# Net Names Table: The Net Names Table is a list of all of the net names. Each net name is listed just once.
# The table begins with the line of text "Net Names Table", followed by one line for each entry in the table. 
# Each entry includes these two fields:
#     • Net Name: String
#     • First Net Connection: Integer - Index into the Net Connections Table of this net's first
#                             connection. A value of 1 indexes to the first entry in the Net Connections Table.
assert lines[line_index] == '"Net Names Table"'
line_index += 1

netnames_table = []
while lines[line_index] != "":
    net_name, net_connections_index = re.match(r'"(.*)"\s*(\d+)', lines[line_index]).groups()
    netnames_table.append((net_name, int(net_connections_index) - 1)) # File is 1-indexed but Python is 0-indexed, hence -1
    line_index += 1

# Skip any blank lines
while lines[line_index] == "":
    line_index += 1

# Net Connections Table: The Net Connections Table is a linked list of connections. Each entry in the table
# establishes a connection between a named net, and one pin of a component. The table begins with the line of 
# text "Net Connections Table", followed by one line for each entry in the table. Each entry includes these 
# four fields:
#    • Net Name Table Index: Integer - Index into the Net Names Table for the name of this net. A value of 1 
#                            indexes to the first entry in the Net Names Table.
#    • Part ID Table Index:  Integer - Index into the Part ID Table for the part that this connection is made
#                            to. A value of 1 indexes to the first entry in the Part IDs Table .
#    • Pin Number: Integer - The pin number on the part that this connection is made to. Note, the pin number
#                            field must be a integer greater than 0, letters are not allowed.
#    • Next Connection: Integer - Index into the Net Connections Table of the next connection that is part of
#                                 this net. A value of 0 indicates this entry is the last connection. A value
#                                 of 1 indexes to the first entry in the Net Connections Table.
assert lines[line_index] == '"Net Connections Table"'
line_index += 1

net_connections_table = []
while lines[line_index] != "":
    tbl_net_name_index, tbl_part_id_index, tbl_pin_num, tbl_next_connection = (int(x) for x in re.match(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', lines[line_index]).groups())
    print(netnames_table[tbl_net_name_index - 1], "-", part_id_table[tbl_part_id_index - 1], "-", tbl_pin_num, "-", tbl_next_connection)
    line_index += 1
                                                                               
