import pytest
from handler import redemet_crawler

def test_api_handler():
    event = {'debug': True}
    assert redemet_crawler(event)