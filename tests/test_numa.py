import numa


def test_available():
    assert numa.available()
