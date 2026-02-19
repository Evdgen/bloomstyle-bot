from .start import router as start_router
from .bloom import router as bloom_router
from .style import router as style_router
from .knowledge import router as knowledge_router
from .settings import router as settings_router
from .premium_commands import router as premium_router
from .payments import router as payments_router
from .crypto_payments import router as crypto_router
from .horoscope import router as horoscope_router
from .mystery_box import router as mystery_box_router
from .habit_tracker import router as habit_tracker_router
from .prank import router as prank_router

__all__ = [
    'start_router',
    'bloom_router',
    'style_router',
    'knowledge_router',
    'settings_router',
    'premium_router',
    'payments_router',
    'crypto_router',
    'horoscope_router',
    'mystery_box_router',
    'habit_tracker_router',
    'prank_router'
]