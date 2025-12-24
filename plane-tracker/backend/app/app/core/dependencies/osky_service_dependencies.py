from typing import Annotated
from fastapi import Depends
from app.services.osky_service import OskyService

def provide_osky_service()->OskyService:
    return OskyService()

OskyServiceDep=Annotated[OskyService,Depends(provide_osky_service)]