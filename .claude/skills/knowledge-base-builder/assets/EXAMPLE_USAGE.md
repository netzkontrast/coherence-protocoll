# Knowledge Base Builder - Example Usage

This document shows practical examples of using the knowledge-base-builder skill.

## Quick Start

### 1. Create a Knowledge Base from Documentation

```bash
# Initialize (automatically created on first use)
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py list

# Ingest your documentation
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py ingest docs/README.md docs
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py ingest docs/API.md api
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py ingest guides/TUTORIAL.txt guides
```

### 2. Search the Knowledge Base

```bash
# Find relevant content
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py search "authentication setup"

# List all entries
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py list

# List entries by category
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py list docs
```

### 3. Retrieve Specific Entries

```bash
# Get full markdown of an entry (use ID from list output)
python .claude/skills/knowledge-base-builder/scripts/kb_manager.py get abc123def456
```

## Integration with Claude Code

### Python Integration

```python
from pathlib import Path
import sys

# Add skill to path
sys.path.insert(0, ".claude/skills/knowledge-base-builder/scripts")
from kb_manager import KnowledgeBaseManager

# Create manager instance
kb = KnowledgeBaseManager()

# Ingest files programmatically
entry_ids = kb.ingest_markdown("docs/guide.md", category="docs")
print(f"Created {len(entry_ids)} entries")

# Search semantically
results = kb.search("how does authentication work?")
for result in results:
    print(f"Found: {result['title']}")

# List all entries
all_entries = kb.list_entries()
for entry in all_entries:
    print(f"[{entry['type']}] {entry['title']} ({entry['category']})")

# Get full content
content = kb.get_entry(entry_ids[0])
print(content)
```

### CLI Integration in Scripts

```bash
#!/bin/bash

KB_SCRIPT=".claude/skills/knowledge-base-builder/scripts/kb_manager.py"

# Function to add documentation
add_docs() {
    local file=$1
    local category=${2:-general}
    python "$KB_SCRIPT" ingest "$file" "$category"
}

# Function to query KB
query_kb() {
    python "$KB_SCRIPT" search "$@"
}

# Usage
add_docs "docs/API.md" "api"
query_kb "REST endpoints"
```

## Real-World Scenarios

### Scenario 1: Building a Project Knowledge Base

```bash
# Ingest all project documentation
find docs/ -name "*.md" | while read file; do
    category=$(basename $(dirname "$file"))
    python scripts/kb_manager.py ingest "$file" "$category"
done

# Now search across all documentation
python scripts/kb_manager.py search "database configuration"
```

### Scenario 2: Creating a Code Patterns Repository

```bash
# Add design documents
python scripts/kb_manager.py ingest design/patterns.md patterns
python scripts/kb_manager.py ingest design/architecture.txt architecture

# Add API reference
python scripts/kb_manager.py ingest api-docs.pdf reference

# Search for implementation guidance
python scripts/kb_manager.py search "microservices"
```

### Scenario 3: Research and Notes Management

```bash
# Ingest research papers/notes
python scripts/kb_manager.py ingest research/notes-2025.txt research
python scripts/kb_manager.py ingest papers/summary.md papers

# Search semantically
python scripts/kb_manager.py search "machine learning best practices"
```

## Knowledge Base Location

By default, the knowledge base is stored in `.knowledge_base/`:

```
.knowledge_base/
├── entries/              # All parsed entries as markdown
│   ├── abc123def456.md
│   ├── def456ghi789.md
│   └── ...
├── lancedb/              # Vector database (if LanceDB installed)
├── metadata.json         # Index and file tracking
```

The entire directory can be:
- **Committed to git** (text-based, human-readable)
- **Backed up** easily
- **Reviewed** in version control
- **Shared** with team members

## Installation

### Dependencies

```bash
# Core functionality (always works)
# - No dependencies required

# For vector-based semantic search
pip install lancedb sentence-transformers

# For PDF support
pip install pypdf

# All features
pip install lancedb sentence-transformers pypdf
```

## Tips & Tricks

### Custom Knowledge Base Location

To use a different location, modify the `KnowledgeBaseManager` initialization:

```python
from kb_manager import KnowledgeBaseManager

# Use custom path
kb = KnowledgeBaseManager(kb_path="my_kb")
```

### Organizing by Category

Use meaningful category names to organize knowledge:

```bash
# By content type
python scripts/kb_manager.py ingest api.md api
python scripts/kb_manager.py ingest tutorial.md tutorial
python scripts/kb_manager.py ingest troubleshooting.txt support

# By topic
python scripts/kb_manager.py ingest auth.md authentication
python scripts/kb_manager.py ingest payments.md payments
```

### Viewing Knowledge Base Structure

```bash
# List all entries with details
python scripts/kb_manager.py list

# Count entries by category
python scripts/kb_manager.py list | grep -o '\[.*\]' | sort | uniq -c
```

### Maintenance

The `.knowledge_base/` directory is self-contained:

```bash
# Back up
cp -r .knowledge_base .knowledge_base.backup

# Reset
rm -rf .knowledge_base
# (Will be recreated on next use)

# Check size
du -sh .knowledge_base
```

## Workflow Example: Documentation Extraction

```bash
# 1. Prepare source documents
cp /path/to/docs/*.md ./docs-to-process/

# 2. Create knowledge base
mkdir -p .knowledge_base
python scripts/kb_manager.py list  # Initialize

# 3. Ingest all documents
for file in docs-to-process/*.md; do
    category=$(basename "$file" .md)
    python scripts/kb_manager.py ingest "$file" "$category"
done

# 4. Verify ingestion
python scripts/kb_manager.py list

# 5. Search to confirm
python scripts/kb_manager.py search "your test query"

# 6. Commit to version control
git add .knowledge_base/
git commit -m "docs: Add knowledge base from documentation"
```

## Next Steps

1. **Read** `references/kb_schema.md` for detailed structure
2. **Explore** `scripts/kb_manager.py` for API documentation
3. **Ingest** your first document
4. **Search** to verify it works
5. **Integrate** into your workflow
