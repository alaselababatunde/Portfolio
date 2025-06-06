from hello import hello


def test_default():
    assert hello() == "Hello, World"
           
         
def test_arguements():
    for name in ["hermione", "Harry", "Ron"]:
        assert hello(name) == f"Hello, {name}"