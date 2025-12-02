#!/usr/bin/env python3
"""
Knowledge Base Manager

Handles reading files (MD, TXT, PDF) and creating/updating a LanceDB knowledge base
with markdown-backed storage and vector embeddings for semantic search.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import hashlib

try:
    import lancedb
    HAS_LANCEDB = True
except ImportError:
    HAS_LANCEDB = False

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


class KnowledgeBaseManager:
    """Manages knowledge base creation, updates, and queries."""

    def __init__(self, kb_path: str = ".knowledge_base"):
        """
        Initialize the knowledge base manager.

        Args:
            kb_path: Path to knowledge base directory
        """
        self.kb_path = Path(kb_path)
        self.kb_path.mkdir(exist_ok=True)
        self.db_path = self.kb_path / "lancedb"
        self.md_path = self.kb_path / "entries"
        self.md_path.mkdir(exist_ok=True)
        self.metadata_file = self.kb_path / "metadata.json"

        self.metadata = self._load_metadata()
        self.db = None

        if HAS_LANCEDB:
            self.db = lancedb.connect(str(self.db_path))

    def _load_metadata(self) -> dict:
        """Load or initialize metadata."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "entries": {},
            "files_processed": []
        }

    def _save_metadata(self):
        """Save metadata to file."""
        self.metadata["updated"] = datetime.now().isoformat()
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def _get_file_hash(self, file_path: str) -> str:
        """Get hash of file content."""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def ingest_markdown(self, file_path: str, category: str = "general") -> list:
        """
        Ingest a markdown file into the knowledge base.

        Args:
            file_path: Path to markdown file
            category: Category for the entries

        Returns:
            List of entry IDs created
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        file_hash = self._get_file_hash(str(file_path))
        entries = self._parse_markdown(content, str(file_path), category)

        entry_ids = []
        for entry in entries:
            entry_id = self._save_entry(entry)
            entry_ids.append(entry_id)

        self.metadata["files_processed"].append({
            "file": str(file_path),
            "hash": file_hash,
            "type": "markdown",
            "processed": datetime.now().isoformat(),
            "entry_count": len(entries)
        })

        if HAS_LANCEDB:
            self._index_entries(entries)

        self._save_metadata()
        return entry_ids

    def ingest_text(self, file_path: str, category: str = "general", chunk_size: int = 500) -> list:
        """
        Ingest a plain text file into the knowledge base.

        Args:
            file_path: Path to text file
            category: Category for the entries
            chunk_size: Characters per chunk

        Returns:
            List of entry IDs created
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        file_hash = self._get_file_hash(str(file_path))

        # Split into chunks
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        entries = []

        for idx, chunk in enumerate(chunks):
            entry = {
                "id": self._generate_id(str(file_path), idx),
                "title": f"{file_path.stem} - Part {idx + 1}",
                "content": chunk,
                "category": category,
                "source": str(file_path),
                "type": "text",
                "created": datetime.now().isoformat()
            }
            entries.append(entry)

        entry_ids = []
        for entry in entries:
            entry_id = self._save_entry(entry)
            entry_ids.append(entry_id)

        self.metadata["files_processed"].append({
            "file": str(file_path),
            "hash": file_hash,
            "type": "text",
            "processed": datetime.now().isoformat(),
            "entry_count": len(entries),
            "chunk_size": chunk_size
        })

        if HAS_LANCEDB:
            self._index_entries(entries)

        self._save_metadata()
        return entry_ids

    def ingest_pdf(self, file_path: str, category: str = "general") -> list:
        """
        Ingest a PDF file into the knowledge base.

        Args:
            file_path: Path to PDF file
            category: Category for the entries

        Returns:
            List of entry IDs created
        """
        if not HAS_PYPDF:
            raise ImportError("pypdf is required for PDF ingestion. Install with: pip install pypdf")

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_hash = self._get_file_hash(str(file_path))
        entries = []

        try:
            reader = PdfReader(str(file_path))
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                entry = {
                    "id": self._generate_id(str(file_path), page_num),
                    "title": f"{file_path.stem} - Page {page_num + 1}",
                    "content": text,
                    "category": category,
                    "source": str(file_path),
                    "type": "pdf",
                    "page": page_num + 1,
                    "created": datetime.now().isoformat()
                }
                entries.append(entry)
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")

        entry_ids = []
        for entry in entries:
            entry_id = self._save_entry(entry)
            entry_ids.append(entry_id)

        self.metadata["files_processed"].append({
            "file": str(file_path),
            "hash": file_hash,
            "type": "pdf",
            "processed": datetime.now().isoformat(),
            "entry_count": len(entries)
        })

        if HAS_LANCEDB:
            self._index_entries(entries)

        self._save_metadata()
        return entry_ids

    def _parse_markdown(self, content: str, source: str, category: str) -> list:
        """Parse markdown into structured entries."""
        entries = []
        lines = content.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith('#'):
                # Save previous section
                if current_section:
                    entry = {
                        "id": self._generate_id(source, current_section),
                        "title": current_section,
                        "content": '\n'.join(current_content).strip(),
                        "category": category,
                        "source": source,
                        "type": "markdown",
                        "created": datetime.now().isoformat()
                    }
                    if entry["content"]:
                        entries.append(entry)

                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            entry = {
                "id": self._generate_id(source, current_section),
                "title": current_section,
                "content": '\n'.join(current_content).strip(),
                "category": category,
                "source": source,
                "type": "markdown",
                "created": datetime.now().isoformat()
            }
            if entry["content"]:
                entries.append(entry)

        return entries

    def _generate_id(self, source: str, identifier: str) -> str:
        """Generate a unique ID for an entry."""
        combined = f"{source}:{identifier}"
        return hashlib.md5(combined.encode()).hexdigest()[:16]

    def _save_entry(self, entry: dict) -> str:
        """Save entry as markdown file and return entry ID."""
        entry_id = entry["id"]

        # Create markdown file
        md_content = f"""# {entry['title']}

**Source:** {entry['source']}
**Category:** {entry['category']}
**Type:** {entry['type']}
**Created:** {entry['created']}

## Content

{entry['content']}
"""

        entry_file = self.md_path / f"{entry_id}.md"
        with open(entry_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

        # Update metadata
        self.metadata["entries"][entry_id] = {
            "title": entry["title"],
            "source": entry["source"],
            "category": entry["category"],
            "type": entry["type"],
            "created": entry["created"],
            "file": str(entry_file)
        }

        return entry_id

    def _index_entries(self, entries: list):
        """Index entries in LanceDB for semantic search."""
        if not HAS_LANCEDB:
            return

        try:
            from sentence_transformers import SentenceTransformer
            HAS_EMBEDDINGS = True
        except ImportError:
            HAS_EMBEDDINGS = False

        if not HAS_EMBEDDINGS:
            print("Warning: sentence-transformers not installed. Vector embeddings disabled.")
            print("Install with: pip install sentence-transformers")
            return

        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')

            # Prepare data for LanceDB
            data = []
            for entry in entries:
                embedding = model.encode(entry["content"], convert_to_tensor=False).tolist()
                data.append({
                    "id": entry["id"],
                    "title": entry["title"],
                    "content": entry["content"][:1000],  # Store first 1000 chars
                    "category": entry["category"],
                    "source": entry["source"],
                    "vector": embedding
                })

            # Create or update table
            table_name = "entries"
            if table_name not in self.db.table_names():
                self.db.create_table(table_name, data=data, mode="overwrite")
            else:
                table = self.db.open_table(table_name)
                table.add(data)
        except Exception as e:
            print(f"Warning: Could not index entries: {e}")

    def search(self, query: str, limit: int = 5) -> list:
        """
        Search the knowledge base semantically.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of matching entries
        """
        if not HAS_LANCEDB:
            return self._search_local(query, limit)

        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            query_embedding = model.encode(query, convert_to_tensor=False).tolist()

            table = self.db.open_table("entries")
            results = table.search(query_embedding).limit(limit).to_list()
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def _search_local(self, query: str, limit: int = 5) -> list:
        """Fallback search without vector DB."""
        query_lower = query.lower()
        results = []

        for entry_id, entry_meta in self.metadata["entries"].items():
            score = 0
            if query_lower in entry_meta["title"].lower():
                score += 2
            if query_lower in entry_meta["category"].lower():
                score += 1

            if score > 0:
                results.append({
                    "id": entry_id,
                    "title": entry_meta["title"],
                    "score": score
                })

        return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]

    def list_entries(self, category: str = None) -> list:
        """List all entries, optionally filtered by category."""
        entries = []
        for entry_id, entry_meta in self.metadata["entries"].items():
            if category is None or entry_meta["category"] == category:
                entries.append({
                    "id": entry_id,
                    "title": entry_meta["title"],
                    "category": entry_meta["category"],
                    "type": entry_meta["type"],
                    "source": entry_meta["source"]
                })
        return entries

    def get_entry(self, entry_id: str) -> str:
        """Get the full markdown content of an entry."""
        if entry_id not in self.metadata["entries"]:
            raise KeyError(f"Entry not found: {entry_id}")

        entry_file = Path(self.metadata["entries"][entry_id]["file"])
        with open(entry_file, 'r', encoding='utf-8') as f:
            return f.read()


def main():
    """CLI for knowledge base manager."""
    if len(sys.argv) < 2:
        print("Usage: kb_manager.py <command> [args]")
        print("Commands:")
        print("  ingest <file> [category]  - Ingest a file (MD, TXT, or PDF)")
        print("  search <query>            - Search the knowledge base")
        print("  list [category]           - List all entries")
        print("  get <entry_id>            - Get an entry")
        sys.exit(1)

    command = sys.argv[1]
    kb = KnowledgeBaseManager()

    if command == "ingest":
        if len(sys.argv) < 3:
            print("Usage: kb_manager.py ingest <file> [category]")
            sys.exit(1)
        file_path = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "general"

        file_ext = Path(file_path).suffix.lower()
        try:
            if file_ext == '.md':
                ids = kb.ingest_markdown(file_path, category)
                print(f"Ingested {len(ids)} entries from {file_path}")
            elif file_ext == '.txt':
                ids = kb.ingest_text(file_path, category)
                print(f"Ingested {len(ids)} entries from {file_path}")
            elif file_ext == '.pdf':
                ids = kb.ingest_pdf(file_path, category)
                print(f"Ingested {len(ids)} entries from {file_path}")
            else:
                print(f"Unsupported file type: {file_ext}")
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: kb_manager.py search <query>")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        results = kb.search(query)
        for result in results:
            print(f"- {result.get('title', result.get('id'))}")

    elif command == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        entries = kb.list_entries(category)
        for entry in entries:
            print(f"[{entry['type']}] {entry['title']} ({entry['category']})")

    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: kb_manager.py get <entry_id>")
            sys.exit(1)
        entry_id = sys.argv[2]
        content = kb.get_entry(entry_id)
        print(content)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
