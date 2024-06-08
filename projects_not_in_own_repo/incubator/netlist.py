"""
Copyright 2024 James E Hume

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Part:
    part_id   : int
    part_name : str

    def __hash__(self):
        return hash(self.part_id)


@dataclass(frozen=True)
class Net:
    name : str
    head : "NetComponent"


@dataclass(frozen=True)
class NetComponent:
    part : Part
    pin  : int
    next : Optionl[Net]


def parse_netlist(filename) -> dict[str, Net]:
    with open(filename) as fh:
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

    part_table : list[Part] = []
    while lines[line_index] != "":
        part_id, part_name, _ = re.match(r'"(.*)"\s*"(.*)"\s*"(.*)"', lines[line_index]).groups()
        part_table.append(Part(part_id, part_name))
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

    netnames_table_raw = []
    while lines[line_index] != "":
        net_name, net_connections_index = re.match(r'"(.*)"\s*(\d+)', lines[line_index]).groups()
        netnames_table_raw.append((net_name, int(net_connections_index) - 1)) # File is 1-indexed but Python is 0-indexed, hence -1
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
    #                            to. A value of 1 indexes to the first entry in the Part IDs Table.
    #                             BUT this is converted to a Python index, so it starts at 0.
    #    • Pin Number: Integer - The pin number on the part that this connection is made to. Note, the pin number
    #                            field must be a integer greater than 0, letters are not allowed.
    #    • Next Connection: Integer - Index into the Net Connections Table of the next connection that is part of
    #                                 this net. A value of 0 indicates this entry is the last connection. A value
    #                                 of 1 indexes to the first entry in the Net Connections Table.
    #                                 BUT this is converted to a Python infex, so -1 indicates the last connection
    #                                 and 0 is the first.
    assert lines[line_index] == '"Net Connections Table"'
    line_index += 1

    net_connections_table_raw = []
    while lines[line_index] != "":
        tbl_net_name_index, tbl_part_id_index, tbl_pin_num, tbl_next_connection = (
            int(x) for x in re.match(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', lines[line_index]).groups())
        net_connections_table_raw.append((tbl_net_name_index, tbl_part_id_index - 1, tbl_pin_num, tbl_next_connection - 1))
        line_index += 1


    def process_net_componenet(net_connection_idx) -> NetComponent:
        tbl_net_name_index, tbl_part_id_index, tbl_pin_num, tbl_next_connection = net_connections_table_raw[net_connection_idx]
        if tbl_next_connection == -1:
            # Then this is the last connection
            return NetComponent(part=part_table[tbl_part_id_index], pin=tbl_pin_num, next=None)
    
        # Else continue to the next component so that the `next` member can be filled in, until the last component in the
        # net is found (as tested for in the above `if`).
        next_component = process_net_componenet(tbl_next_connection)
        return NetComponent(part=part_table[tbl_part_id_index], pin=tbl_pin_num, next=next_component)


    # Go through the net names table, which provides the index of the first componenet in the net.
    nets = {}
    for net_name, net_connection_idx in netnames_table_raw:
        nets[net_name] = Net(name=net_name, head=process_net_componenet(net_connection_idx))
        
    return nets



if __name__ == "__main__":
    nets = parse_netlist("../../src/images/jeh-tech/electronics_common_emitter_amplifier.net")

    import pprint
    pprint.pp(nets)

