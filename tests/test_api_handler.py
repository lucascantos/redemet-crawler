import pytest
from src.main import api_handler

def test_api_handler():
    event = {'debug': True}
    assert api_handler(event)