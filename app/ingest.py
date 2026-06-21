import os
from clients import conn, vo

DATA_DIR = "./data/docs"

def main():
    conn.execute("TRUNCATE chunks RESTART IDENTITY")
    all_chunks = []
      
    for source in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, source)

        with open(path, "r") as f:
            content = f.read()

        sections = content.split("\n## ")

        for section in sections:
            section = section.strip()
            if not section:
                continue

            all_chunks.append((source, section))

    texts = [section for (source, section) in all_chunks]
    result = vo.embed(texts, model=os.environ["VOYAGE_API_MODEL"], input_type="document")
    embeddings = result.embeddings

    for (source, section), embedding in zip(all_chunks, embeddings):
        conn.execute(
            "INSERT INTO chunks (source, content, embedding) VALUES (%s, %s, %s)",
            (source, section, embedding),
        )

    conn.commit()

if __name__ == "__main__":
    main()



