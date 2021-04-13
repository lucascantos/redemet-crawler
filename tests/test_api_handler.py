import pytest
from src.handler import api_handler

def test_api_handler():
    event = {'debug': True}
    assert api_handler(event)