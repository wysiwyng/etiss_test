/**

        @copyright

        <pre>

        Copyright 2018 Infineon Technologies AG

        This file is part of ETISS tool, see <https://gitlab.lrz.de/de-tum-ei-eda-open/etiss>.

        The initial version of this software has been created with the funding support by the German Federal
        Ministry of Education and Research (BMBF) in the project EffektiV under grant 01IS13022.

        Redistribution and use in source and binary forms, with or without modification, are permitted
        provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice, this list of conditions and
        the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
        and the following disclaimer in the documentation and/or other materials provided with the distribution.

        3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse
        or promote products derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
        WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
        PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
        DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
        PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
        HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
        NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
        POSSIBILITY OF SUCH DAMAGE.

        </pre>

        @author Marc Greim <marc.greim@mytum.de>, Chair of Electronic Design Automation, TUM

        @date July 29, 2014

        @version 0.1

*/
/**
        @file

        @brief implementation of etiss/IntegratedLibrary/TraceInstruction.h

        @detail

*/

#include "etiss/IntegratedLibrary/TraceInstruction.h"
#include "etiss/CPUArch.h"
#include "etiss/CPUCore.h"

using namespace etiss::plugin;

void TraceInstruction::init(ETISS_CPU *cpu, ETISS_System *system, etiss::CPUArch *arch)
{
    arch_ = arch;
    cpu_ = cpu;
    system_ = system;
}

void TraceInstruction::cleanup()
{
    arch_ = nullptr;
    cpu_ = nullptr;
    system_ = nullptr;
}

void TraceInstruction::initCodeBlock(etiss::CodeBlock &block) const
{
    block.fileglobalCode().insert("extern void TraceInstruction_print(const char*, void*);"); // add print function
}

void TraceInstruction::finalizeInstrSet(etiss::instr::ModedInstructionSet &mis) const
{
	std::string pcode = getPointerCode();

    mis.foreach ([pcode](etiss::instr::VariableInstructionSet &vis) {
        vis.foreach ([pcode](etiss::instr::InstructionSet &set) {
            set.foreach ([pcode](etiss::instr::Instruction &instr) {
                instr.addCallback(
                    [&instr, pcode](etiss::instr::BitArray &ba, etiss::CodeSet &cs, etiss::instr::InstructionContext &ic) {
                        std::stringstream ss;

                        ss << "TraceInstruction_print(\"";

                        ss << "0x" << std::hex << std::setfill('0') << std::setw(16) << ic.current_address_ << ": ";

                        ss << instr.printASM(ba);

                        ss << "\", " << pcode << ");\n";

                        cs.append(CodePart::PREINITIALDEBUGRETURNING).code() = ss.str();

                        return true;
                    },
                    0);
            });
        });
    });
}

std::string TraceInstruction::_getPluginName() const
{
    return "TraceInstruction";
}

void TraceInstruction::callback(const char* c)
{
	auto f = plugin_core_->getStruct();
	std::cerr << c << std::setfill('0');

	unsigned int count = 0;

	f->foreachField(
		[&count](std::shared_ptr<etiss::VirtualStruct::Field> f) {
            if (f->name_ == "instructionPointer") return;
			if (count % 4 == 0) std::cerr << std::endl;
			std::cerr << f->name_ << ": 0x" << std::hex << std::setw(8) << f->read() << " | ";
			count++;
		}
	);

	std::cerr << std::endl;
}

extern "C"
{
    void TraceInstruction_print(const char* c, void* traceinstruction)
    {
		auto plugin = (TraceInstruction*)traceinstruction;
		plugin->callback(c);
    }
}
