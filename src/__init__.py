from aiogram import Router

from handlers.start_menu import router as start_menu_router
from handlers.food_analysis import router as food_analysis_router
from handlers.purpose import router as purpose_menu_router
from handlers.support import router as support_router
from handlers.kbzhu import router as kbzhu_menu_router

main_router = Router()

main_router.include_router(start_menu_router)
main_router.include_router(purpose_menu_router)
main_router.include_router(support_router)
main_router.include_router(kbzhu_menu_router)
main_router.include_router(food_analysis_router)
