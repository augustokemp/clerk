import argparse
import os

from search import search
from clients import claude


def answer(question: str) -> tuple[str, list[str]]:
    chunks = search(q=question)
    sources = sorted({source for source, _ in chunks})

    context = "\n\n".join(f"[{source}] {content}" for source, content in chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"

    response = claude.messages.create(
        model=os.environ["ANTHROPIC_API_MODEL"],
        max_tokens=500,
        system=(
            "You are a customer-support assistant. Answer the user's question using "
            "ONLY the context provided. If the answer is not in the context, say you "
            "don't have that information. Be concise."
        ),
        messages=[{"role": "user", "content": prompt}],
    )

    if not response.content:
        raise RuntimeError("Claude returned no content")

    return response.content[0].text, sources


def ask_and_print(question: str) -> None:
    text, sources = answer(question)
    print(f"\n{text}")
    if sources:
        print(f"\nSources: {', '.join(sources)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask clerk a question.")
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to ask. If omitted, starts interactive mode.",
    )
    args = parser.parse_args()

    # One-shot: `python app/ask.py "how do I get a refund?"`
    if args.question:
        ask_and_print(args.question)
        return

    # Interactive: empty line or Ctrl-C / Ctrl-D to quit
    print("clerk — ask a question (empty line or Ctrl-C to quit)")
    try:
        while True:
            question = input("\n> ").strip()
            if not question:
                break
            ask_and_print(question)
    except (EOFError, KeyboardInterrupt):
        pass
    print("\nBye!")


if __name__ == "__main__":
    main()
