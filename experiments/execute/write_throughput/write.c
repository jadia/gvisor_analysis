#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>

int NUM_TRIALS;
int WRITE_SIZE;
char* FILE_PATH;
int INMEM_FLAG = 346;

// Gets the current time
struct timespec diff(struct timespec start, struct timespec end)
{
        struct timespec temp;
        if ((end.tv_nsec - start.tv_nsec) < 0)
        {
                temp.tv_sec = end.tv_sec - start.tv_sec - 1;
                temp.tv_nsec = 1000000000 + end.tv_nsec - start.tv_nsec;
        }
        else
        {
                temp.tv_sec = end.tv_sec - start.tv_sec;
                temp.tv_nsec = end.tv_nsec - start.tv_nsec;
        }
        return temp;
}


float execute(char *file) {
        int fd;

        // Open the specific file
        fd = open(file, O_WRONLY|O_CREAT);
        if (fd == 0) {
                perror ("ERROR: open");
                return 1;
        }

	char *data = calloc(WRITE_SIZE, sizeof(char));
        int r = 0;
        int total_written = 0;

        // Start timer
        struct timespec ts0;
        clock_gettime(CLOCK_REALTIME, &ts0);

	for (int i = 0; i < NUM_TRIALS; i++) {
		if ((i % 1000) == 1) {
			lseek(fd, 0, SEEK_SET);
		}
		// Reads total read size
		if ( (r = write(fd, data, WRITE_SIZE)) == WRITE_SIZE) {
			total_written = total_written + r;
		} else {
			printf("ERROR: Was not able to write WRITE_SIZE. Trial: %d\n", i);
			exit(1);
		}
	}
 
	// End timer
        struct timespec ts1;
        clock_gettime(CLOCK_REALTIME, &ts1);
        struct timespec t = diff(ts0,ts1);

        //close(fd);

	// Remove the file
	//remove(file);

        float elapsed_time = t.tv_sec + t.tv_nsec/(float)1000000000;

        return elapsed_time;
}

int main(int argc, char *argv[]) {
        // Parse command line args
        if (argc != 4) {
                printf("ERROR: Usage: ./write <number of trials> <size of file read in Bytes> <path to rile to read>\n");
                return 0;
        }


        NUM_TRIALS = atoi(argv[1]);
        WRITE_SIZE = atoi(argv[2]);
	FILE_PATH = argv[3];

        float total = 0;

        total = execute(FILE_PATH);

        printf("LOG_OUTPUT: Average for %d trials and WRITE_SIZE = %d: Write time average = %.12f seconds\n", NUM_TRIALS, WRITE_SIZE, total/NUM_TRIALS);

        return 0;
}

