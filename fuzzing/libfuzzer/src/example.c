// fuzz_example_file.c
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

// Bubble sort algorithm
void bubble_sort(int arr[], size_t n) {
    for (size_t i = 0; i < n - 1; ++i) {
        for (size_t j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// LibFuzzer entry point
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Ensure input size is multiple of int size
    if (size % sizeof(int) != 0 || size == 0) {
        return 0;  // Input size not valid
    }
 
    // Determine number of integers in the input
    size_t num_integers = size / sizeof(int);
 
    // Cast input data to array of integers
    const int *input_array = (const int *)data;
 
    // Allocate memory for sorted array
    int *sorted_array = (int *)malloc(size);
    if (sorted_array == NULL) {
        return 0;  // Memory allocation failed
    }
 
    // Perform bubble sort on the input array
    memcpy(sorted_array, input_array, size);
    bubble_sort(sorted_array, num_integers);
 
    // Free allocated memory
    free(sorted_array);
 
    return 0;
}

