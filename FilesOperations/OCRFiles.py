from markitdown import MarkItDown


class OCRFiles():
    def __init__(self):

        self.md = MarkItDown()

    def ocr(self, path_to_file):
        result = self.md.convert(path_to_file)
        contentDocument = result.text_content

        return contentDocument
    
    def loopFilesAndOcr(self, arrayFiles):
        fileAndContent = {}
        for file in arrayFiles:
            content = self.ocr(file)
            fileAndContent[file] = content

        return fileAndContent
