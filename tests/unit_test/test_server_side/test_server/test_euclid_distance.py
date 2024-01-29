from src.server.server import euclid_distance

def test_euclid_distance():
    # Given...
    p1 = [0, 0]
    p2 = [3, 4]

    # When...
    actual = euclid_distance(p1, p2)
    expected = 5

    # Then...
    assert actual == expected
