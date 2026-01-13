from llama_index.core import Document

def load_chunks_as_documents(chunks):
    documents = []

    for chunk in chunks:
        documents.append(
            Document(
                text=chunk["text"],
                metadata={
                    "chunk_id": chunk["chunk_id"],
                    "book_id": chunk["book_id"],
                    "chapter_number": chunk["chapter_number"],
                    "chapter_name": chunk["chapter_name"],
                    "section_number": chunk["section_number"],
                    "section_name": chunk["section_name"],
                    "topic": chunk.get("topic"),
                    "page_start": chunk["chapter_page_start"],
                    "page_end": chunk["chapter_page_end"],
                }
            )
        )

    return documents