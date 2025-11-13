from fastapi import APIRouter, Request, Depends
from service_locator import get_locator, ServiceLocator

from controllers.advert_controller import AdvertController
from controllers.main_controller import MainController
from controllers.user_controller import UserController
from controllers.deals_controller import DealsController
from controllers.likes_controller import LikesController

advert_router = APIRouter()
main_router = APIRouter()
user_router = APIRouter()
deals_router = APIRouter()
likes_router = APIRouter()

# Advert routes
@advert_router.get("/profile/create_advert")
async def create_advert_form(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = AdvertController(locator)
    return await controller.create_advert_form(request)

@advert_router.post("/profile/create_advert")
async def create_advert(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = AdvertController(locator)
    return await controller.create_advert(request)

# Main routes
@main_router.get("/")
async def index(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = MainController(locator)
    return await controller.index(request)

@main_router.get("/category/{category_id}")
async def adverts_by_category(
    request: Request,
    category_id: int,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = MainController(locator)
    return await controller.adverts_by_category(request, category_id)

@main_router.get("/search")
async def search_adverts(
    request: Request,
    q: str,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = MainController(locator)
    return await controller.search_adverts(request, q)

@main_router.get("/profile")
async def profile_page(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = MainController(locator)
    return await controller.profile_page(request)

# User routes
@user_router.get("/login")
async def login_page(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = UserController(locator)
    return await controller.login_page(request)

@user_router.post("/login")
async def login(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = UserController(locator)
    return await controller.login(request)

@user_router.get("/register")
async def register_page(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = UserController(locator)
    return await controller.register_page(request)

@user_router.post("/register")
async def register(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = UserController(locator)
    return await controller.register(request)

@user_router.get("/logout")
async def logout(
    request: Request,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = UserController(locator)
    return await controller.logout(request)

# Deals routes
@deals_router.post("/deal_create/{item_id}")
async def create_deal(
    request: Request,
    item_id: int,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = DealsController(locator)
    return await controller.create_deal(request, item_id)

# Likes routes
@likes_router.post("/like/{item_id}")
async def add_like(
    request: Request,
    item_id: int,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = LikesController(locator)
    return await controller.add_like(request, item_id)

@likes_router.post("/unlike/{item_id}")
async def remove_like(
    request: Request,
    item_id: int,
    locator: ServiceLocator = Depends(get_locator)
):
    controller = LikesController(locator)
    return await controller.remove_like(request, item_id)