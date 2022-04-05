/**
 * Generated on Wed, 02 Mar 2022 20:09:51 +0100.
 *
 * This file contains the function macros for the RV32IMACFD core architecture.
 */

#ifndef __RV32IMACFD_FUNCS_H
#define __RV32IMACFD_FUNCS_H

#ifndef ETISS_ARCH_STATIC_FN_ONLY
#include "Arch/RV32IMACFD/RV32IMACFD.h"
#include "etiss/jit/CPU.h"
#include "etiss/jit/System.h"
#include "etiss/jit/ReturnCode.h"
#endif



#ifndef ETISS_ARCH_STATIC_FN_ONLY

static inline etiss_uint32 csr_read (ETISS_CPU * const cpu, ETISS_System * const system, void * const * const plugin_pointers, etiss_uint32 csr)
{
if (csr == 1) {
return *((RV32IMACFD*)cpu)->CSR[3] & 31;
}
if (csr == 2) {
return (*((RV32IMACFD*)cpu)->CSR[3] >> 5) & 7;
}
if (csr == 3072) {
return etiss_get_cycles(cpu, system, plugin_pointers);
}
if (csr == 3200) {
return etiss_get_cycles(cpu, system, plugin_pointers) >> 32;
}
if (csr == 3073) {
return etiss_get_time();
}
if (csr == 3201) {
return etiss_get_time() >> 32;
}
if (csr == 3074) {
return etiss_get_instret(cpu, system, plugin_pointers);
}
if (csr == 3202) {
return etiss_get_instret(cpu, system, plugin_pointers) >> 32;
}
return *((RV32IMACFD*)cpu)->CSR[csr];
}

#endif

#ifndef ETISS_ARCH_STATIC_FN_ONLY

static inline void csr_write (ETISS_CPU * const cpu, ETISS_System * const system, void * const * const plugin_pointers, etiss_uint32 csr, etiss_uint32 val)
{
if (csr == 1) {
*((RV32IMACFD*)cpu)->CSR[3] = (*((RV32IMACFD*)cpu)->CSR[3] & (7 << 5)) | (val & 31);
} else {
if (csr == 2) {
*((RV32IMACFD*)cpu)->CSR[3] = ((val & 7) << 5) | (*((RV32IMACFD*)cpu)->CSR[3] & 31);
} else {
if (csr == 3) {
*((RV32IMACFD*)cpu)->CSR[3] = val & 255;
} else {
*((RV32IMACFD*)cpu)->CSR[csr] = val;
}
}
}
}

#endif
#endif