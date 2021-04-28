import pytest

class TestExample:
    def func(self,x):
        return x + 1

    def exit_(self):
        raise SystemExit(1)

    def test_answer(self):
        assert self.func(3) == 4

    def test_raise(self):
        with pytest.raises(SystemExit):
            self.exit_()
