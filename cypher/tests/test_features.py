from src.feature_extraction import extract_features


def test_returns_eight_features():
    assert len(extract_features("https://example.com")) == 8


def test_https_flag():
    assert extract_features("https://example.com")[2] == 1
    assert extract_features("http://example.com")[2] == 0


def test_suspicious_keyword_flag():
    assert extract_features("http://secure-login.example.com/verify")[6] == 1
    assert extract_features("https://github.com")[6] == 0


def test_digit_flag():
    assert extract_features("http://192.168.0.1/login")[7] == 1
    assert extract_features("https://github.com")[7] == 0
