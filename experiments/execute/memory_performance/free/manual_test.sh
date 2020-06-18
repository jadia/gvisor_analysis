#!/bin/bash

MALLOCFREE_SIZE=(4096 16384 65536 262144 1048576)
rip log
mkdir -p log
trails=$1

while [[ $trails -gt 0 ]];
do
    echo "Trail: $trails"
    echo "native"
    # exit
    for i in ${MALLOCFREE_SIZE[@]}; do
        ./myapp 100000 $i >> log/native-$i.log
    done

    echo "runc"
    for i in ${MALLOCFREE_SIZE[@]}; do
        docker run -ti --rm -v $(pwd):/malloc malloc-free 100000 $i >> log/runc-$i.log
    done

    echo "runsc-ptrace"
    for i in ${MALLOCFREE_SIZE[@]}; do
        docker run -ti --rm --runtime=runsc --platform=ptrace -v $(pwd):/malloc malloc-free 100000 $i >> log/runsc-ptrace-$i.log
    done

    echo "runsc-kvm"
    for i in ${MALLOCFREE_SIZE[@]}; do
        docker run -ti --rm --runtime=runsc --platform=kvm -v $(pwd):/malloc malloc-free 100000 $i >> log/runsc-kvm-$i.log
    done


    echo "kata"
    for i in ${MALLOCFREE_SIZE[@]}; do
        docker run -ti --rm --runtime=kata -v $(pwd):/malloc malloc-free 100000 $i >> log/kata-$i.log
    done
    trails=$(($trails-1))
done

echo "Saving result to result.txt file"
./calculate_avg.sh > result.txt

ntfy send "Memory task done"