from enum import Enum

class QuestionType(str, Enum):
    """
    Simplified medical question classification into 4 main categories
    covering the complete patient journey and information needs
    """
    GENERAL_INFO = "GENERAL_INFO"      # What, definitions, basic information
    MEDICAL_GUIDANCE = "MEDICAL_GUIDANCE"  # Symptoms, diagnosis, assessment
    CARE_MANAGEMENT = "CARE_MANAGEMENT"    # Treatment, prevention, lifestyle
    SPECIFIC_INQUIRY = "SPECIFIC_INQUIRY"  # Yes/no, comparisons, specific details

QUESTION_DESCRIPTION = {
    QuestionType.GENERAL_INFO: {
        "keywords": [
            "what is", "what are", "define", "definition of", "meaning of", 
            "general", "information", "about", "overview", "explain", 
            "how does", "why does", "describe", "tell me about", "causes"
        ],
        "examples": [
            "What is diabetes?", "What are the symptoms of asthma?", 
            "Explain how insulin works", "What causes heart disease?",
            "Tell me about cancer", "How does the immune system work?"
        ],
        "response_style": "comprehensive_overview",
        "instructions": """Provide a comprehensive yet accessible overview covering:
1. Clear definition in simple terms
2. Key characteristics or symptoms (if applicable)
3. Primary causes or mechanisms
4. Essential context for understanding
Keep response focused but informative (4-6 sentences). Use medical terminology with explanations.

**Follow-up Questions**: If the topic is broad or could benefit from more specific information, ask:
- "Would you like to know more about [specific aspect]?"
- "Are you interested in learning about the symptoms, causes, or treatment options?"
- "Is there a particular aspect of [condition] you'd like me to explain further?"
- "Would you like information about how this affects [specific population/age group]?"

Example: "Would you like to know more about the different types of diabetes or how it's diagnosed?"
"""
    },

    QuestionType.MEDICAL_GUIDANCE: {
        "keywords": [
            "symptoms", "i have", "experiencing", "feeling", "pain", 
            "what disease", "what condition", "diagnosis", "when to see",
            "should i worry", "is this normal", "could this be", "risk factors",
            "who is at risk", "chances of", "likelihood", "genetic"
        ],
        "examples": [
            "I have chest pain and shortness of breath", 
            "What disease causes these symptoms?", "Who is at risk for stroke?",
            "Should I worry about this headache?", "Is diabetes hereditary?",
            "When should I see a doctor for fever?"
        ],
        "response_style": "guidance_focused",
        "instructions": """Provide medical guidance with emphasis on safety:
1. Address the specific concern or symptom pattern
2. List 2-3 most relevant possibilities or risk factors
3. Include clear guidance on when to seek medical care
4. Always emphasize professional medical consultation for symptoms
Balance being informative while encouraging appropriate medical care.

**Follow-up Questions**: To gather more context for better guidance, ask:
- "How long have you been experiencing these symptoms?"
- "Are there any other symptoms you've noticed?"
- "Do you have any family history of [relevant condition]?"
- "Are you currently taking any medications?"
- "Have you seen a healthcare provider about this concern?"
- "Would you like information about what to expect during a medical consultation?"

Example: "How long have you been experiencing these symptoms? This information can help determine the urgency of seeking medical care."
"""
    },

    QuestionType.CARE_MANAGEMENT: {
        "keywords": [
            "how to treat", "treatment for", "cure for", "therapy", "medication",
            "how to prevent", "avoid", "reduce risk", "prevention of",
            "manage", "control", "lifestyle", "diet", "exercise", "recovery",
            "prognosis", "outlook", "healing", "rehabilitation"
        ],
        "examples": [
            "How to treat high blood pressure?", "Ways to prevent heart disease?",
            "What medications are used for depression?", "How to manage diabetes?",
            "Recovery time after surgery", "Lifestyle changes for arthritis"
        ],
        "response_style": "actionable_care",
        "instructions": """Provide practical care management information:
1. Primary treatment or prevention strategies (3-4 key approaches)
2. Lifestyle modifications when applicable
3. Expected outcomes or timeline if relevant
4. Emphasize working with healthcare providers for personalized plans
Focus on evidence-based, actionable guidance while noting individual variation.

**Follow-up Questions**: To provide more personalized guidance, ask:
- "Are you looking for information about [specific treatment type] or general management?"
- "Would you like to know about lifestyle changes, medications, or both?"
- "Are you interested in prevention strategies or managing an existing condition?"
- "Do you have any specific concerns about treatment options?"
- "Would you like information about what to discuss with your healthcare provider?"
- "Are there any particular challenges you're facing with current management?"

Example: "Are you looking for dietary recommendations, exercise guidelines, or medication information for managing diabetes?"
"""
    },

    QuestionType.SPECIFIC_INQUIRY: {
        "keywords": [
            "is", "can", "does", "will", "should", "difference between", 
            "vs", "compared to", "better than", "which", "how long",
            "how much", "how many people", "prevalence", "statistics",
            "inheritance", "hereditary", "genetic testing", "side effects"
        ],
        "examples": [
            "Is diabetes hereditary?", "Can stress cause heart disease?",
            "Difference between Type 1 and Type 2 diabetes", "MRI vs CT scan",
            "How many people are affected by this condition?", 
            "Which treatment is better?", "What are the side effects?"
        ],
        "response_style": "direct_specific",
        "instructions": """Provide direct, specific answers:
1. Start with a clear, direct response to the specific question
2. Provide 2-3 key supporting details or distinctions
3. Include relevant statistics or facts when applicable
4. For comparisons, highlight the most important differences
Keep responses concise but complete, focusing on the exact information requested.

**Follow-up Questions**: To explore related topics or clarify, ask:
- "Would you like more details about [specific aspect mentioned]?"
- "Are you interested in learning about the implications of this information?"
- "Do you have questions about how this applies to your specific situation?"
- "Would you like to know about related topics or conditions?"
- "Is there a particular reason you're asking about this?"
- "Would additional comparisons or examples be helpful?"

Example: "Is diabetes hereditary? Yes, genetics play a role in both Type 1 and Type 2 diabetes... Would you like to know about specific risk factors or genetic testing options?"
"""
    }
}