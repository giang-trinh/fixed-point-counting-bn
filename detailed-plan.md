# Counting Fixed Points in Boolean Networks: ASP vs. SAT

## Goal

The aim of this study is to systematically evaluate, compare, and understand modern methods for **counting fixed points** in Boolean Networks (BNs).
This includes both **algorithmic performance** and **theoretical properties**, as well as applications beyond biological models such as Dialectical Abstract frameworks (ADFs).

Most recent work:

+ ASP: Scalable Counting of Minimal Trap Spaces and Fixed Points in Boolean Networks (CP'25) <https://doi.org/10.4230/LIPIcs.CP.2025.17>
+ SAT: A SAT-based method for counting all singleton attractors in Boolean networks (IJCAI'25) <https://doi.org/10.24963/ijcai.2025/290>

CP'25 and IJCAI'25 remain poorly understood in terms of
- comparative performance,
- interaction with preprocessing reduction techniques,
- applications to ADFs.

To achieve this, we focus on the following research questions:

### RQ1: ASP vs. SAT Approaches

*What is the practical and conceptual comparison between ASP and SAT approaches for counting fixed points in BNs?*

Key aspects to compare:

- Counting efficiency (runtime, scalability, memory usage)
- Exact vs. approximate counting performance
- Encoding size and structural properties
- Behavior on real biological networks vs. synthetic benchmarks

### RQ2: Effect of Network Reductions

*How do BN reduction techniques influence the performance of counting methods?*

Reduction techniques preserving fixed points (i.e., there is a bijection between the set of fixed points of the reduced BN and that of the original BN):

+ Stripping output nodes (Efficient Handling of Large Signalling-Regulatory Networks by Focusing on Their Core Control <https://doi.org/10.1007/978-3-642-33636-2_17>)
+ Propagating fixed nodes (A Reduction Method for Boolean Network Models Proven to Conserve Attractors <https://doi.org/10.1137/13090537X>)
+ Suppressing non-autoregulated nodes (Reduction of Boolean network models <https://doi.org/10.1016/j.jtbi.2011.08.042>)

Specific questions:

- Which reduction techniques give the best performance gains?
- Do ASP and SAT methods for BNs benefit differently from reductions?
- How do reductions interact with exact vs. approximate counters?
- Regarding approximate counting, how do reductions influence the size of independent support?
- Is there a systematic way to predict when reductions will be helpful?
- Regarding reduced model construction, how do the syntactical procedure and the BDD-based procedure (An open problem: Why are motif-avoidant attractors so rare in asynchronous Boolean networks? <https://doi.org/10.1007/s00285-025-02235-8>) behave?

### RQ3: Applications to ADFs

*How can fixed-point counting for BNs provide insights or tools for ADFs?*

Notes:

- 2-valued models of an ADF = fixed points of its corresponding BN
- There is no reduction technique regarding 2-valued models in ADFs.
- There is no counting method regarding 2-valued models in ADFs.
- Applying BN fixed-point counting methods and reduction techniques to 2-valued model counting in ADFs, then obtaining new insights in terms of ADFs

## Methodology

### Tested Problems 

All three fixed-point counting problems formulated in CP'25: C-FIX-1, C-FIX-2, C-FIX-3

> Some SAT encodings do not directly support C-FIX-2 and C-FIX-3, thus we need some slight adaptions. [Son]

### Dataset Construction

Three separate datasets:

+ Real-world BNs
+ Synthetic BNs
+ ADFs: find harder models [Van-Giang, Sam]

> BN models are taken from the benchmarks of CP'25 and IJCAI'25.

> ADF models taken from the benchmarks of FM'26 (submitted, focusing on ADFs).

> Can apply the method of npj paper on phenotype-determining nodes to get a meaningful set of phenotype nodes [Sam]

### Methods Evaluated

ASP encodings $\times$ SAT encodings $\times$ \{exact counting, approximate counting\}

**ASP encodings:**

- NNF-based ASP encoding (from CP'25)

> Can overlook inferior ASP encodings (e.g., pyboolnet, mpbn, trapmvn, an-asp)

Improvement, analogous to hybrid encoding in IJCAI'25 [Sam, Van-Giang]

**SAT encodings:**

- Three CNF encodings (from IJCAI'25)
- Native CNF encoding (from TCBB'11 (A SAT-based algorithm for finding attractors in synchronous Boolean networks <https://doi.org/10.1109/TCBB.2010.20>) and IJCAI'11 (Logic programming for boolean networks) <https://www.ijcai.org/Proceedings/11/Papers/160.pdf>)
- SAF (from SAF: SAT-based attractor finder in asynchronous automata networks <https://doi.org/10.1007/978-3-031-42697-1_12>)

### Network Reductions to Evaluate

\{Stripping output nodes, Propagating fixed nodes, Suppressing non-autoregulated nodes\} $\times$ \{syntactical construction, BDD-based construction\}

> For the suppressing non-autoregulated nodes reduction, we should consider multiple stop criteria similar to those investigated in ``Phenotype control and elimination of variables in Boolean networks'' <https://doi.org/10.24072/pcjournal.452>.

> [Sam] guide Son to run AEON's BDD-based reduction

> Optimize the reduction workflow, threshold setting [Sam]

> [Van-Giang] stop criteria may be related to treewidth

### Evaluation Criteria

- Runtime
- Memory consumption
- Output (exact count or estimate)
- Error bounds for approximate methods
- Solver robustness
- Influence of reductions (speedup factors)

## Targets

### Conferences and Expected Submission Types

ICLP 2026 <https://www.semsys.aau.at/events/iclp2026/>: 

- Technical Communication paper (March 27, 2026)

KR 2026 <https://kr.org/KR2026/>: 

- KR in the Wild track (mid February, 2026) ---> full paper (focus on implementation, datasets, reproducible empirical findings)
- Main track (February 13, 2026) ---> short paper
 
CP 2026 (best fit) <https://cp2026.a4cp.org/>:
 
- Short paper (March 07, 2026)
- Full paper (March 07, 2026)

> Van-Giang: I think if we can manipulate all stuff mentioned above, it is potentially possible to submit a full paper.

## Members

+ Van-Giang
+ Thanh-Son Phan (Van-Giang's 4-year undergraduate student at VNU-HCMUT <https://hcmut.edu.vn/en>)
+ Sam 
+ Mahi

## Extension of CP'25

>Van-Giang: I guess Mahi might be concerned about the extension of CP'25. I and Sam agreed on the following plan.

Follow the biological direction:

- Biological case studies with experimental validation
- Some other ideas from Sam, e.g., sensitivity of BN phenotypes to perturbations of their input nodes
- Target a biology journal such as IEEE TCBB and Bioinformatics
- Can collaborate with Anna who is a systems biologist working on large BNs

Possibly another conference paper if obtaining:

- New methodological results (e.g., more efficient encodings, ways to reduce the size of independent support)
- New complexity results on BN fixed-point counting
- Applications to probabilistic reasoning in BNs

