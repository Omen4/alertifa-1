from fastapi import APIRouter

from . import channels, authentication, permissions, messages, users

router = APIRouter()
router.include_router(channels.router, tags=["channels"], prefix="/channels")
router.include_router(authentication.router, tags=["authentication"], prefix="/auth")
router.include_router(permissions.router, tags=["permissions"], prefix="/permissions")
router.include_router(messages.router, tags=["messages"], prefix="/messages")
router.include_router(users.router, tags=["users"], prefix="/users")

# from fastapi import APIRouter, Depends
# from app.Http.Controllers.TestController import TestController
# from app.Providers.HTTPHeaderAuthProvider import HTTPHeaderAuthentication

# PROTECTED = Depends(HTTPHeaderAuthentication(scopes=['valid_role']))
# router = APIRouter()
# router.add_api_route(methods=['GET'], path='/', endpoint=TestController.home, name="Home", dependencies=[])
# router.add_api_route(methods=['GET'], path='/profile/{authuser}', endpoint=TestController.profile, name="Profile", dependencies=[PROTECTED])