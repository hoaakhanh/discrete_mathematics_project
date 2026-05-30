# Solving the Traveling Salesman Problem (TSP) using Hybrid Heuristic Architectures

An empirical study and implementation of a Two-Phase Hybrid Heuristic Framework to solve the Symmetric Euclidean Traveling Salesman Problem, benchmarked against the standard **ATT48** dataset (48 cities in the US).

##  Project Overview
This project evaluates the optimization efficiency, computational time complexity, and architectural synergy of combining constructive heuristics with localized neighborhood descent. 

We analyze two main algorithmic pipelines:
1. **Nearest Insertion (NI) + Relocate Local Search** (Primary Framework)
2. **Nearest Neighbor (NN) + Relocate Local Search** (Extended Comparison Baseline)

---

##  Algorithmic Architecture

The framework operates on a **Two-Phase Optimization** paradigm:

*   **Phase 1: Constructive Heuristic:** Generates a valid initial Hamiltonian cycle. We compare a globally-evaluated **Nearest Insertion (NI)** approach against a myopic, short-sighted **Nearest Neighbor (NN)** strategy.
*   **Phase 2: Local Search Refinement:** Uses the **Relocate** operator ($O(N^2)$ neighborhood scan) to systematically shift nodes to alternative cost-reducing positions and untangle structural inefficiencies.

---

##  Computational Performance & Results

The empirical data extracted from benchmarking the **ATT48** instance reveals a critical trade-off between initialization geometric quality and local search convergence dynamics:

| Phase 1 + Phase 2 Configuration | Initial Tour Length | Post-Relocate Tour Length | Net Distance Reduction | Algorithmic Improvement (%) | Cumulative Runtime (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Nearest Insertion + Relocate** | $37994.32$ | **34665.45** | $3328.87$ | 8.76% | $72.452 \text{ ms}$ |
| **Nearest Neighbor + Relocate** | $40526.42$ | $35896.90$ | **4629.52** | **11.42%** | **68.827 ms** |

###  Key Takeaways & Strategic Synergy
*   **The Power of Cooperative Synergy (NI + Relocate):** Nearest Insertion constructs a globally balanced baseline geometry. This allows the Relocate operator to focus on micro-adjustments, perfectly untangling paths to achieve the absolute best routing cost of **$34665.45$**.
*   **The Initialization Bottleneck (NN + Relocate):** While Nearest Neighbor is ultra-fast ($1.479\text{ ms}$ standalone), its localized greediness creates massive macro-level distortions. The Relocate operator lacks the global lookahead power to completely repair this mutated structure, causing it to get prematurely trapped in a poorer local optimum ($35896.90$).
*   **Industrial Applicability:** For real-time, dynamic dispatching, raw **NN** is ideal due to sub-2ms latency. For strategic logistics (reducing fuel and carbon footprints), the **NI + Relocate** configuration is the superior operational choice.

---

##  Getting Started

### Prerequisites
Make sure you have Python installed along with the required libraries for visualization:
```bash
pip install matplotlib numpy
