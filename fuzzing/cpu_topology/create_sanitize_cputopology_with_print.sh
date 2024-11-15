#!/bin/bash

# Usage: ./script.sh source_file.c function_name1 function_name2 ... output_file.c

# Arguments
SOURCE_FILE=$1
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
echo "#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include \"assert.h\"
#include \"pal_topology.h\"
" >> "$OUTPUT_FILE"

# Harcoded macros
echo "#define READ_ONCE(x)                                      \\
    ({                                                    \\
        __typeof__(x) y = *(volatile __typeof__(x)*)&(x); \\
        y;                                                \\
    })" >> "$OUTPUT_FILE"


echo "#define PAL_ERROR_INVAL 4
#define MAX_CACHES     4
#define MAX_THREADS    16
#define MAX_CORES      16
#define MAX_SOCKETS    16
#define MAX_NUMA_NODES 16
" >> "$OUTPUT_FILE"


# Extract #define IS_IN_RANGE_INCL from api.h and replace false with 0 and true with 1
awk '
  $0 ~ "^#define IS_IN_RANGE_INCL" {
    gsub("false", "0")
    gsub("true", "1")
    print
  }
' "./common/include/api.h" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Harcoded Function names

echo "size_t random_size_t(size_t min, size_t max){
    return rand() % (max - min + 1) + min;
}

static void coerce_untrusted_bool(bool* ptr) {
    static_assert(sizeof(bool) == sizeof(unsigned char), \"Unsupported compiler\");
    *ptr = !!READ_ONCE(*(unsigned char*)ptr);
}" >> "$OUTPUT_FILE"

echo "void print_data(struct pal_topo_info* topo_info) {
    printf(\"Caches: %zu\\n\", topo_info->caches_cnt);
    for (size_t i = 0; i < topo_info->caches_cnt; i++) {
        printf(
            \"Type: %d, Level: %zu, Size: %zu, Coherency Line Size: %zu, Number of Sets: %zu, \"
            \"Physical Line Partition: %zu\\n\",
            topo_info->caches[i].type, topo_info->caches[i].level, topo_info->caches[i].size,
            topo_info->caches[i].coherency_line_size, topo_info->caches[i].number_of_sets,
            topo_info->caches[i].physical_line_partition);
    }
    printf(\"\\n\");
    printf(\"Threads: %zu\\n\", topo_info->threads_cnt);
    for (size_t i = 0; i < topo_info->threads_cnt; i++) {
        printf(\"Is Online: %d, Core ID: %zu, Cache IDs: \", topo_info->threads[i].is_online,
               topo_info->threads[i].core_id);
        for (size_t j = 0; j < MAX_CACHES; j++) {
            printf(\"%zu \", topo_info->threads[i].ids_of_caches[j]);
        }
        printf(\"\\n\");
    }
    printf(\"\\n\");
    printf(\"Cores: %zu\\n\", topo_info->cores_cnt);
    for (size_t i = 0; i < topo_info->cores_cnt; i++) {
        printf(\"Socket ID: %zu, Node ID: %zu\\n\", topo_info->cores[i].socket_id,
               topo_info->cores[i].node_id);
    }
    printf(\"\\n\");
    printf(\"Sockets: %zu\\n\", topo_info->sockets_cnt);
    for (size_t i = 0; i < topo_info->sockets_cnt; i++) {
        printf(\"Unused: %c\\n\", topo_info->sockets[i].unused);
    }
    printf(\"\\n\");
    printf(\"NUMA Nodes: %zu\\n\", topo_info->numa_nodes_cnt);
    for (size_t i = 0; i < topo_info->numa_nodes_cnt; i++)
    {
        printf(\"Is Online: %d, Hugepages: \", topo_info->numa_nodes[i].is_online);
        for (size_t j = 0; j < HUGEPAGES_MAX; j++) {
            printf(\"%zu \", topo_info->numa_nodes[i].nr_hugepages[j]);
        }
        printf(\"\\n\");
    }
    printf(\"\\n\");
    printf(\"NUMA Distance Matrix:\\n\");
    for (size_t i = 0; i < topo_info->numa_nodes_cnt; i++) {
        for (size_t j = 0; j < topo_info->numa_nodes_cnt; j++) {
            printf(\"%zu \", topo_info->numa_distance_matrix[i * topo_info->numa_nodes_cnt + j]);
        }
        printf(\"\\n\");
    }
    printf(\"\\n\");
}" >> "$OUTPUT_FILE"


echo "void free_memory(struct pal_topo_info* topo_info) {
    free(topo_info->caches);
    free(topo_info->threads);
    free(topo_info->cores);
    free(topo_info->sockets);
    free(topo_info->numa_nodes);
    free(topo_info->numa_distance_matrix);
    free(topo_info);
}" >> "$OUTPUT_FILE"

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
      # skip empty lines
      if ($0 ~ "^\\s*$") next
      print

      # Count braces
      if ($0 ~ "\\{") brace_count++
      if ($0 ~ "\\}") brace_count--
      if (brace_count == 0 && $0 ~ "\\}") {
        in_func = 0
        print ""
      }
    }

    # Handle case where function is not found
    END {
      if (function_started == 0) {
        print "Function not found or function is empty" > "/dev/stderr"
        exit 1
      }
      else{
        print "Function extracted successfully" > "/dev/stderr"
      }
    }
  ' "$SOURCE_FILE" >> "$OUTPUT_FILE"
done


# Harcoded LLVMFuzzerTestOneInput function for libfuzzer
echo "int LLVMFuzzerTestOneInput(const uint32_t* Data, long long Size) {
    struct pal_topo_info* topo_info = calloc(1, sizeof(struct pal_topo_info));

    topo_info->caches_cnt     = 0;
    topo_info->threads_cnt    = 0;
    topo_info->cores_cnt      = 0;
    topo_info->sockets_cnt    = 0;
    topo_info->numa_nodes_cnt = 0;

    topo_info->caches               = calloc(MAX_CACHES, sizeof(struct pal_cache_info));
    topo_info->threads              = calloc(MAX_THREADS, sizeof(struct pal_cpu_thread_info));
    topo_info->cores                = calloc(MAX_CORES, sizeof(struct pal_cpu_core_info));
    topo_info->sockets              = calloc(MAX_SOCKETS, sizeof(struct pal_socket_info));
    topo_info->numa_nodes           = calloc(MAX_NUMA_NODES, sizeof(struct pal_numa_node_info));
    topo_info->numa_distance_matrix = calloc(MAX_NUMA_NODES * MAX_NUMA_NODES, sizeof(size_t));

    int len = Size / sizeof(uint32_t);

    if (Size < 1 || Data == NULL || len < 1) {
        free_memory(topo_info);
        return 0;
    }
    size_t index = 0;

    topo_info->caches_cnt = (Data[index++] % MAX_CACHES) + 1;
    for (size_t i = 0; i < topo_info->caches_cnt; i++) {
        if (index + 5 >= len){
            free_memory(topo_info);
            return 0;
        }
        topo_info->caches[i].type                    = Data[index++] % 3;
        topo_info->caches[i].level                   = (Data[index++] % 3) + 1;
        topo_info->caches[i].size                    = (Data[index++] % (1 << 30)) + 1;
        topo_info->caches[i].coherency_line_size     = (Data[index++] % (1 << 16)) + 1;
        topo_info->caches[i].number_of_sets          = (Data[index++] % (1 << 30)) + 1;
        topo_info->caches[i].physical_line_partition = (Data[index++] % (1 << 16)) + 1;
    }

    if(index + 1 >= len){
        free_memory(topo_info);
        return 0;
    }

    topo_info->threads_cnt = (Data[index++] % MAX_THREADS) + 1;

    for (size_t i = 0; i < topo_info->threads_cnt; i++) {
      if (index + 1 + MAX_CACHES >= len){
        free_memory(topo_info);
        return 0;
      }
      topo_info->threads[i].is_online = Data[index++] % 2;
      if (topo_info->threads[i].is_online) {
        topo_info->threads[i].core_id = Data[index++];
        for (size_t j = 0; j < MAX_CACHES; j++) {
          topo_info->threads[i].ids_of_caches[j] = Data[index++];
        }
      } else {
        topo_info->threads[i].core_id = 0;
        for (size_t j = 0; j < MAX_CACHES; j++) {
          topo_info->threads[i].ids_of_caches[j] = (size_t)-1;
        }
      }
    }

    if(index + 1 >= len){
      free_memory(topo_info);
      return 0;
    }
    topo_info->cores_cnt = (Data[index++] % MAX_CORES) + 1;
    for (size_t i = 0; i < topo_info->cores_cnt; i++) {
      if(index + 2 >= len){
        free_memory(topo_info);
        return 0;
      }
      topo_info->cores[i].socket_id = Data[index++];
      topo_info->cores[i].node_id   = Data[index++];
    }

    if(index + 1 >= len){
      free_memory(topo_info);
      return 0;
    }
    topo_info->sockets_cnt = (Data[index++] % MAX_SOCKETS) + 1;
    for (size_t i = 0; i < topo_info->sockets_cnt; i++) {
      if(index >= len){
        free_memory(topo_info);
        return 0;
      }
      topo_info->sockets[i].unused = Data[index++] % 26 + 'a';
    }

    if(index + 1 >= len){
      free_memory(topo_info);
      return 0;
    }

    topo_info->numa_nodes_cnt = (Data[index++] % MAX_NUMA_NODES) + 1;
    for (size_t i = 0; i < topo_info->numa_nodes_cnt; i++) {
      if(index + HUGEPAGES_MAX + 1 >= len){
        free_memory(topo_info);
        return 0;
      }
      topo_info->numa_nodes[i].is_online = Data[index++] % 2;
      if (topo_info->numa_nodes[i].is_online) {
        for (size_t j = 0; j < HUGEPAGES_MAX; j++) {
          topo_info->numa_nodes[i].nr_hugepages[j] = Data[index++];
        }
      }
    }

    for (size_t i = 0; i < topo_info->numa_nodes_cnt; i++) {
      for (size_t j = 0; j < topo_info->numa_nodes_cnt; j++) {
        if(index >= len){
          free_memory(topo_info);
          return 0;
        }
        topo_info->numa_distance_matrix[i * topo_info->numa_nodes_cnt + j] = Data[index++];
      }
    }
    printf(\"--------------------------\\n\");
    print_data(topo_info);

    int ret = sanitize_topo_info(topo_info);
    if (ret == 0) {
      print_data(topo_info);
      printf(\"Sanitize successfull\n\");
    } else {
      printf(\"Sanitize failed\n\");
    }

    free_memory(topo_info);
    return 0;
}" >> "$OUTPUT_FILE"