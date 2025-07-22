class Metadata:
    def __init__(self, file_name: str, directory: str, year: int):
        self.file_name = file_name
        self.directory = directory
        self.year = year

    def __str__(self):
        return f"{self.file_name} --- Thư mục: {self.directory} --- Năm {self.year}"
    
    def __hash__(self):
        return hash(self.file_name)  # Only hash based on 'id'

    def __eq__(self, other):
        return isinstance(other, Metadata) and self.file_name == other.file_name  # Only compare by 'id'