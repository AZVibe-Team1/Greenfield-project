# ChromaDB Mock Data

This directory contains mock text data used to populate the ChromaDB vector store for the Job Portal application. The data is used for Retrieval-Augmented Generation (RAG) to provide intelligent, context-aware responses.

## Data Files

1. **job_postings.txt** - Sample job postings across various tech roles
2. **company_profiles.txt** - Company information and profiles
3. **interview_tips.txt** - Interview preparation guides and tips
4. **resume_writing.txt** - Resume writing best practices
5. **career_development.txt** - Career growth and development advice

## Adding New Data

To add new data to the knowledge base:

1. Create a new `.txt` file in this directory
2. Add your content (plain text format)
3. Run the ingestion script to update the vector store:
   ```bash
   docker compose run backend python backend/ingest_data.py
   ```

## Data Format

- Files should be in plain text format (`.txt`)
- Use clear section separators (e.g., `---` or blank lines)
- Include descriptive headers for better context
- Keep content relevant to job search, career development, or tech industry

## Notes

- The ingestion script automatically chunks the text for optimal retrieval
- Larger files will be split into smaller, overlapping chunks
- Metadata (file names) is preserved for source attribution
- The vector store uses semantic search to find relevant content

