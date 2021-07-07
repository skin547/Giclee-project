from pydantic import BaseModel

class BlendImage(BaseModel):
    name: str
    convert_to: str
    shift_x: int
    shift_y: int
    base64image : str