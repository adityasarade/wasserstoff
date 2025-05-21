from typing import List, Dict, Tuple
from app.services.llm_service import query_llm
from collections import defaultdict
from app.config import params

def summarize_document_chunks(doc_chunks: List[Dict]) -> Dict:
    """
    Summarizes a single document using its chunks.
    Returns: {"doc_id", "answer", "citation"}
    """
    doc_id = doc_chunks[0]["doc_id"]
    
    # Build the LLM input
    content = "\n".join([
        f"Page {c['page']}, Para {c['sentence']}: {c['text']}"
        for c in doc_chunks
    ])
    
    # Specific task and structure provided to the llm
    prompts = params["prompts"]["summarize_doc"]
    system_prompt = prompts["system"]
    user_prompt = prompts["user"].format(content=content)

    response = query_llm(system_prompt, user_prompt)
    lines = response.strip().split("\n")
    
    # Find the answer and citation lines
    answer_line = next((l for l in lines if l.lower().startswith("answer:")), "")
    citation_line = next((l for l in lines if l.lower().startswith("citation:")), "")

    # Extract the text after the colon
    answer = answer_line.split(":", 1)[1].strip() if ":" in answer_line else answer_line
    citation = citation_line.split(":", 1)[1].strip() if ":" in citation_line else citation_line

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
    
    # LLM groups the summaries and provides us with different Themes
    prompts = params["prompts"]["synthesize_themes"]
    system_prompt = prompts["system"]
    user_prompt = prompts["user"].format(context=context)

    return query_llm(system_prompt, user_prompt)

def group_chunks_by_doc_id(chunks):
    """
    Groups a flat list of chunks into a dict mapping doc_id -> [chunks].
    """
    grouped: Dict[str, List[Dict]] = defaultdict(list)
    for chunk in chunks:
        grouped[chunk["doc_id"]].append(chunk)
    return dict(grouped)

def summarize_documents(grouped_chunks: Dict[str, List[Dict]]) -> Tuple[List[Dict], str]:
    """
    Summarizes each document and synthesizes themes from the summaries.
    Returns: (individual_summaries, synthesized_summary)
    """
    individual_results : List[Dict] = []

    for doc_id, chunks in grouped_chunks.items():
        summary = summarize_document_chunks(chunks)
        individual_results.append(summary)
        
    synthesized_summary = synthesize_themes(individual_results)
    
    # Returning the final output to be presented
    return individual_results, synthesized_summary