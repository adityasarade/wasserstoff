from typing import List, Dict, Tuple
from app.services.llm_service import query_llm
from collections import defaultdict

def summarize_document_chunks(doc_chunks: List[Dict]) -> Dict:
    """
    Summarizes a single document using its chunks.
    Returns: {"doc_id", "answer", "citation"}
    """
    doc_id = doc_chunks[0]["doc_id"]
    content = "\n".join([
        f"Page {c['page']}, Para {c['sentence']}: {c['text']}"
        for c in doc_chunks
    ])

    system_prompt = "You are a helpful research assistant that summarizes documents."
    user_prompt = f"""Given the document chunks below, write a concise summary (2–3 sentences) of the document's main topic. Also include a citation based on the Page and Paragraph numbers shown.

Document Chunks:
{content}

Respond strictly in this format:
- Answer: <summary>
- Citation: Page X, Para Y"""

    response = query_llm(system_prompt, user_prompt)

    lines = response.strip().split("\n")
    answer = lines[0].replace("Answer: ", "").strip()
    citation = lines[1].replace("Citation: ", "").strip()

    return {"doc_id": doc_id, "answer": answer, "citation": citation}


def synthesize_themes(document_answers: List[Dict]) -> str:
    """
    Groups related document summaries into 2–3 core themes.
    Returns a structured theme synthesis with supporting doc_ids.
    """
    context = "\n".join([
        f"{doc['doc_id']}: {doc['answer']}"
        for doc in document_answers
    ])

    system_prompt = "You are a research assistant summarizing themes across documents."
    user_prompt = f"""You are given summaries from several documents. Identify 2–3 core themes across them. Label each theme, list supporting document IDs, and write a short explanation.

Document Summaries:
{context}

Respond in this format:

Theme 1: <Title>
- Supporting documents: DOC123, DOC456
- Description: <theme explanation>"""

    return query_llm(system_prompt, user_prompt)

def group_chunks_by_doc_id(chunks):
    grouped = defaultdict(list)
    for chunk in chunks:
        doc_id = chunk.get('doc_id')  # or whatever key identifies the doc
        grouped[doc_id].append(chunk)
    return dict(grouped)

def summarize_documents(grouped_chunks: Dict[str, List[Dict]]) -> Tuple[List[Dict], str]:
    """
    Summarizes each document and synthesizes themes from the summaries.
    """
    individual_results = []

    for doc_id, chunks in grouped_chunks.items():
        summary = summarize_document_chunks(chunks)
        individual_results.append(summary)

    synthesized_summary = synthesize_themes(individual_results)
    return individual_results, synthesized_summary