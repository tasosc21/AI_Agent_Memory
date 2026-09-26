from presentation import terminal


def test_start(capsys):
    terminal.start()

    captured = capsys.readouterr()

    assert "Starting application..." in captured.out


def test_exit(capsys):
    terminal.exit()

    captured = capsys.readouterr()

    assert "Exiting application..." in captured.out


def test_read(monkeypatch):
    inputs = iter(["", "", "hello"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    result = terminal.read()

    assert result == "hello"


def test_write(capsys):
    terminal.write("Hello there!")

    captured = capsys.readouterr()

    assert "AI: Hello there!" in captured.out


def test_change_user_with_message(capsys):
    result = terminal.change_user("Jane", "Hello")

    captured = capsys.readouterr()

    assert result == ("Jane", "Hello")
    assert "Current User: Jane" in captured.out


def test_change_user_without_message(capsys):
    result = terminal.change_user("Jane", "")

    captured = capsys.readouterr()

    assert result == ("Jane", "")
    assert "Current User: Jane" in captured.out