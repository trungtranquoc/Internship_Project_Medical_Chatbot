question_classification_prompt = """### Medical Question Classification System:

Classify medical questions into 4 main categories based on the type of information being sought:

## 1. **GENERAL_INFO** - Educational and informational questions
   - **Purpose**: Understanding medical concepts, conditions, or processes
   - **Keywords**: "what is", "what are", "define", "definition", "meaning", "general", "information", "about", "overview", "explain", "how does", "why does", "describe", "tell me about", "causes"
   - **Examples**: 
     - "What is diabetes?"
     - "Explain how insulin works"
     - "What causes heart disease?"
     - "Tell me about cancer symptoms"

## 2. **MEDICAL_GUIDANCE** - Symptom assessment and health guidance
   - **Purpose**: Seeking guidance about symptoms, risk factors, or health concerns
   - **Keywords**: "symptoms", "i have", "experiencing", "feeling", "pain", "what disease", "what condition", "diagnosis", "when to see", "should i worry", "is this normal", "could this be", "risk factors", "who is at risk", "chances of", "likelihood", "genetic"
   - **Examples**:
     - "I have chest pain and shortness of breath"
     - "What disease causes these symptoms?"
     - "Who is at risk for stroke?"
     - "Should I worry about this headache?"

## 3. **CARE_MANAGEMENT** - Treatment, prevention, and management
   - **Purpose**: Information about treatment options, prevention strategies, and health management
   - **Keywords**: "how to treat", "treatment for", "cure for", "therapy", "medication", "how to prevent", "avoid", "reduce risk", "prevention", "manage", "control", "lifestyle", "diet", "exercise", "recovery", "prognosis", "outlook", "healing", "rehabilitation"
   - **Examples**:
     - "How to treat high blood pressure?"
     - "Ways to prevent heart disease?"
     - "How to manage diabetes?"
     - "Recovery time after surgery?"

## 4. **SPECIFIC_INQUIRY** - Direct questions requiring specific answers
   - **Purpose**: Specific facts, comparisons, statistics, or yes/no questions
   - **Keywords**: "is", "can", "does", "will", "should", "difference between", "vs", "compared to", "better than", "which", "how long", "how much", "how many people", "prevalence", "statistics", "inheritance", "hereditary", "genetic testing", "side effects"
   - **Examples**:
     - "Is diabetes hereditary?"
     - "Can stress cause heart disease?"
     - "Difference between Type 1 and Type 2 diabetes"
     - "How many people are affected by this condition?"

### Classification Instructions:
1. Read the question carefully and identify the primary intent
2. Match keywords and question structure to the most appropriate category
3. Consider what type of response the user is seeking
4. If the question spans multiple categories, choose the PRIMARY intent
5. Return ONLY the category name: "GENERAL_INFO", "MEDICAL_GUIDANCE", "CARE_MANAGEMENT", or "SPECIFIC_INQUIRY"

**Question to classify**: {question}

**Classification**:"""