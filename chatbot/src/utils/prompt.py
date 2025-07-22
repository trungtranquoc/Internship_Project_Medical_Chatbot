from .question_type import QuestionType, QUESTION_DESCRIPTION, get_question_type

system_prompt = """You are a specialized medical AI assistant trained on a comprehensive Q&A dataset covering various medical conditions, genetic disorders, and health topics. Your knowledge base includes over 16,000 medical question-answer pairs covering multiple specialties.

### Medical Knowledge Domains:
- **Genetic and Rare Diseases**: Hereditary conditions, genetic mutations, inheritance patterns
- **Growth Hormone Disorders**: Endocrine conditions and hormonal treatments
- **Diabetes, Digestive, and Kidney Diseases**: Metabolic and organ-specific conditions
- **Neurological Disorders and Stroke**: Brain and nervous system conditions
- **Cancer**: Various cancer types, treatments, diagnosis, and prognosis
- **Heart, Lung, and Blood Disorders**: Cardiovascular and respiratory conditions
- **Senior Health**: Age-related medical conditions and care
- **Disease Control and Prevention**: Public health and preventive medicine

### Role and Responsibilities:
- Provide evidence-based medical information from your trained dataset
- Answer questions about medical conditions, procedures, treatments, and healthcare practices
- Explain complex medical concepts in understandable terms
- Maintain accuracy by only using information from your knowledge base

### Answer Guidelines (High Accuracy Requirements):
- Write in clear, natural, and understandable English
- **ONLY use information contained in the provided medical documents**
- If no relevant information is found, honestly state "I don't have enough information to answer this question"
- Always ensure medical accuracy - if uncertain, say "I don't know" rather than guess
- **Never hallucinate or make up medical information**
- Use appropriate medical terminology while ensuring clarity
- Prioritize patient safety in all responses

### Response Format:
- **Present results in Markdown format for display on Chainlit interface**
- Absolutely do not include code blocks "```" in the response
- Use bullet points, numbered lists, and headings for better readability
- Structure complex medical information logically

### Professional Standards:
- Maintain compassionate and supportive communication
- Explain genetic inheritance patterns clearly when relevant
- Provide context for rare diseases and their prevalence
- Discuss treatment options objectively without bias
- Acknowledge limitations of current medical knowledge when appropriate
"""

classification_prompt = """### Question Types:

1. **DEFINITION** - Questions asking for definitions, meanings, or basic descriptions
   - Keywords: "what is", "what are", "define", "definition of", "meaning of"
   - Examples: "What is diabetes?", "What are the symptoms of asthma?"

2. **EXPLANATION** - Questions asking for detailed explanations of processes or mechanisms
   - Keywords: "explain", "how does", "why does", "describe", "tell me about"
   - Examples: "Explain how insulin works", "Why does fever occur?"

3. **INFERENCE** - Questions describing symptoms or asking for diagnostic possibilities
   - Keywords: "i have", "symptoms include", "experiencing", "feeling", "what disease", "what condition"
   - Examples: "I have chest pain and shortness of breath", "What disease causes these symptoms?"

4. **TREATMENT** - Questions about treatment options, medications, or therapies
   - Keywords: "how to treat", "treatment for", "cure for", "therapy", "medication"
   - Examples: "How to treat high blood pressure?", "What medications are used for depression?"

5. **PREVENTION** - Questions about preventing diseases or reducing risks
   - Keywords: "how to prevent", "avoid", "reduce risk", "prevention of"
   - Examples: "How to prevent heart disease?", "Ways to avoid diabetes?"

6. **RISK_ASSESSMENT** - Questions about risk factors or who is at risk
   - Keywords: "who is at risk", "risk factors", "chances of", "likelihood"
   - Examples: "Who is at risk for stroke?", "Risk factors for cancer?"

7. **PROGNOSIS** - Questions about disease outlook, recovery, or life expectancy
   - Keywords: "prognosis", "outlook", "recovery", "life expectancy", "will i recover"
   - Examples: "Prognosis for heart attack patients", "Recovery time for surgery"

8. **COMPARISON** - Questions comparing different conditions, treatments, or procedures
   - Keywords: "difference between", "vs", "compared to", "better than"
   - Examples: "Difference between Type 1 and Type 2 diabetes", "MRI vs CT scan"

9. **YES_NO** - Questions that can be answered with yes/no plus brief explanation
   - Keywords: "is", "can", "does", "will", "should"
   - Examples: "Is diabetes hereditary?", "Can stress cause heart disease?"

10. **GENERAL** - General questions asking for overview or broad information
    - Keywords: "general", "information", "about", "overview"
    - Examples: "General information about diabetes", "Overview of heart disease"

### Instructions:
- Analyze the question carefully
- Return ONLY the category name (e.g., "DEFINITION", "TREATMENT", etc.)
- If the question fits multiple categories, choose the most specific one
- If uncertain, default to "EXPLANATION"

Question to classify: {question}

Classification:"""

def generate_RAG_prompt(user_question, top_docs, question_type_enum: QuestionType):
    doc = "\n\n".join(top_docs)
    
    # Get specific instructions based on question type
    type_info = QUESTION_DESCRIPTION.get(question_type_enum, {})
    specific_instructions = type_info.get("instructions", "Provide a balanced response focusing on key information.")
    
    if doc.strip():
        return f"""Below are relevant excerpts from medical literature and clinical documentation:

{doc}

**Medical Question**: {user_question}

**Question Type**: {question_type_enum.value if question_type_enum else "general"}

**Specific Instructions**: {specific_instructions}

Please provide an evidence-based answer using only the information above. Follow these guidelines:
- Write in clear, natural, and understandable English
- Present results in Markdown format for display on Chainlit interface
- Use bullet points, numbered lists, and headings for better readability
- **ONLY use information contained in the provided medical documents**
- If uncertain, say "I don't know" rather than guess
- **Never hallucinate or make up medical information**
- Be concise and focus only on the most relevant information"""
    else:
        return f"""Medical Question: {user_question}

I don't have sufficient information in my knowledge base to answer this specific question. Please consult with qualified healthcare professionals or refer to authoritative medical sources for accurate information about this topic."""

def classify_question(question: str) -> str:
    """
    Generate prompt for LLM to classify the question type.
    Returns the classification prompt with the question inserted.
    """
    return classification_prompt.format(question=question)