#!/bin/bash

work_dir="."
pdb_dir="$work_dir/pdb"
align_dir="$work_dir/align"

# Create the output directory (if it does not exist)
mkdir -p "$align_dir"

# Iterate through the .pdb file and perform the 1-vs-1 alignment
for pdb1 in "$pdb_dir"/*.pdb; do
    for pdb2 in "$pdb_dir"/*.pdb; do
        # avoid self-alignment (a-vs-a)
        if [ "$pdb1" != "$pdb2" ]; then
            file1=$(basename -s .pdb "$pdb1")
            file2=$(basename -s .pdb "$pdb2")

            # avoid duplicate alignment (a-vs-b & b-vs-a)
            if [ "$file1" \< "$file2" ]; then
                # perform the alignment
                tmalign_output="$align_dir/${file1}_${file2}.align.txt"
                TMalign "$pdb1" "$pdb2" > "$tmalign_output"

                echo "TMalign comparison between $file1 and $file2 saved to $tmalign_output"
            fi
        fi
    done
done
