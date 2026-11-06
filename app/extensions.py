"""
extensions.py
Instâncias compartilhadas das extensões Flask.
Inicializadas aqui para evitar importações circulares.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
