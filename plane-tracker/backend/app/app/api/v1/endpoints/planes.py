from typing import Annotated
from fastapi import APIRouter, Query
from asyncer import asyncify, create_task_group, syncify
from app.core.config import settings
import httpx
from app.schemas.response_schema import IGetResponseBase, create_response

router = APIRouter()