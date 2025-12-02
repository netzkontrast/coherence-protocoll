---
name: knowledge-base-builder
description: This skill should be used when reading files (Markdown, Text, PDF) and creating or updating a knowledge base with semantic indexing using LanceDB for vector search capabilities. Supports hybrid storage with markdown files for human readability and LanceDB for efficient semantic queries.
---

# Knowledge Base Builder Skill

## Purpose

This skill enables extracting content from multiple file formats (Markdown, Text, PDF) and building a structured, searchable knowledge base. It combines:

- **Markdown-backed storage** for human-readable, version-controllable entries
- **LanceDB vector database** for semantic search capabilities
- **Metadata tracking** for file management and deduplication
- **Flexible categorization** for organizing knowledge across domains

## When to Use This Skill

Use this skill when:

- Extracting knowledge from documentation files into a searchable system
- Building a project-specific knowledge base from multiple sources
- Creating semantic search capabilities over structured content
- Ingesting technical documentation (code docs, guides, manuals)
- Maintaining a versioned, git-friendly knowledge repository
- Searching content by meaning, not just keywords

## How to Use This Skill

### 1. Understanding the Approach

The skill uses a hybrid architecture:

1. **Source files** → Parse into structured entries
2. **Markdown storage** → Human-readable `.md` files in `.knowledge_base/entries/`
3. **Vector indexing** → LanceDB creates semantic embeddings for search
4. **Metadata tracking** → JSON file tracks all entries and file hashes

See `references/kb_schema.md` for detailed schema documentation.

### 2. Core Capabilities

#### Ingest Files

To add content to the knowledge base, use `scripts/kb_manager.py`:

```bash
# Ingest markdown file (split by headers)
python scripts/kb_manager.py ingest /path/to/document.md docs

# Ingest text file (split into chunks)
python scripts/kb_manager.py ingest /path/to/notes.txt general

# Ingest PDF (split by pages)
python scripts/kb_manager.py ingest /path/to/manual.pdf guides
```

**File type handling:**
- **Markdown**: Automatically splits on headers (`#`, `##`, etc.), creating one entry per section
- **Text**: Chunks into 500-character segments with sequential ordering
- **PDF**: Extracts one entry per page with page number tracking

#### Search the Knowledge Base

```bash
# Semantic search (if LanceDB available)
python scripts/kb_manager.py search "authentication patterns"

# Keyword fallback search (without vector DB)
python scripts/kb_manager.py search "database"
```

#### List Entries

```bash
# List all entries
python scripts/kb_manager.py list

# List by category
python scripts/kb_manager.py list docs
```

#### Retrieve Full Entry

```bash
# Get markdown content of specific entry
python scripts/kb_manager.py get abc123def456
```

### 3. Integration with Claude

When using this skill in Claude Code:

1. **Read the Python script** at `scripts/kb_manager.py` to understand the API
2. **Import the manager** for programmatic use:
   ```python
   from kb_manager import KnowledgeBaseManager

   kb = KnowledgeBaseManager()
   entry_ids = kb.ingest_markdown("path/to/file.md", "docs")
   results = kb.search("my query")
   ```

3. **Use CLI mode** for automated workflows with subprocess calls
4. **Reference the schema** in `references/kb_schema.md` for data structure details

### 4. Configuration

Default behavior:
- Knowledge base stored in `.knowledge_base/` directory
- Vector model: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- Text chunk size: 500 characters (configurable in code)
- Deduplication: Based on file content hash

### 5. Dependencies

**Required:**
- Python 3.7+

**Optional (for full functionality):**
- `lancedb` - For semantic search with vectors
- `sentence-transformers` - For generating embeddings
- `pypdf` - For PDF text extraction

Install all optional dependencies:
```bash
pip install lancedb sentence-transformers pypdf
```

## Architecture Details

### Entry ID Generation

Entry IDs are deterministic MD5 hashes combining source file path and section identifier. This ensures:
- Same file re-ingested produces same IDs
- Enables deduplication and updates
- Provides stable references across sessions

### Semantic Search

When LanceDB is available:
1. Entry content encoded to 384-dimensional vector using all-MiniLM-L6-v2
2. Query text encoded to same vector space
3. L2 distance used to find semantically similar entries
4. Results ranked by similarity score

Fallback to keyword search if LanceDB unavailable.

### File Deduplication

Files tracked by MD5 hash of content:
- Hash stored in metadata
- Prevents duplicate processing
- Allows safe re-ingestion (overwrites with same hash)
- Clean audit trail of processed files

## Practical Examples

### Building a Documentation KB

```bash
# Ingest all documentation
python scripts/kb_manager.py ingest docs/getting-started.md docs
python scripts/kb_manager.py ingest docs/api-reference.md docs
python scripts/kb_manager.py ingest docs/troubleshooting.md docs

# Search semantically
python scripts/kb_manager.py search "how do I install the library?"
```

### Technical Knowledge Base

```bash
# Ingest from various sources
python scripts/kb_manager.py ingest design/architecture.md architecture
python scripts/kb_manager.py ingest notes/patterns.txt patterns
python scripts/kb_manager.py ingest manual.pdf reference

# Query by topic
python scripts/kb_manager.py search "microservices patterns"
```

## Output

The knowledge base creates:

- **`.knowledge_base/entries/*.md`** - Individual entry markdown files (git-friendly)
- **`.knowledge_base/metadata.json`** - Index and tracking (git-friendly)
- **`.knowledge_base/lancedb/`** - Vector index (binary, not git-tracked)

All text data is human-readable markdown, suitable for version control and review.

## Troubleshooting

**Vector search not working:**
- Install dependencies: `pip install lancedb sentence-transformers`
- Skill falls back to keyword search automatically if unavailable

**PDF extraction issues:**
- Install pypdf: `pip install pypdf`
- Some PDF types (scanned images) won't extract text

**Memory issues with large files:**
- Text chunking reduces memory usage (adjust in code if needed)
- Markdown headers naturally limit entry size

## See Also

- `references/kb_schema.md` - Complete data structure documentation
- `scripts/kb_manager.py` - Full implementation and Python API
