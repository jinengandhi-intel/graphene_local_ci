# Commands for cpuid fuzzing using libfuzzer
# Install clang 
sudo apt install clang-12

sudo update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-12 100
sudo update-alternatives --install /usr/bin/clang clang /usr/bin/clang-12 100
export CC="clang"
export CXX="clang++"
export AS="clang"

# Compilation commands with clang
# 1. Compilation with only fuzzer without santizer
clang -fsanitize=fuzzer sanize_cpuid.c -o executable-name

# 2. Compilation with fuzzer and address sanitizer
clang -fsanitize=fuzzer,address sanize_cpuid.c -o executable-name

# 3. Compilation with fuzzer and memory sanitizer
clang -fsanitize=fuzzer,memory sanize_cpuid.c -o executable-name

# Starting fuzzing run
./executable-name values_corpus

# we can limit the time duration of fuzzing run with -max_total_time=60 in secs
./executable-name values_corpus -max_total_time=60

# Steps to generate coverage report
clang -fsanitize=fuzzer -fprofile-instr-generate -fcoverage-mapping -mllvm -runtime-counter-relocation sanize_cpuid.c -o executable-name

LLVM_PROFILE_FILE="executable-name.profraw" ./executable-name values_corpus -max_total_time=60

export PATH=$PATH:/opt/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-20.04/bin

llvm-profdata merge -sparse executable-name.profraw -o executable-name.profdata

llvm-cov report ./executable-name -instr-profile=executable-name.profdata
