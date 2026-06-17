from langchain_ollama import ChatOllama
class Generator:
    def __init__(self):
        self.llm = ChatOllama(
            model="phi3:mini",
            temperature=0
        )

    def generate_answer(self, question, chunks):

        context = "\n\n".join(
            chunk.page_content for chunk in chunks
        )

        prompt = f"""
You are an AI assistant answering questions ONLY from the AWS Customer Agreement.

Rules:
1. Use ONLY the provided context.
2. If the answer is not in the context, say:
"I could not find this information in the AWS Customer Agreement."
3. Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content