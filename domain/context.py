class Context:

    def __init__(self) -> None:
        self.per_user: dict = {}
        self.current_context: list = []