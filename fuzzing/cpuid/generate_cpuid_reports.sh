#!/bin/bash

# Usage: ./generate_cpuid_reports.sh log_file [address|memory]

sanitizer=$2
non_null_EDX_value=$(grep "Non-null EDX value in Processor Extended State Enum CPUID leaf hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
processor_extended_state_enum_error=$(grep "Unexpected values in Processor Extended State Enum CPUID leaf hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
tile_information_CPUID_leaf_subleaf_0x0_error=$(grep "Tile Information CPUID Leaf (subleaf=0x0) error hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
tile_information_CPUID_leaf_error=$(grep "Tile Information CPUID Leaf (subleaf) error hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
TMUL_information_CPUID_leaf_error=$(grep "TMUL Information CPUID Leaf error hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
cpuid_sanitized=$(grep "cpuid sanitized hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
cpuid_already_present=$(grep "cpuid is already present hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
add_cpuid_to_cache=$(grep "Added cpuid to the cache hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
got_cpuid_from_cache=$(grep "Got cpuid from cache hits" $1 | tail -1 | cut -d: -f2 | tr -d ' ')
finalcorpus=$(ls values_corpus | wc -l)
mutations=$(grep -E "#[0-9]+" $1 | tail -1 | cut -d# -f2 | cut -f1)


create_cpuid_libfuzzer_report(){
    echo "$1","$2","$3","$4","$5","$6","$7","$8","$9","${10}","${11}","${12}"  > cpuid_libfuzzer_${sanitizer}_sanitizer_report.csv
}

write_cpuid_libfuzzer_report(){
    sed -i "1a$1,$2,$3,$4,$5,$6,$7,$8,$9,${10},${11},${12}" cpuid_libfuzzer_${sanitizer}_sanitizer_report.csv
}



create_cpuid_libfuzzer_report "Timeout" "Mutation" "Final corpus" "CPUID sanitized" "Non-null EDX value" "Processor Extended State Enum error" "Tile Information CPUID Leaf (subleaf=0x0) error" "Tile Information CPUID Leaf error" "TMUL Information CPUID Leaf error" "cpuid already present" "Add cpuid to cache" "Got cpuid from cache"
write_cpuid_libfuzzer_report $timeout $mutations $finalcorpus $cpuid_sanitized $non_null_EDX_value $processor_extended_state_enum_error $tile_information_CPUID_leaf_subleaf_0x0_error $tile_information_CPUID_leaf_error $TMUL_information_CPUID_leaf_error $cpuid_already_present $add_cpuid_to_cache $got_cpuid_from_cache