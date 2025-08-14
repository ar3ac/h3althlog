from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Istanza CSRF (il token nei form funziona quando la colleghiamo all'app)
csrf = CSRFProtect()

# Istanza Limiter (conta i tentativi per IP; storage in memoria per dev)
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
