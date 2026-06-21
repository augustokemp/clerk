from search import search
from clients import claude

question = "Do you ship to the moon?"

chunks = search(q=question)

context = "\n\n".join(f"[{source}] {content}" for source, content in chunks)
prompt = f"Context:\n{context}\n\nQuestion: {question}"

msg = claude.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    system=(
        "You are a customer-support assistant. Answer the user's question using "
        "ONLY the context provided. If the answer is not in the context, say you "
        "don't have that information. Be concise."
    ),
    messages=[{"role": "user", "content": prompt}],
)

print(msg.content[0].text)
print("\nSources:", ", ".join(sorted({source for source, _ in chunks})))