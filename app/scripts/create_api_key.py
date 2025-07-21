from app.models.api_keys_record import APIKey
from app.database import sessionlocal

def create_api_key(role, owner_email):
    session = sessionlocal()
    
    new_key = APIKey(
        role = role,
        owner_email = owner_email
    )

    session.add(new_key)
    session.commit()
    if owner_email == "hussein@admin.com":
        print("API Key created:", new_key.key)
    
    session.close()


