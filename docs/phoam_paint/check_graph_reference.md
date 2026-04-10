Analyze the impact of a proposed change by querying the project knowledge graph.

Change description: $ARGUMENTS

## Instructions

Spawn an Explore agent to do the heavy lifting. This keeps the main context clean.

Use the Agent tool with subagent_type "Explore" and the following prompt:

---

You are analyzing the impact of a proposed change in this project.

**Change description**: $ARGUMENTS

**Your task**:

1. Run `python scripts/kb_graph.py rebuild-index` to ensure KB_INDEX.md is
   current.

2. Read KB_INDEX.md to understand the project structure.

3. Identify which modules/systems the change involves. Map them to entry-point
   files in the index.

4. For each entry point, run blast-radius queries:
   ```
   python scripts/kb_graph.py traverse <entry-point> --depth 2
   python scripts/kb_graph.py neighbors <entry-point>
   ```

5. Read every affected file the graph reveals. Do not skip any.

6. If the change involves creating a new module that parallels an existing one
   in the repo (e.g., a new `qc.py` in a sibling directory where one already
   exists), identify the existing analog as a **Template** in your report. The
   implementing agent should read the template before writing the new module.

7. Return a structured impact report:

### Change Summary
One sentence.

### Entry Points
Primary files that need edits. List each with its graph key.

### Blast Radius (via graph)
Files surfaced by traversal, grouped by depth, with WHY each is relevant.

### Template (if applicable)
Existing in-repo analog that the new module should follow. Include file path and
the key patterns to replicate (function signatures, return types, how it's wired
into its parent orchestrator/caller).

### Blockers & Decisions
- OPEN: questions that must be resolved before implementation
- DECIDED: existing decisions that constrain this change (quote the source)

### Impact Assessment
- Scope: Isolated (1-2 files) | Moderate (3-5) | Wide (6+)
- Breaking: Yes/No
- Risk: LOW / MEDIUM / HIGH (based on how many packages are in blast radius)
- Complexity: Simple | Moderate | Complex

### Recommended Approach
3-5 bullet plan.

### New Wiki-Links Needed
Specific [[wiki-links]] to add to connect this change into the graph.

---

Once the agent returns, display its report directly to the user.
