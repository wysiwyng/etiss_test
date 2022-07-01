#include "etiss/Plugin.h"
#include "etiss/jit/CPU.h"
#include "etiss/jit/System.h"

namespace etiss {
    namespace plugin {
        class TraceInstruction : public etiss::TranslationPlugin
        {
            public:
				void init(ETISS_CPU *cpu, ETISS_System *system, CPUArch *arch) override;
				void cleanup() override;
                void finalizeInstrSet(etiss::instr::ModedInstructionSet &) const override;
                void initCodeBlock(etiss::CodeBlock &block) const override;
                std::string _getPluginName() const override;
				void callback(const char* c);
			private:
				ETISS_CPU* cpu_;
				ETISS_System* system_;
				CPUArch* arch_;
        };
    }
}