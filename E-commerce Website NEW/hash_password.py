import bcrypt

password = "password123"  # Change this to your desired password
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print("Hashed Password:", hashed_password)