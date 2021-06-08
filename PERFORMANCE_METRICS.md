# Flowchart for running Benchmarks and displaying the performance metrics.

1. 5 Test runs for the 3 Just-In-Time Engines, namely TCC, GCC, and LLVM. This implies total 15 benchmarks are run.
2. MIPS for each run is recorded
3. The average MIPS for each JIT engine is extracted and stored in json files.
4. The MIPS result from current commit is compared against the previous best result. Only the best result is stored for future comparison.
5. The MIPS for the current commit and the previous best MIPS are displayed in three ways till now:

   If the github event is a PUSH:
   a) As a comment under an open issue
   b) As a webpage given by the link : https://samanti-das.github.io/etiss_new/
   c) As a wiki page

   If the github event is a PULL REQUEST:
   a) As a comment under an open pull request
   b) As a webpage given by the link : https://samanti-das.github.io/etiss_new/
   c) As a wiki page
