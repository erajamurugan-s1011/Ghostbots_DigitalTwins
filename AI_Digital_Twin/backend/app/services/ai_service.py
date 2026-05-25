from transformers import pipeline
from app.services.embedding_service import search_text

# Load model
chatbot = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)


def generate_reply(message):

    # Retrieve memory
    context = search_text(message)

    if not context:
        return "I could not find that information."

    prompt = f"""
You are Ghostbot.

Context:
{context}

Rules:
- Answer only from the context
- Give only one direct answer
- Do not repeat the context
- Maximum 15 words

Question:
{message}

Answer:
"""

    output = chatbot(
        prompt,
        max_new_tokens=15,
        do_sample=False,
        temperature=0.1
    )

    generated = output[0]["generated_text"]

    response = generated.replace(prompt, "").strip()

    # Remove accidental continuation
    stop_words = [
        "Question:",
        "Context:",
        "Answer:",
        "\n"
    ]

    for word in stop_words:
        if word in response:
            response = response.split(word)[0]

    return response.strip()