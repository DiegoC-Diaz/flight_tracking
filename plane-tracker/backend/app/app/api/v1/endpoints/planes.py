from typing import Annotated
from fastapi import APIRouter, Query,Depends
from asyncer import asyncify, create_task_group, syncify
from app.core.config import settings
import httpx
from app.schemas.response_schema import IGetResponseBase, create_response
from app.schemas.vector_schema import VectorRequest
from app.core.dependencies.osky_service_dependencies import OskyServiceDep
router = APIRouter()

@router.get("/vectors")
def get_vectors_for_plane() -> IGetResponseBase:
    return create_response(data={"vectors": []}, message="Vectors retrieved successfully")

@router.get("/vectors/area")
def get_vectors_in_area(osky_service: OskyServiceDep, vector_request: VectorRequest = Depends()) -> IGetResponseBase:
    
    osky_service.get_state_vectors_area(vector_request.model_dump())
    
    return create_response(data=vector_request.model_dump(), message="Vectors in area retrieved successfully")


