
def answer_format(response, source):
    """
    Format the response and source information into a structured answer.
    
    Args:
        response (str): The main response text.
        source (list): List of source dictionaries containing file_name and year.
    
    Returns:
        str: Formatted answer string.
    """
    related_questions_text = '\n'.join(source)

    answer = f"""
    {response}

---

### 🗂️ Related questions:
{related_questions_text}
    """
    
    return answer  # Remove any leading/trailing whitespace