import uuid

class Line:
    def __init__(self, text: str):
        self._name = str(uuid.uuid4().hex)

        start = text.find("|")
        self._text = text[start:]
        self._meta = text[:start]
        
        if self._meta[0].lower() == "l" or self._meta[0].lower() == "r":
            self._octave = self._meta[1:]
        else:
            self._octave = self._meta

    def name(self) -> str:
        return self._name

    def octave(self) -> str:
        return self._octave

    def char(self, index: int) -> str:
        return self._text[index]

    def text(self) -> str:
        return self._text

    def __str__(self) -> str:
        return self._meta + self._text
