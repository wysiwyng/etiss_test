#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>


int main()
{

    printf("hello world!\n");
    printf("Reading CSRs:\n");
    int i;
  
    for (i = 1; i < 6; ++i)
    {
        uint64_t cpu_time;
        uint64_t cpu_time_h;

        asm volatile("csrr %0, 0xC01" : "=r"(cpu_time) : );
        asm volatile("csrr %0, 0xC81" : "=r"(cpu_time_h) : );
        cpu_time |= cpu_time_h << 32;

        printf("The CPU time is  %d\n", cpu_time);

        uint64_t cpu_cycle;
        uint64_t cpu_cycle_h;
        asm volatile("csrr %0, 0xC00" : "=r"(cpu_cycle) : );
        asm volatile("csrr %0, 0xC80" : "=r"(cpu_cycle_h) : );
        cpu_cycle |= cpu_cycle_h << 32;

        printf("The CPU cycles is  %d\n", cpu_cycle);

        uint64_t cpu_instret;
        uint64_t cpu_instret_h;
        asm volatile("csrr %0, 0xC02" : "=r"(cpu_instret) : );
        asm volatile("csrr %0, 0xC82" : "=r"(cpu_instret_h) : );
        cpu_instret |= cpu_instret_h << 32;

        printf("The instructions retured is  %d\n", cpu_instret);

    }
}