"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model corresponds to a MongoDB collection where the
collection name is the lowercase of the class name.

Examples:
- Project -> "project"
- Skill -> "skill"
- Message -> "message"
"""

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# ---------- Portfolio Collections ----------

class Project(BaseModel):
    """Projects to showcase in the portfolio."""
    title: str = Field(..., min_length=2, max_length=120)
    description: str = Field(..., min_length=4, max_length=500)
    tech: List[str] = Field(default_factory=list, description="List of technologies used")
    liveLink: Optional[str] = Field(default=None, description="URL for the live demo")
    githubLink: Optional[str] = Field(default=None, description="URL for the source code repo")
    image: Optional[str] = Field(default=None, description="Cover image URL")

class Skill(BaseModel):
    """Skills with a simple percentage level for progress bars."""
    name: str = Field(..., min_length=1, max_length=60)
    level: int = Field(..., ge=0, le=100, description="Proficiency percentage 0-100")

class Message(BaseModel):
    """Contact form messages submitted by visitors."""
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    message: str = Field(..., min_length=5, max_length=2000)

# Additional collections (Education, Certificates) can be added later if needed.
