from fastapi import APIRouter, Depends
from app.schemas.response_schema import IGetResponseBase, create_response
from app.schemas.vector_schema import VectorRequest
from app.core.dependencies.osky_service_dependencies import OskyServiceDep
from app.utils.mappers.vector_mapper import map_vector_from_osky

router = APIRouter()

@router.get("/vectors")
def get_vectors_for_plane() -> IGetResponseBase:
    return create_response(data=[], message="Vectors retrieved successfully")

@router.get("/vectors/area")
async def get_vectors_in_area(osky_service: OskyServiceDep, vector_request: VectorRequest = Depends()) -> IGetResponseBase:
    # The service expects a tuple: (lomin, lamin, lomax, lamax)
    bbox = (
        vector_request.lomin,
        vector_request.lamin,
        vector_request.lomax,
        vector_request.lamax,
    )
    osky_data = await osky_service.get_state_vectors_area(bbox=bbox)
    mapped_data = map_vector_from_osky(osky_data)
    return create_response(data=mapped_data.model_dump(), message="Vectors in area retrieved successfully")


@router.get("/planes/vector{icao}")
async def get_vector_for_plane(icao: str, osky_service: OskyServiceDep) -> IGetResponseBase:
    response=osky_service.get_state_vector_from_flight(icao)
    return create_response(data=response, message="Vector retrieved successfully")