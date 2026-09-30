from aiogram import Router

from handlers.start_menu import router as start_menu_router
from handlers.food_analysis import router as food_analysis_router
from handlers.other_menu import router as other_menu_router

main_router = Router()

main_router.include_router(start_menu_router)
main_router.include_router(other_menu_router)
main_router.include_router(food_analysis_router)
