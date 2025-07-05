from typing import NewType
import base64

DataFile = NewType('DataFile', list[bytes]) 

class Base64Str(str):
    def __new__(self, raw: bytes | str):
        if isinstance(raw, str):
            raw = raw.encode()

        raw = base64.b64encode(raw).decode()
        return super().__new__(self, raw)
    
    @classmethod
    def from_string(cls, text: str):
        raw_bytes = base64.b64decode(text)
        return cls(raw_bytes)

    def decode(self) -> bytes:
        return base64.b64decode(self) 
    