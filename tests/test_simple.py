import pytest

@pytest.mark.anyio
async def test_simple():
    assert 1 == 1