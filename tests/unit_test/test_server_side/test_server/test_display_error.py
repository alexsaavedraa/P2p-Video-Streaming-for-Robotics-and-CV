from src.server import server

def test_display_error(mocker):
    # Given...
    p1 = [0, 0]
    p2 = [3, 4]
    e = 5
    mock_cv2 = mocker.patch("src.server.server.cv2")
    mock_cv2.putText.return_value = "image"
    
    # When...
    server.display_error(p1, p2, e)

    # Then...
    mock_cv2.imshow.assert_called_with("Server: Error Detection", "image")