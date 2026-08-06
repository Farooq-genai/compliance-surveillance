from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class Attachement(BaseModel):
    file_name = Field()