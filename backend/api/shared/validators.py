from fastapi import HTTPException

def validate_terms(accept_terms: bool, accept_privacy_policy: bool):
    if not accept_terms or not accept_privacy_policy:
        raise HTTPException(status_code=400, detail="You must accept the terms and privacy policy to register.")
