language_detection_prompt = """
    Detect the language of the following question. Only output "Vietnamese", "English" or "Unsupported" if the language is neither Vietnamese nor English.
    
    ## Advanced Instructions:
    - If the question contains full Vietnamese characters or English characters, classify it as "Vietnamese" or "English" respectively.
    - Some of the Proper Noun or Nouns may be used in different languages, classify it as the language that is more prevalent in the question.
    - If the question contains too much language that is either not Vietnamese or English, classify it as "Unsupported".
    
    Question: {question}
"""

language_reponse_guidelines = {
    "vietnamese": """
        - Write in clear, natural, and understandable Vietnamese. 
        - Always include English reference name in parenthesis when first mentioned about medical terms in the answer. For example: "Bệnh tiểu đường (Diabetes) là ..., " hay "Cảm cúm (Flu) có các triệu chứng ...". Use appropriate medical terminology while ensuring clarity.
        - For those very specific medical terms that are not commonly used in Vietnamese, use the English term directly. For example: name of bacteria.
    """,
    "english": """
        Write in clear, natural, and understandable English.
    """
}