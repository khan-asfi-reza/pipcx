import os
import shutil
from pathlib import Path

import pytest

from pipcx.commands.init import Command as InitCommand
from pipcx.main import CLI
from test.utils import make_multiple_inputs, safe_remove_dir, safe_remove_file


@pytest.fixture
def init_command():
    return InitCommand()


@pytest.fixture
def path():
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    return path


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    safe_remove_dir("testproject")
    safe_remove_dir("testvenv")
    safe_remove_file("pipcx.yaml")
    safe_remove_file("pytest.yaml")


def test_init_with_option_args(init_command, path, monkeypatch):
    # Set input parameter
    monkeypatch.setattr("builtins.input", make_multiple_inputs(
        ["testproject", "mit", "author", "name@name.com"]))
    # Run the command
    init_command.run(["pipcx", "init", "--venv=testvenv"])
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("testproject/main.py")
    # Remove test files
    shutil.rmtree(path / 'testvenv')
    shutil.rmtree(path / 'testproject')
    os.remove("pipcx.yaml")


def test_init_with_predefined_files(path, init_command, monkeypatch):
    cli = CLI(["pipcx", "init", "testproject", "--venv=testvenv", "--no-input"])
    # Set input parameter
    os.mkdir("testproject")
    with open("testproject/main.py", "w") as file:
        file.write("print('Hello World')")
        file.close()
    # Run the command
    cli.execute()
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("testproject/main.py")
    # Read if file has not been updated
    with open("testproject/main.py", "r") as file:
        assert "Hello World" in file.read()
        file.close()
    # Remove test files
    shutil.rmtree(path / 'testvenv')
    shutil.rmtree(path / 'testproject')
    os.remove("pipcx.yaml")


def test_init_with_predefined_files2(path, monkeypatch):
    cli = CLI(["pipcx", "init", "testproject", "--venv=testvenv"])
    # Set input parameter
    monkeypatch.setattr("builtins.input", make_multiple_inputs(
        ["mit", "author", "name@name.com"]))

    os.mkdir("testproject")
    with open("testproject/main.py", "w") as file:
        file.write("print('Hello World')")
        file.close()
    # Run the command
    cli.execute()
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("testproject/main.py")
    # Read if file has not been updated
    with open("testproject/main.py", "r") as file:
        assert "Hello World" in file.read()
        file.close()
    # Remove test files
    shutil.rmtree(path / 'testvenv')
    shutil.rmtree(path / 'testproject')
    os.remove("pipcx.yaml")
