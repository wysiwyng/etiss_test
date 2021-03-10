#include "platform.h"

/* The functions in this file are only meant to support Dhrystone on an
 * embedded RV32 system and are obviously incorrect in general. */

long time(void)
{
  return get_timer_value() / get_timer_freq();
}

// set the number of dhrystone iterations
void __wrap_scanf(const char* fmt, int* n)
{
//  *n = 100000000;
  *n = 1000000;
}

volatile uint64_t tohost;
volatile uint64_t fromhost;

void __wrap_exit(int n){
      tohost = 0x1;
      for (;;);
}
