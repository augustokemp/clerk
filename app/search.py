import os
from clients import vo, conn

def search(q: str) -> list[tuple[str, str]]:
    result = vo.embed(texts=[q], model=os.environ["VOYAGE_API_MODEL"], input_type="query")
    emb = result.embeddings[0]

    rows = conn.execute("""
        SELECT source, content
        FROM chunks
        ORDER BY embedding <=> %s::vector
        LIMIT 3
        """, (emb,)
    ).fetchall()

    return rows
