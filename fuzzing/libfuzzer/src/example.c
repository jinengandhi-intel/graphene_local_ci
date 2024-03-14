// fuzz_example_file.c
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>

char get_first_cap(const char *in, int size) {
  const char *first_cap = NULL;
 //  printf("%s", in);
  if (size == 0)
    return ' ';
  for ( ; *in != 0; in++) {
    if (*in >= 'A' && *in <= 'Z') {
      first_cap = in;
      break;
    }
  }
  if (first_cap)
    return *first_cap;
  else
    return ' ';
}

int LLVMFuzzerTestOneInput(const char *Data, long long Size) {
  get_first_cap(Data, Size);
  return 0;
}

