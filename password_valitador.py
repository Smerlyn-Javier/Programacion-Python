def validar_password(password: str):
    """
    Valida una password según los siguientes criterios:
      a) Mínimo de 8 caracteres.
      b) Contiene letras minúsculas, mayúsculas, números y al menos 1 carácter no alfanumérico.
      c) No contiene espacios en blanco.
      d) Si es válida, retorna True.
      e) Si no es válida, retorna un mensaje de error.
    
    :param password: str: La contraseña a validar.
    :return: True si la contraseña es válida, en caso contrario un mensaje de error.
    """
    tiene_minuscula = any('a' <= char <= 'z' for char in password) 
    # En ASCII 'a' tiene un valor de 97 y 'z' tiene un valor de 122. 'a' <= a <= 'z' // 97 <= 97 <= 122
    
    tiene_mayuscula = any('A' <= char <= 'Z' for char in password) 
    # En ASCII 'A' tiene un valor de 65 y 'Z' tiene un valor de 90. 'A' <= A <= 'Z' // 65 <= 90 <= 90
    
    tiene_numero = any('0' <= char <= '9' for char in password)
    tiene_especial = any(not char.isalnum() for char in password)
    tiene_espacios = any(char.isspace() for char in password)

    if len(password) < 8:
        return "❌ La contraseña elegida no es segura: debe tener al menos 8 caracteres. 🩳"

    if not tiene_minuscula:
        return "❌ La contraseña elegida no es segura: debe incluir al menos una letra minúscula. 🔡"

    if not tiene_mayuscula:
        return "❌ La contraseña elegida no es segura: debe incluir al menos una letra mayúscula. 🔠"

    if not tiene_numero:
        return "❌ La contraseña elegida no es segura: debe incluir al menos un número. 🔢"

    if not tiene_especial:
        return "❌ La contraseña elegida no es segura: debe incluir al menos un carácter no alfanumérico. 🈳"

    if tiene_espacios:
        return "❌ La contraseña elegida no es segura: no puede contener espacios en blanco. 👨‍🚀"

    return True


# Loop hasta que la cotraseña sea valida ✅
while True:
    password = input("Por favor ingrese una contraseña: ")
    result = validar_password(password)
    if result == True:
        print(f"✅ '{password}': La contraseña es válida. 👍")
        break
    else:
        print(result)
        
        
        
# Ejemplo de uso Test 🪲
if __name__ == "__main__":
    print("🪲 Test ::")
    ejemplos = [
        "Hola123!",       # Contraseña válida
        "short!",         # Muy corta
        "solominusculas1!",  # Sin mayúsculas
        "SOLOMAYUSCULAS1!",  # Sin minúsculas
        "NoSpecialChar1",   # Sin caracteres especiales
        "Tiene Espacio1!",  # Con espacios
    ]

    for password in ejemplos:
        resultado = validar_password(password)
        if resultado is True:
            print(f"✅'{password}': La contraseña es válida. 👍")
        else:
            print(f"'{password}': {resultado}")        