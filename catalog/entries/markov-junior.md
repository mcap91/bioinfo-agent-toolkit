---
name: markov-junior
title: MarkovJunior
url: "https://github.com/mxgmn/MarkovJunior"
category: framework
summary: "Probabilistic programming language where programs are ordered lists of rewrite rules and inference is constraint propagation — generates dungeons, mazes, architecture, puzzles, and simulations on 2D/3D grids; C#/.NET, 153 examples, supports WFC and ConvChain nodes; MIT"
tags: [procedural-generation, rewrite-rules, constraint-propagation, markov-algorithms, wave-function-collapse, grid-generation, csharp, dotnet]
reviewed: 2026-09-29
acquired: 2026-09-29
supersedes: []
overlaps: []
license: MIT
security_flags: []
workflows: []
---

## What it does

MarkovJunior is a probabilistic programming language based on Markov algorithms — ordered lists of rewrite rules applied to grids. On each step the interpreter finds the first rule with a match, selects a random match, and applies it. Programs compose rules into sequence nodes (run one after another) and Markov nodes (loop back to the first matching child). Inference via constraint propagation allows imposing constraints on future state, generating only runs that reach the constrained goal.

Core capabilities:

- **Rewrite rules on grids**: `(RBB=WWR)` is a self-avoiding walk. `(WBB=WAW)` generates mazes. Rules work in any number of dimensions without modification.
- **Inference**: connects two states via rewrite rule chains using unidirectional or bidirectional constraint propagation. Generalizes Dijkstra fields to arbitrary rules. Solves Sokoban puzzles, generates grid-covering paths, connects points with constrained paths.
- **Composability**: sequence nodes, Markov nodes (with nesting à la REFAL), forall-nodes (from Imagegram), WFC and ConvChain custom nodes.
- **153 examples**: maze generation, dungeon generation (including Bob Nystrom's algorithm), architecture (ModernHouse, Apartemazements), puzzles, growth models, percolation.

## Mechanical details

C# console application, .NET Core, no dependencies beyond standard library. Runs on Windows/Linux/macOS. Models defined in XML (`models.xml`). Output as PNG or .vox (MagicaVoxel). Fast pattern matching via multidimensional Boyer-Moore; incremental match tracking avoids full grid scans. Notable ports: TypeScript (web), JavaScript, Rust (Python library), Python, Julia. Funded by Embark Studios, Oskar Stålberg, Freehold Games.

## Security

MIT licensed. No security flags. Standalone offline tool, no network calls, no credentials. Standard .NET build-from-source trust model.