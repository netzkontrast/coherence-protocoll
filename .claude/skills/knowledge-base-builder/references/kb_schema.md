# Knowledge Base Schema

## Overview

The Knowledge Base uses a hybrid approach:
- **Markdown files** for human-readable, version-controllable storage
- **LanceDB** for vector-based semantic search and efficient querying
- **JSON metadata** for tracking and indexing

## Directory Structure

```
.knowledge_base/
├── entries/              # Markdown files (one per KB entry)
│   ├── abc123def456.md
│   ├── def456ghi789.md
│   └── ...
├── lancedb/             # LanceDB vector database
│   ├── data/
│   └── ...
└── metadata.json        # Index and tracking file
```

## Entry Format

Each entry is stored as a markdown file with frontmatter-style metadata:

```markdown
# Entry Title

**Source:** /path/to/original/file
**Category:** general
**Type:** markdown|text|pdf
**Created:** 2025-12-02T10:30:00

## Content

[Full entry content here]
```

### Entry Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique 16-char hash ID |
| `title` | string | Entry title (from heading or derived) |
| `content` | string | Main entry content |
| `category` | string | Categorization for organization |
| `source` | string | Original file path |
| `type` | string | Entry type: `markdown`, `text`, or `pdf` |
| `created` | ISO string | Creation timestamp |

## Metadata Structure

```json
{
  "created": "2025-12-02T10:30:00",
  "updated": "2025-12-02T10:35:00",
  "entries": {
    "abc123def456": {
      "title": "Entry Title",
      "source": "/path/to/file.md",
      "category": "general",
      "type": "markdown",
      "created": "2025-12-02T10:30:00",
      "file": ".knowledge_base/entries/abc123def456.md"
    }
  },
  "files_processed": [
    {
      "file": "/path/to/file.md",
      "hash": "a1b2c3d4e5f6g7h8",
      "type": "markdown",
      "processed": "2025-12-02T10:30:00",
      "entry_count": 3
    }
  ]
}
```

## LanceDB Schema

When available, LanceDB stores vector embeddings:

```
Table: entries
├── id (string)          - Entry ID
├── title (string)       - Entry title
├── content (string)     - First 1000 chars of content
├── category (string)    - Entry category
├── source (string)      - Original source
└── vector (float[384])  - Embedding vector (all-MiniLM-L6-v2)
```

## Processing Rules

### Markdown Files
- Headers (# ## ###) become entry boundaries
- Each section becomes a separate entry
- Content between headers belongs to that section

### Text Files
- Split into chunks (default 500 characters)
- Each chunk becomes a separate entry
- Preserves sequential order

### PDF Files
- Each page becomes a separate entry
- Page number stored in metadata
- Text extracted using pypdf

## Vector Embeddings

When LanceDB and sentence-transformers are available:

- Model: `all-MiniLM-L6-v2` (384-dimensional)
- Encoding: Text content encoded to vector
- Search: L2 distance for similarity matching
- Indexing: Automatic indexing on ingestion

## File Deduplication

Files are tracked by hash to prevent duplicate ingestion:
- Hash computed from file content (MD5)
- Prevents re-processing same file
- Update supported by re-processing with new hash
