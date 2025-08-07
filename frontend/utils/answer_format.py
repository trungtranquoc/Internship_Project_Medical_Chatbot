
def answer_format(response, keywords):
    """
    Format the response and source information into a structured answer.
    
    Args:
        response (str): The main response text.
        source (list): List of source dictionaries containing file_name and year.
    
    Returns:
        str: Formatted answer string.
    """
    answer = f"""
    {response}

---

🗂️ **Related medical status:** {'; '.join(keywords)}
    """
    
    return answer  # Remove any leading/trailing whitespace