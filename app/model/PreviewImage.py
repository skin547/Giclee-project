from pydantic import BaseModel

class PreviewImage(BaseModel):
    name: str
    convert_to: str
    base64image: str
