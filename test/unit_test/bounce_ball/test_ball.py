from src.bounce_ball import Ball

def test_init():
    # Given...
    x = 10
    y = 10
    r = 15
    color = (20, 20, 20)

    # When...
    ball = Ball(x, y, r, color)

    # Then...
    assert ball.x == x
    assert ball.y == y
    assert ball.r == r
    assert ball.color == color

def test_increment_position():
    # Given...
    x = 10
    y = 10
    r = 15
    color = (20, 20, 20)
    ball = Ball(x, y, r, color)
    dx = 5
    dy = -5

    # When...
    ball.increment_position(dx, dy)
    expected_x = 15
    expected_y = 5

    # Then...
    assert ball.x == expected_x
    assert ball.y == expected_y 