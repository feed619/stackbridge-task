from fastapi import HTTPException, status

TokenAdminException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Your doesn't have permissions",
    headers={"WWW-Authenticate": "Bearer"},
)

NotAuthenticatedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)

IncorrectUserDataException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Bearer"},
)
UserDeactivateException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Your account is deactivated",
    headers={"WWW-Authenticate": "Bearer"},
)
