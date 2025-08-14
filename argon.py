from argon2 import PasswordHasher

ph = PasswordHasher()
print(ph.hash(input("Password ADMIN (non verrà salvata): ")))
