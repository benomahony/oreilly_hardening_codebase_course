stock = 10

def test_shared_stock():
    global stock
    stock -= 1
    assert stock == 9
