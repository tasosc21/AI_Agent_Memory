def read():
    while True:
        user_input = input("User: ")
        if user_input:
            break

    return user_input

def write(response):
    print(f"AI: {response}")