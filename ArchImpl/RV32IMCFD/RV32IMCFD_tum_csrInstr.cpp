/**
 * Generated on Wed, 23 Feb 2022 20:40:41 +0100.
 *
 * This file contains the instruction behavior models of the tum_csr
 * instruction set for the RV32IMCFD core architecture.
 */

#include "RV32IMCFDArch.h"

#define ETISS_ARCH_STATIC_FN_ONLY
#include "RV32IMCFDFuncs.h"

using namespace etiss;
using namespace etiss::instr;


// CSRRW -----------------------------------------------------------------------
static InstructionDefinition csrrw_rd_rs1_csr (
	ISA32_RV32IMCFD,
	"csrrw",
	(uint32_t) 0x001073,
	(uint32_t) 0x00707f,
	[] (BitArray & ba,etiss::CodeSet & cs,InstructionContext & ic)
	{

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 rs1 = 0;
static BitArrayRange R_rs1_0(19, 15);
rs1 += R_rs1_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		CodePart & partInit = cs.append(CodePart::INITIALREQUIRED);

		partInit.code() = std::string("//CSRRW\n");

// -----------------------------------------------------------------------------
partInit.code() += "cpu->instructionPointer = " + std::to_string(ic.current_address_ + 4) + ";\n";
partInit.code() += "etiss_uint32 xrs1 = *((RV32IMCFD*)cpu)->X[" + std::to_string(rs1) + "];\n";
if (rd != 0) {
partInit.code() += "etiss_uint32 xrd = csr_read(cpu, system, plugin_pointers, " + std::to_string(csr) + ");\n";
partInit.code() += "csr_write(cpu, system, plugin_pointers, " + std::to_string(csr) + ", xrs1);";
partInit.code() += "*((RV32IMCFD*)cpu)->X[" + std::to_string(rd) + "] = xrd;\n";
} else {
partInit.code() += "csr_write(cpu, system, plugin_pointers, " + std::to_string(csr) + ", xrs1);";
}
// -----------------------------------------------------------------------------

		partInit.getRegisterDependencies().add(reg_name[rs1], 32);
		partInit.getAffectedRegisters().add(reg_name[rd], 32);
		partInit.getAffectedRegisters().add("instructionPointer", 32);

		return true;
	},
	0,
	[] (BitArray & ba, Instruction & instr)
	{
// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 rs1 = 0;
static BitArrayRange R_rs1_0(19, 15);
rs1 += R_rs1_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		std::stringstream ss;
// -----------------------------------------------------------------------------
ss << "csrrw" << " # " << ba << (" [rd=" + std::to_string(rd) + " | rs1=" + std::to_string(rs1) + " | csr=" + std::to_string(csr) + "]");
// -----------------------------------------------------------------------------
		return ss.str();
	}
);

// CSRRS -----------------------------------------------------------------------
static InstructionDefinition csrrs_rd_rs1_csr (
	ISA32_RV32IMCFD,
	"csrrs",
	(uint32_t) 0x002073,
	(uint32_t) 0x00707f,
	[] (BitArray & ba,etiss::CodeSet & cs,InstructionContext & ic)
	{

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 rs1 = 0;
static BitArrayRange R_rs1_0(19, 15);
rs1 += R_rs1_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		CodePart & partInit = cs.append(CodePart::INITIALREQUIRED);

		partInit.code() = std::string("//CSRRS\n");

// -----------------------------------------------------------------------------
partInit.code() += "cpu->instructionPointer = " + std::to_string(ic.current_address_ + 4) + ";\n";
partInit.code() += "etiss_uint32 xrd = csr_read(cpu, system, plugin_pointers, " + std::to_string(csr) + ");\n";
partInit.code() += "etiss_uint32 xrs1 = *((RV32IMCFD*)cpu)->X[" + std::to_string(rs1) + "];\n";
if (rs1 != 0) {
partInit.code() += "csr_write(cpu, system, plugin_pointers, " + std::to_string(csr) + ", xrd | xrs1);";
}
if (rd != 0) {
partInit.code() += "*((RV32IMCFD*)cpu)->X[" + std::to_string(rd) + "] = xrd;\n";
}
// -----------------------------------------------------------------------------

		partInit.getRegisterDependencies().add(reg_name[rs1], 32);
		partInit.getAffectedRegisters().add(reg_name[rd], 32);
		partInit.getAffectedRegisters().add("instructionPointer", 32);

		return true;
	},
	0,
	[] (BitArray & ba, Instruction & instr)
	{
// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 rs1 = 0;
static BitArrayRange R_rs1_0(19, 15);
rs1 += R_rs1_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		std::stringstream ss;
// -----------------------------------------------------------------------------
ss << "csrrs" << " # " << ba << (" [rd=" + std::to_string(rd) + " | rs1=" + std::to_string(rs1) + " | csr=" + std::to_string(csr) + "]");
// -----------------------------------------------------------------------------
		return ss.str();
	}
);

// CSRRC -----------------------------------------------------------------------
static InstructionDefinition csrrc_rd_rs1_csr (
	ISA32_RV32IMCFD,
	"csrrc",
	(uint32_t) 0x003073,
	(uint32_t) 0x00707f,
	[] (BitArray & ba,etiss::CodeSet & cs,InstructionContext & ic)
	{

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 rs1 = 0;
static BitArrayRange R_rs1_0(19, 15);
rs1 += R_rs1_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		CodePart & partInit = cs.append(CodePart::INITIALREQUIRED);

		partInit.code() = std::string("//CSRRC\n");

// -----------------------------------------------------------------------------
partInit.code() += "cpu->instructionPointer = " + std::to_string(ic.current_address_ + 4) + ";\n";
partInit.code() += "etiss_uint32 xrd = csr_read(cpu, system, plugin_pointers, " + std::to_string(csr) + ");\n";
partInit.code() += "etiss_uint32 xrs1 = *((RV32IMCFD*)cpu)->X[" + std::to_string(rs1) + "];\n";
if (rs1 != 0) {
partInit.code() += "csr_write(cpu, system, plugin_pointers, " + std::to_string(csr) + ", xrd & ~(xrs1));";
}
if (rd != 0) {
partInit.code() += "*((RV32IMCFD*)cpu)->X[" + std::to_string(rd) + "] = xrd;\n";
}
// -----------------------------------------------------------------------------

		partInit.getRegisterDependencies().add(reg_name[rs1], 32);
		partInit.getAffectedRegisters().add(reg_name[rd], 32);
		partInit.getAffectedRegisters().add("instructionPointer", 32);

		return true;
	},
	0,
	[] (BitArray & ba, Instruction & instr)
	{
// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 rs1 = 0;
static BitArrayRange R_rs1_0(19, 15);
rs1 += R_rs1_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		std::stringstream ss;
// -----------------------------------------------------------------------------
ss << "csrrc" << " # " << ba << (" [rd=" + std::to_string(rd) + " | rs1=" + std::to_string(rs1) + " | csr=" + std::to_string(csr) + "]");
// -----------------------------------------------------------------------------
		return ss.str();
	}
);

// CSRRWI ----------------------------------------------------------------------
static InstructionDefinition csrrwi_rd_zimm_csr (
	ISA32_RV32IMCFD,
	"csrrwi",
	(uint32_t) 0x005073,
	(uint32_t) 0x00707f,
	[] (BitArray & ba,etiss::CodeSet & cs,InstructionContext & ic)
	{

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 zimm = 0;
static BitArrayRange R_zimm_0(19, 15);
zimm += R_zimm_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		CodePart & partInit = cs.append(CodePart::INITIALREQUIRED);

		partInit.code() = std::string("//CSRRWI\n");

// -----------------------------------------------------------------------------
partInit.code() += "cpu->instructionPointer = " + std::to_string(ic.current_address_ + 4) + ";\n";
partInit.code() += "etiss_uint32 xrd = csr_read(cpu, system, plugin_pointers, " + std::to_string(csr) + ");\n";
partInit.code() += "csr_write(cpu, system, plugin_pointers, " + std::to_string(csr) + ", " + std::to_string((etiss_uint32)(zimm)) + ");";
if (rd != 0) {
partInit.code() += "*((RV32IMCFD*)cpu)->X[" + std::to_string(rd) + "] = xrd;\n";
}
// -----------------------------------------------------------------------------

		partInit.getAffectedRegisters().add(reg_name[rd], 32);
		partInit.getAffectedRegisters().add("instructionPointer", 32);

		return true;
	},
	0,
	[] (BitArray & ba, Instruction & instr)
	{
// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 zimm = 0;
static BitArrayRange R_zimm_0(19, 15);
zimm += R_zimm_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		std::stringstream ss;
// -----------------------------------------------------------------------------
ss << "csrrwi" << " # " << ba << (" [rd=" + std::to_string(rd) + " | zimm=" + std::to_string(zimm) + " | csr=" + std::to_string(csr) + "]");
// -----------------------------------------------------------------------------
		return ss.str();
	}
);

// CSRRSI ----------------------------------------------------------------------
static InstructionDefinition csrrsi_rd_zimm_csr (
	ISA32_RV32IMCFD,
	"csrrsi",
	(uint32_t) 0x006073,
	(uint32_t) 0x00707f,
	[] (BitArray & ba,etiss::CodeSet & cs,InstructionContext & ic)
	{

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 zimm = 0;
static BitArrayRange R_zimm_0(19, 15);
zimm += R_zimm_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		CodePart & partInit = cs.append(CodePart::INITIALREQUIRED);

		partInit.code() = std::string("//CSRRSI\n");

// -----------------------------------------------------------------------------
partInit.code() += "cpu->instructionPointer = " + std::to_string(ic.current_address_ + 4) + ";\n";
partInit.code() += "etiss_uint32 xrd = csr_read(cpu, system, plugin_pointers, " + std::to_string(csr) + ");\n";
if (zimm != 0) {
partInit.code() += "csr_write(cpu, system, plugin_pointers, " + std::to_string(csr) + ", xrd | " + std::to_string((etiss_uint32)(zimm)) + ");";
}
if (rd != 0) {
partInit.code() += "*((RV32IMCFD*)cpu)->X[" + std::to_string(rd) + "] = xrd;\n";
}
// -----------------------------------------------------------------------------

		partInit.getAffectedRegisters().add(reg_name[rd], 32);
		partInit.getAffectedRegisters().add("instructionPointer", 32);

		return true;
	},
	0,
	[] (BitArray & ba, Instruction & instr)
	{
// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 zimm = 0;
static BitArrayRange R_zimm_0(19, 15);
zimm += R_zimm_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		std::stringstream ss;
// -----------------------------------------------------------------------------
ss << "csrrsi" << " # " << ba << (" [rd=" + std::to_string(rd) + " | zimm=" + std::to_string(zimm) + " | csr=" + std::to_string(csr) + "]");
// -----------------------------------------------------------------------------
		return ss.str();
	}
);

// CSRRCI ----------------------------------------------------------------------
static InstructionDefinition csrrci_rd_zimm_csr (
	ISA32_RV32IMCFD,
	"csrrci",
	(uint32_t) 0x007073,
	(uint32_t) 0x00707f,
	[] (BitArray & ba,etiss::CodeSet & cs,InstructionContext & ic)
	{

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 zimm = 0;
static BitArrayRange R_zimm_0(19, 15);
zimm += R_zimm_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		CodePart & partInit = cs.append(CodePart::INITIALREQUIRED);

		partInit.code() = std::string("//CSRRCI\n");

// -----------------------------------------------------------------------------
partInit.code() += "cpu->instructionPointer = " + std::to_string(ic.current_address_ + 4) + ";\n";
partInit.code() += "etiss_uint32 xrd = csr_read(cpu, system, plugin_pointers, " + std::to_string(csr) + ");\n";
if (zimm != 0) {
partInit.code() += "csr_write(cpu, system, plugin_pointers, " + std::to_string(csr) + ", xrd & " + std::to_string(~(((etiss_uint32)(zimm)))) + ");";
}
if (rd != 0) {
partInit.code() += "*((RV32IMCFD*)cpu)->X[" + std::to_string(rd) + "] = xrd;\n";
}
// -----------------------------------------------------------------------------

		partInit.getAffectedRegisters().add(reg_name[rd], 32);
		partInit.getAffectedRegisters().add("instructionPointer", 32);

		return true;
	},
	0,
	[] (BitArray & ba, Instruction & instr)
	{
// -----------------------------------------------------------------------------
etiss_uint32 rd = 0;
static BitArrayRange R_rd_0(11, 7);
rd += R_rd_0.read(ba) << 0;
etiss_uint32 zimm = 0;
static BitArrayRange R_zimm_0(19, 15);
zimm += R_zimm_0.read(ba) << 0;
etiss_uint32 csr = 0;
static BitArrayRange R_csr_0(31, 20);
csr += R_csr_0.read(ba) << 0;

// -----------------------------------------------------------------------------

		std::stringstream ss;
// -----------------------------------------------------------------------------
ss << "csrrci" << " # " << ba << (" [rd=" + std::to_string(rd) + " | zimm=" + std::to_string(zimm) + " | csr=" + std::to_string(csr) + "]");
// -----------------------------------------------------------------------------
		return ss.str();
	}
);