from fastapi import APIRouter,Depends
import httpx
from app.schemas.response_schema import IGetResponseBase, create_response
from app.schemas.vector_schema import VectorRequest
from app.core.dependencies.osky_service_dependencies import OskyServiceDep
router = APIRouter()

@router.get("/vectors")
def get_vectors_for_plane() -> IGetResponseBase:
    return create_response(data={"vectors": []}, message="Vectors retrieved successfully")

@router.get("/vectors/area")
async def get_vectors_in_area(osky_service: OskyServiceDep, vector_request: VectorRequest = Depends()) -> IGetResponseBase:
    model_dic=vector_request.model_dump()
    vector_tuple=tuple(model_dic.values())
    response =await osky_service.get_state_vectors_area(bbox=vector_tuple)
    
    return create_response(data=response, message="Vectors in area retrieved successfully")


