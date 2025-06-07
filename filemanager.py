class FileManager:
    def __init__(self):
        self.files = {}
    def new_file(self, name, content=""):
        if name in self.files:
            raise ValueError(f"File '{name}' already exists.")
        self.files[name] = content
    def get_file(self, name):
        if name not in self.files:
            raise ValueError(f"File '{name}' does not exist.")
        return self.files[name]
    def delete_file(self, name):
        if name not in self.files:
            raise ValueError(f"File '{name}' does not exist.")
        del self.files[name]
    def list_files(self):
        return list(self.files.keys())
