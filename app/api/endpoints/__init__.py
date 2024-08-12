# app/api/endpoints/__init__.py
from .user import router as user_router
from .rooms import router as rooms_router
from  .devices import router as devices_router
from  .stats import router as stats_router