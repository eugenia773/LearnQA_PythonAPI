class TestPhrase:
    def test_phrase_len(self):
        phrase = input("Set a phrase:")
        over_len = 15
        assert len(phrase) < over_len, f"Phrase has {over_len} or more symbols"
