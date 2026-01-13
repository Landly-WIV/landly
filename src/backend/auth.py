# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from typing import Optional
# from src.backend import models, schemas, crud

# # ========================
# # PASSWORT-HASHING
# # ========================

# # Passlib Context für bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     """
#     Hasht ein Klartext-Passwort mit bcrypt.
    
#     Args:
#         password: Klartext-Passwort
    
#     Returns:
#         Gehashtes Passwort
#     """
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Vergleicht Klartext-Passwort mit gehashtem Passwort.
    
#     Args:
#         plain_password: Eingegebenes Passwort
#         hashed_password: Gespeicherter Hash aus DB
    
#     Returns:
#         True wenn Passwort korrekt, sonst False
#     """
#     return pwd_context.verify(plain_password, hashed_password)


# # ========================
# # REGISTRIERUNG
# # ========================

# def register_user(
#     db: Session,
#     email: str,
#     password: str,
#     rolle: str = "kunde",
#     kunde_id: Optional[int] = None,
#     bauer_id: Optional[int] = None
# ) -> models.User:
#     """
#     Registriert einen neuen User.
    
#     Args:
#         db: Database Session
#         email: Email des Users
#         password: Klartext-Passwort (wird gehasht)
#         rolle: Rolle des Users ("kunde", "bauer", "admin")
#         kunde_id: Optional - Verknüpfung zu Kunde
#         bauer_id: Optional - Verknüpfung zu Bauer
    
#     Returns:
#         Erstellter User
    
#     Raises:
#         ValueError: Wenn Email bereits existiert
#     """
#     # Prüfe ob Email bereits existiert
#     existing_user = crud.get_user_by_email(db, email=email)
#     if existing_user:
#         raise ValueError("Email bereits registriert")
    
#     # Hash Passwort
#     hashed_password = hash_password(password)
    
#     # Erstelle User-Schema mit gehashtem Passwort
#     user_data = schemas.UserCreate(
#         email=email,
#         passwort=hashed_password,  # Bereits gehasht!
#         rolle=rolle,
#         kunde_id=kunde_id,
#         bauer_id=bauer_id
#     )
    
#     # Speichere in DB
#     return crud.create_user(db, user=user_data)


# # ========================
# # LOGIN
# # ========================

# def login_user(db: Session, email: str, password: str) -> Optional[models.User]:
#     """
#     Authentifiziert einen User (Login).
    
#     Args:
#         db: Database Session
#         email: Email des Users
#         password: Klartext-Passwort
    
#     Returns:
#         User-Objekt wenn Login erfolgreich, sonst None
#     """
#     # Hole User aus DB
#     user = crud.get_user_by_email(db, email=email)
    
#     if not user:
#         return None  # User nicht gefunden
    
#     # Prüfe ob User aktiv
#     if user.aktiv != 1:
#         return None  # User deaktiviert
    
#     # Prüfe Passwort
#     if not verify_password(password, user.passwort_hash):
#         return None  # Falsches Passwort
    
#     return user  # Login erfolgreich


# def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
#     """
#     Alias für login_user() - authentifiziert einen User.
#     """
#     return login_user(db, email=email, password=password)


# # ========================
# # PASSWORT ÄNDERN
# # ========================

# def change_password(
#     db: Session,
#     user_id: int,
#     old_password: str,
#     new_password: str
# ) -> bool:
#     """
#     Ändert das Passwort eines Users.
    
#     Args:
#         db: Database Session
#         user_id: ID des Users
#         old_password: Altes Passwort (zur Verifizierung)
#         new_password: Neues Passwort
    
#     Returns:
#         True wenn erfolgreich, False wenn altes Passwort falsch
#     """
#     user = crud.get_user(db, user_id=user_id)
    
#     if not user:
#         return False
    
#     # Prüfe altes Passwort
#     if not verify_password(old_password, user.passwort_hash):
#         return False
    
#     # Hashe neues Passwort
#     new_hash = hash_password(new_password)
    
#     # Update User
#     crud.update_user(db, user_id=user_id, user_data={"passwort_hash": new_hash})
    
#     return True


# ========================
# OPTIONALE FUNKTIONEN
# ========================

# Für JWT-Token (falls später benötigt):
# from datetime import datetime, timedelta
# from jose import JWTError, jwt

# SECRET_KEY = "dein-geheimer-schlüssel"  # In .env auslagern!
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     """JWT Access Token erstellen"""
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
