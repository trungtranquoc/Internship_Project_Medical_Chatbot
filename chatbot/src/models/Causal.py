from openai import OpenAI
from pydantic import BaseModel
from ..utils import QuestionType, QUESTION_DESCRIPTION, classify_question

class QuestionDescription(BaseModel):
    question_type: QuestionType

class CausalModel:
    def __init__(self, model_name: str, api_key, system_prompt):
        self.model_name = model_name
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

        self.system_prompt = system_prompt

    def generate_response(self, prompt: str, history: list) -> str:
        msgs = [{"role": "system", "content": self.system_prompt}]
        msgs.extend(history)
        msgs.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=msgs,
            temperature=0.2,
            max_tokens=1000,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        output = response.choices[0].message.content if response.choices[0].message.content else ""

        return output
    
    def classify_question(self, question: str) -> QuestionType:
        """
        Classify the question type based on the provided question.
        Returns the QuestionType enum.
        """
        try:
            # Generate the classification prompt
            classification_prompt = classify_question(question)
            
            # Use structured output with Pydantic model
            response = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a medical question classifier. Classify the given question into one of the predefined categories."},
                    {"role": "user", "content": classification_prompt}
                ],
                response_format=QuestionDescription,
                temperature=0.1,  # Low temperature for consistent classification
                max_tokens=50
            )
            
            # Extract the question type from the response
            question_description = response.choices[0].message.parsed
            return question_description.question_type
            
        except Exception as e:
            print(f"Error in question classification: {e}")
            # Default fallback to EXPLANATION if classification fails
            return QuestionType.EXPLANATION