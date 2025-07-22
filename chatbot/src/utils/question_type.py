from enum import Enum

class QuestionType(str, Enum):
    DEFINITION = "definition"
    EXPLANATION = "explanation"
    INFERENCE = "inference"
    TREATMENT = "treatment"
    PREVENTION = "prevention"
    RISK_ASSESSMENT = "risk assessment"
    PROGNOSIS = "prognosis"
    COMPARISON = "comparison"
    YES_NO = "yes no"
    EMERGENCY = "emergency"
    GENERAL = "general"

QUESTION_DESCRIPTION = {
    QuestionType.DEFINITION: {
        "keywords": ["what is", "what are", "define", "definition of", "meaning of"],
        "examples": ["What is diabetes?", "What are the symptoms of asthma?"],
        "response_style": "concise_definition",
        "instructions": "Provide a brief definition in 3-4 sentences. Focus on the most relevant aspects."
    },
    QuestionType.EXPLANATION: {
        "keywords": ["explain", "how does", "why does", "describe", "tell me about"],
        "examples": ["Explain how insulin works", "Why does fever occur?"],
        "response_style": "detailed_explanation",
        "instructions": "Explain the mechanism or process in 3-4 sentences. Focus on the most important aspects."
    },

    QuestionType.INFERENCE: {
        "keywords": ["i have", "symptoms include", "experiencing", "feeling", "what disease", "what condition"],
        "examples": ["I have chest pain and shortness of breath", "What disease causes these symptoms?"],
        "response_style": "diagnostic_guidance",
        "instructions": "List the most likely conditions based on symptoms. Emphasize seeing a healthcare provider. Keep to 3-4 key possibilities."
    },

    QuestionType.TREATMENT: {
        "keywords": ["how to treat", "treatment for", "cure for", "therapy", "medication"],
        "examples": ["How to treat high blood pressure?", "What medications are used for depression?"],
        "response_style": "treatment_focused",
        "instructions": "List primary treatment options in bullet points. Include 3-5 main approaches only."
    },

    QuestionType.PREVENTION: {
        "keywords": ["how to prevent", "avoid", "reduce risk", "prevention of"],
        "examples": ["How to prevent heart disease?", "Ways to avoid diabetes?"],
        "response_style": "prevention_focused",
        "instructions": "Provide 3-5 key prevention strategies in bullet points. Focus on actionable advice."
    },

    QuestionType.RISK_ASSESSMENT: {
        "keywords": ["who is at risk", "risk factors", "chances of", "likelihood"],
        "examples": ["Who is at risk for stroke?", "Risk factors for cancer?"],
        "response_style": "risk_focused",
        "instructions": "Identify 3-4 main risk factors. Be specific about high-risk populations."
    },

    QuestionType.PROGNOSIS: {
        "keywords": ["prognosis", "outlook", "recovery", "life expectancy", "will i recover"],
        "examples": ["Prognosis for heart attack patients", "Recovery time for surgery"],
        "response_style": "prognosis_focused",
        "instructions": "Provide general outlook in 2-3 sentences. Avoid overly detailed statistics."
    },
    
    QuestionType.COMPARISON: {
        "keywords": ["difference between", "vs", "compared to", "better than"],
        "examples": ["Difference between Type 1 and Type 2 diabetes", "MRI vs CT scan"],
        "response_style": "comparative",
        "instructions": "Create a clear comparison focusing on 2-3 key differences. Use table structure."
    },

    QuestionType.YES_NO: {
        "keywords": ["is", "can", "does", "will", "should"],
        "examples": ["Is diabetes hereditary?", "Can stress cause heart disease?"],
        "response_style": "direct_answer",
        "instructions": "Start with Yes/No, then provide 1-2 sentences of explanation."
    },

    QuestionType.GENERAL: {
        "keywords": ["general", "information", "about", "overview"],
        "examples": ["General information about diabetes", "Overview of heart disease"],
        "response_style": "general_overview",
        "instructions": "Provide a broad overview in 3-4 sentences. Focus on key aspects."
    },
}

def get_question_type(question: str) -> QuestionType:
    """
    Determine the type of question based on keywords.
    """
    for qtype, info in QUESTION_DESCRIPTION.items():
        if any(keyword in question.lower() for keyword in info["keywords"]):
            return qtype
    return QuestionType.EXPLANATION  # Default to explanation if no specific type found