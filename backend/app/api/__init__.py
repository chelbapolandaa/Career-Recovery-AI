# Export routers
from .applications import router as applications_router
from .analysis import router as analysis_router  # ← TAMBAH INI

__all__ = ["applications_router", "analysis_router"]  # ← TAMBAH