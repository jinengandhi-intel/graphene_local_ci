#!/bin/bash

# Usage: ./func.sh gramine_dir function_name1 function_name2 ... output_file.c

# Arguments
GRAMINE_DIR=$1
SOURCE_FILE=$GRAMINE_DIR/pal/src/host/linux-sgx/pal_misc.c
shift
OUTPUT_FILE=${!#}  # Last argument is the output file
FUNCTION_NAMES=("$@") # Get all arguments from 2nd to the last
unset 'FUNCTION_NAMES[${#FUNCTION_NAMES[@]}-1]' # Remove the last argument

# Validate arguments
if [ -z "$SOURCE_FILE" ] || [ ! -f "$SOURCE_FILE" ]; then
  echo "Usage: $0 source_file.c function_name1 function_name2 ... output_file.c"
  exit 1
fi

# Ensure the output file is empty or create it if it doesn't exist
: > "$OUTPUT_FILE"

# Harcoded headers
echo "#include <asm/fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <time.h>
#include <stdbool.h>
#include \"cpu.h\"
" >> "$OUTPUT_FILE"

# Extract #define CPUID_CACHE_SIZE from SOURCE_FILE
awk '
  $0 ~ "^#define CPUID_CACHE_SIZE" {
    print
  }
' "$SOURCE_FILE" >> "$OUTPUT_FILE"

# Extract #define IS_IN_RANGE_INCL from api.h and replace false with 0 and true with 1
awk '
  $0 ~ "^#define IS_IN_RANGE_INCL" {
    gsub("false", "0")
    gsub("true", "1")
    print
  }
' "$GRAMINE_DIR/common/include/api.h" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "int64_t  non_null_edx = 0;
int64_t  ex_state_enum_leaf_error = 0;
int64_t  tile_info_subleaf_0x0_error = 0;
int64_t  tile_info_subleaf_error = 0;
int64_t  tmul_info_leaf_error = 0;
int64_t  cpu_sanitized = 0;
int16_t is_cpuid_present = 0;
int16_t add_cpuid_cache = 0;
int64_t  get_cpuid_cache = 0;
time_t start, end;
bool start_timer;
double elapsed = 0.0;
" >> "$OUTPUT_FILE"

# Extract g_cpu_extension_offsets and g_cpu_extension_sizes from enclave_xstate.c
awk '
  BEGIN { in_cpu_extension_offsets = 0; in_cpu_extension_sizes = 0 }

  $0 ~ "^const uint32_t g_cpu_extension_offsets" {
    in_cpu_extension_offsets = 1
  }

  $0 ~ "^const uint32_t g_cpu_extension_sizes" {
    in_cpu_extension_sizes = 1
  }

  in_cpu_extension_offsets {
    print
    if ($0 ~ "}") {
      in_cpu_extension_offsets = 0
      print ""
    }
  }

  in_cpu_extension_sizes {
    print
    if ($0 ~ "}") {
      in_cpu_extension_sizes = 0
      print ""
    }
  }

' "$GRAMINE_DIR/pal/src/host/linux-sgx/enclave_xstate.c" >> "$OUTPUT_FILE"

# Extract static int g_pal_cpuid_cache_top from pal_misc.c
awk '
  $0 ~ "^static int g_pal_cpuid_cache_top" {
    print
  }
' "$SOURCE_FILE" >> "$OUTPUT_FILE"

# Extract struct pal_cpuid, static variable from pal_misc.c
awk '
  BEGIN { in_struct = 0 }

  $0 ~ "^static struct pal_cpuid" {
    in_struct = 1
  }

  in_struct {
    print
    if ($0 ~ "}") {
      in_struct = 0
      print ""
    }
  }

  END {
    if (in_struct) {
      print "Error: Could not find the end of struct pal_cpuid" > "/dev/stderr"
    }
  }
' "$SOURCE_FILE" >> "$OUTPUT_FILE"

# Extract static inline extension_enabled
# static inline uint32_t extension_enabled(uint32_t xfrm, uint32_t bit_idx) {
#     uint32_t feature_bit = 1U << bit_idx;
#     return xfrm & feature_bit;
# }
awk '
  BEGIN { in_func = 0 }

  $0 ~ "^static inline uint32_t extension_enabled" {
    in_func = 1
  }

  in_func {
    print
    if ($0 ~ "}") {
      in_func = 0
      print ""
    }
  }

' "$SOURCE_FILE" >> "$OUTPUT_FILE"

# Process each function name
for FUNCTION_NAME in "${FUNCTION_NAMES[@]}"; do
  echo "Extracting function '$FUNCTION_NAME' from '$SOURCE_FILE' into '$OUTPUT_FILE'"

  awk -v func_name="$FUNCTION_NAME" '
    BEGIN { in_func = 0; brace_count = 0; function_started = 0 }

    # Match the function definition line
    $0 ~ "^.*" func_name "\\s*\\(" {
      if (!function_started) {
        in_func = 1
        brace_count = 0
        function_started = 1
      }
    }

    # If inside the function, start copying lines
    in_func {
      # Skip spinlock functions
      if ($0 ~ "spinlock") {
        next
      }
      # skip empty lines
      if ($0 ~ "^\\s*$") next
      print

      # Count braces
      if ($0 ~ "\\{") brace_count++
      if ($0 ~ "\\}") brace_count--
      if (brace_count == 0 && $0 ~ "\\}") {
        in_func = 0
        print "/*" func_name "*/"
        print ""
      }
    }

    # Handle case where function is not found
    END {
      if (function_started == 0) {
        print "Function not found or function is empty" > "/dev/stderr"
      }
    }
  ' "$SOURCE_FILE" >> "$OUTPUT_FILE"
done

# Harcoded LLVMFuzzerTestOneInput function for libfuzzer
echo 'int LLVMFuzzerTestOneInput(const uint32_t *Data, long long Size) {
    uint32_t leaf = 11, subleaf = 4;
    uint32_t values[4];
    int len = Size/sizeof(uint32_t);
    int ret = -1;
    if(Size < 24 || Data == NULL || len < 6) {
        return 0;
    }
    values[0] = Data[0];
    values[1] = Data[1];
    values[2] = Data[2];
    values[3] = Data[3];
    leaf = Data[4];
    subleaf = Data[5];

   sanitize_cpuid(leaf, subleaf, values);
   add_cpuid_to_cache(leaf, subleaf, values);
   ret = get_cpuid_from_cache(leaf, subleaf, values);
   
    if (!start_timer){
        time(&start); /* start the timer */
        start_timer = true;
    }
    time(&end);
    elapsed = difftime(end, start);
    if (elapsed >= 1200.0){
        printf("Non-null EDX value in Processor Extended State Enum CPUID leaf hits : %ld\n", non_null_edx);
        printf("Unexpected values in Processor Extended State Enum CPUID leaf hits : %ld\n", ex_state_enum_leaf_error);
        printf("Tile Information CPUID Leaf (subleaf=0x0) error hits : %ld\n", tile_info_subleaf_0x0_error);
        printf("Tile Information CPUID Leaf (subleaf) error hits : %ld\n", tile_info_subleaf_error);
        printf("TMUL Information CPUID Leaf error hits : %ld\n", tmul_info_leaf_error);
        printf("cpuid sanitized hits : %ld\n", cpu_sanitized);
        printf("cpuid is already present hits : %hd\n", is_cpuid_present);
        printf("Added cpuid to the cache hits : %hd\n", add_cpuid_cache);
        printf("Got cpuid from cache hits : %ld\n", get_cpuid_cache);
        time(&start);
    }

    return 0;
}' >> "$OUTPUT_FILE"

# Replace some values with constants
sed -i -e 's/g_pal_linuxsgx_state.enclave_info.attributes.xfrm/231; \/\/ This value is constant 231 on Linux ubuntu/g' \
  -e 's/g_extended_feature_flags_max_supported_sub_leaves/2; \/\/ This value is constant 2 on Linux ubuntu/g' \
  -e 's/_PalProcessExit(1)/return/g' \
  -e 's/log_error/printf/g' \
  -e 's/PAL_ERROR_DENIED/6/g' "$OUTPUT_FILE"

# Replace print statement with counters
sed -i -e 's/printf("Non-null EDX.*CPUID leaf");/non_null_edx++;/' \
  -e 's/printf("Unexpected.*Processor Extended State Enum CPUID leaf");/ex_state_enum_leaf_error++;/' \
  -e 's/printf("Unexpected.*subleaf=0x0)");/tile_info_subleaf_0x0_error++;/' \
  -e 's/printf("Unexpected.*TMUL Information CPUID Leaf");/tmul_info_leaf_error++;/' \
  -e  '/values\[3\].*\.values\[3\];/a \            get_cpuid_cache++;' \
  -e  '/chosen.*values\[3\];/a \        add_cpuid_cache++;' \
  -e  '/.*CPUID entry is already present in the cache.*/a \                is_cpuid_present++;' "$OUTPUT_FILE"
sed -i -e ':a;N;$!ba;s/printf("Unexpected.*subleaf=%#x)".*subleaf);/tile_info_subleaf_error++;/' "$OUTPUT_FILE"
sed -i ':a;N;$!ba;s/}\n\/\*sanitize_cpuid\*\//    cpu_sanitized++;\n}/' "$OUTPUT_FILE"

echo "All functions have been copied to '$OUTPUT_FILE'"
