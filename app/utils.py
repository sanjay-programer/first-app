from passlib.context import CryptContext
pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash(password):
    return  pwd_context.hash(password)

def password_verifying(PlainPassword,HashPassword):
    return pwd_context.verify(PlainPassword,HashPassword)

