#!/bin/bash


#### Create log dir ###
mkdir -p logs/experiments/execute/memory_performance/nofree/
mkdir -p logs/experiments/execute/memory_performance/free/


#### Constants ####

# TEST_EXECUTE_LIST=()

TEST_FILE="test.sh"

#### Execute ####

# # malloc and free
# MALLOCFREE_FOLDER_PATH="experiments/execute/memory_performance/free/"
# MALLOCFREE_APP_NAME="malloc_free"
# MALLOCFREE_TRIALS=1
# #100000
# MALLOCFREE_SIZE=(4096 16384 65536 262144 1048576)
# #(4096 16384 65536 262144 1048576)
# MALLOCFREE_TESTS=1
# #100

# # malloc without free
# MALLOCNOFREE_FOLDER_PATH="experiments/execute/memory_performance/nofree/"
# MALLOCNOFREE_APP_NAME="malloc_nofree"
# MALLOCNOFREE_TRIALS=1
# #100000
# MALLOCNOFREE_SIZE=(4096 16384 65536 262144 1048576)
# #(4096 16384 65536 262144 1048576)
# MALLOCNOFREE_TESTS=1

# malloc and free
MALLOCFREE_FOLDER_PATH="experiments/execute/memory_performance/free/"
MALLOCFREE_APP_NAME="malloc_free"
MALLOCFREE_TRIALS=100000
MALLOCFREE_SIZE=(4096 16384 65536 262144 1048576)
MALLOCFREE_TESTS=100

# malloc without free
MALLOCNOFREE_FOLDER_PATH="experiments/execute/memory_performance/nofree/"
MALLOCNOFREE_APP_NAME="malloc_nofree"
MALLOCNOFREE_TRIALS=100000
MALLOCNOFREE_SIZE=(4096 16384 65536 262144 1048576)
MALLOCNOFREE_TESTS=100

	# Malloc
generate_cmds() {
  RUNTIME=$1
	# Mallocfree
	for i in ${MALLOCFREE_SIZE[@]}
	do
		for (( j=1; j <= $MALLOCFREE_TESTS; ++j ))
		do
			TEST_EXECUTE_LIST+=("$MALLOCFREE_FOLDER_PATH$TEST_FILE $MALLOCFREE_FOLDER_PATH $MALLOCFREE_APP_NAME $RUNTIME $MALLOCFREE_TRIALS $i")
		done
	done
  # Mallocnofree
	for i in ${MALLOCNOFREE_SIZE[@]}
	do
		for (( j=1; j <= $MALLOCNOFREE_TESTS; ++j ))
		do
			TEST_EXECUTE_LIST+=("$MALLOCNOFREE_FOLDER_PATH$TEST_FILE $MALLOCNOFREE_FOLDER_PATH $MALLOCNOFREE_APP_NAME $RUNTIME $MALLOCNOFREE_TRIALS $i")
		done
	done
}
