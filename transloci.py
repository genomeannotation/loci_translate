#!/usr/bin/env python

import sys

def main():
    #####################################
    # Parse args
    if len(sys.argv) < 6:
        print("Usage: transloci.py <agp_file> <loci_to_translate> <name_column> <start_column> <end_column>")
        exit(0)

    agp_file = open(sys.argv[1], 'r')
    loci_file = open(sys.argv[2], 'r')
    name_col = int(sys.argv[3])
    start_col = int(sys.argv[4])
    end_col = int(sys.argv[5])

    # Read in the agp file
    scaffolds = {}
    for line_num, line in enumerate(agp_file):
        fields = line[:-1].split('\t') # Skip \n and split by tabs
        if len(fields) != 9:
            continue
        try:
            new_name = fields[0]
            old_name = fields[5]
            new_start = int(fields[1])
            new_end = int(fields[2])
            old_start = int(fields[6])
            old_end = int(fields[7])
            orient = fields[8]
            scaffolds[old_name] = [new_name, old_start, old_end, new_start, new_end, orient]
        except:
            sys.stderr.write("Skipping invalid agp line "+str(line_num+1)+"\n")
            continue
    agp_file.close()
    
    # Process the file to update
    for line in loci_file:
        if line[0] == '#':
            sys.stdout.write(line)
            continue
        fields = line[:-1].split('\t') # Skip \n and split by tabs
        name = fields[name_col]
        start = int(fields[start_col])
        end = int(fields[end_col])

        new_name, old_start, old_end, new_start, new_end, orient = scaffolds[name]
        length = old_end - old_start

        if orient == '+' or orient == '?':
            trans_start = new_start + old_start - 1
            trans_end = trans_start + length
        elif orient == '-':
            trans_end = new_start + old_start - 1
            trans_start = trans_end + length
        else:
            sys.stderr.write("Invalid orientation for "+name+"; skipping\n")
            sys.stdout.write(line)
            continue

        fields[name_col] = new_name
        fields[start_col] = str(trans_start)
        fields[end_col] = str(trans_end)
        sys.stdout.write('\t'.join(fields)+'\n')
    loci_file.close()
    sys.stderr.write("Done!\n")

#############################################################

if __name__ == '__main__':
    main()
