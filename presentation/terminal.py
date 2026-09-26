def start() -> None:
    print()
    print("Starting application...")
    print()

def exit() -> None:
    print()
    print("Exiting application...")
    print()

def read() -> str:
    while True:
        user_input = input("User: ")
        if user_input:
            break

    return user_input

def write(response: str) -> None:
    print(f"AI: {response}")
    print()

def change_user(username: str, message: str) -> tuple[str, str]:
    print(f"User has been changed successfully. Current User: {username}\n")
    return username, message
