#include "work.h"

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/mman.h>

#define PAGE_SIZE (2 * 1024 * 1024) // 2MB pages

void setup_large_pages() {
    FILE *file = fopen("largepages.txt", "r");
    if (!file) {
        fprintf(stderr, "Failed to open largepages.txt: %s\n", strerror(errno));
        return;
    }

    // Read addresses from the file
    unsigned long address;
    while (fscanf(file, "%lu", &address) == 1) {
        // Use mmap to allocate memory at the specified address
        void *ptr = mmap((void *)address, PAGE_SIZE, PROT_READ | PROT_WRITE,
                         MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED | MAP_HUGETLB, -1, 0);

        if (ptr == MAP_FAILED) {
            fprintf(stderr, "mmap failed for address %lu: %s\n", address, strerror(errno));
            continue; // Move to the next address if this one fails
        } 
    }

    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: main <last 5 digits of your reg. no>\n");
        return EXIT_FAILURE;
    }

    work_init(atoi(argv[1]));

    // Set up large pages using addresses from the file
    setup_large_pages();

    if (work_run() == 0) {
        printf("Work completed successfully\n");
    }

    return 0;
}


// Performance counter stats for './main 24623':

//     13,024,910,004      L1-dcache-loads                                                         (40.00%)
//      6,166,967,396      L1-dcache-load-misses            #   47.35% of all L1-dcache accesses   (40.01%)
//         11,324,296      L1-dcache-stores                                                        (40.01%)
//         32,343,104      LLC-loads                                                               (40.01%)
//          1,640,252      LLC-load-misses                  #    5.07% of all L1-icache accesses   (40.01%)
//            187,941      LLC-stores                                                              (20.00%)
//              6,361      LLC-store-misses                                                        (20.00%)
//      6,915,952,597      dTLB-load-misses                                                        (29.99%)
//             49,759      dTLB-store-misses                                                       (39.99%)
//             70,384      iTLB-load-misses                                                        (39.99%)

//       30.608161194 seconds time elapsed

//       30.598771000 seconds user
//        0.007999000 seconds sys


//  Performance counter stats for './main 24623':

//     13,017,908,664      L1-dcache-loads                                                         (39.98%)
//      5,624,197,959      L1-dcache-load-misses            #   43.20% of all L1-dcache accesses   (39.98%)
//          7,496,117      L1-dcache-stores                                                        (39.98%)
//          6,159,286      LLC-loads                                                               (40.00%)
//          1,314,282      LLC-load-misses                  #   21.34% of all L1-icache accesses   (40.01%)
//            115,095      LLC-stores                                                              (20.01%)
//              3,988      LLC-store-misses                                                        (20.01%)
//      4,073,267,978      dTLB-load-misses                                                        (30.01%)
//             29,485      dTLB-store-misses                                                       (40.01%)
//             43,767      iTLB-load-misses                                                        (39.99%)

//       18.274826241 seconds time elapsed

//       18.266110000 seconds user
//        0.008000000 seconds sys
