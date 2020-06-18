array=(4069 16384 65536 262144 1048576)

for i in ${array[@]}; do
	./read 100000 $i ./file.txt
done
