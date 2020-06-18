#!/bin/bash

files=(native runc runsc-ptrace runsc-kvm kata)
MALLOCFREE_SIZE=(4096 16384 65536 262144 1048576)


for i in ${files[@]}; do
    echo "$i:"
    for size in ${MALLOCFREE_SIZE[@]}; do
        input="log/$i-$size.log"
        sed -i 's/\r$//g' $input
        count=$(wc -l < "$input")
        tmp=0.00
        while read line
        do
            tmp=$(echo "$tmp + $line" |  bc -l)
        done < "$input"
        tmp=$(echo "scale=2; $tmp/$count" |  bc -l)
        echo "$size: $tmp"
        echo ""
    done
done