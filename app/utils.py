from passlib.context import CryptContext
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_hash(password):
    return pwd_context.hash(password)

def validate(user_pass, password):
    return pwd_context.verify(user_pass, password)

def convert_post_to_dict(post, votes):
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "created_at": post.created_at,
        "user_id": post.user_id,
        "owner": {
            "id": post.owner.id,
            "email": post.owner.email,
            # Add other fields from the User model as needed
        },
        "votes": votes
    }

# used for sending image data as a response
def convert_bytes_to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8') if data else None
