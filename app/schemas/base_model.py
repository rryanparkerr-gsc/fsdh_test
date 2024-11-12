# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-07-07
"""

from pydantic import BaseModel


class BaseModelConfig(BaseModel):
    class Config:
        orm_mode = True
