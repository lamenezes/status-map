def assert_list(first, second):
    assert len(first) == len(second)
    assert (set(first) - set(second)) == set()
    assert (set(second) - set(first)) == set()
