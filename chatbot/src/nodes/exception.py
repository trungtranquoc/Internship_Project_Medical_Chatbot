from ..utils import QuestionType


class GraphNodeException(Exception):
    """Base exception for graph node errors."""
    pass

class LanguageDetectionError(GraphNodeException):
    """Custom exception for language detection errors."""
    def __init__(self):
        super().__init__("Error occurred while detecting the language of the question. Only Vietnamese and English are supported.")

class QuestionClassificationError(GraphNodeException):
    """Custom exception for question classification errors."""
    def __init__(self):
        super().__init__(f"System unsupported this kind of question type. Only support {', '.join([q_type.value for q_type in QuestionType])}.")

class InsufficientInformationError(GraphNodeException):
    """Custom exception for insufficient information errors."""
    def __init__(self):
        super().__init__("Can not find any context or documents related to the question.")