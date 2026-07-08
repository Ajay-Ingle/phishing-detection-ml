"""Tests for src/features/extractor.py.

WHOIS-dependent functions (extract_features, domain_age, domain_end) are
tested with mocked datetime inputs so tests run offline and deterministically
— we're testing our own logic, not python-whois or the network.
"""

from datetime import datetime, timedelta

from src.features.extractor import (
    domain_age,
    domain_end,
    get_depth,
    get_length,
    have_at_sign,
    having_ip,
    prefix_suffix,
    redirection,
    tiny_url,
)


# ---- Address-bar features: pure string logic, no mocking needed -----------

def test_having_ip_detects_raw_ip_host():
    assert having_ip("http://192.168.1.1/login") == 1


def test_having_ip_ignores_normal_domain():
    assert having_ip("http://example.com/login") == 0


def test_have_at_sign_present():
    assert have_at_sign("http://example.com@evil.com") == 1


def test_have_at_sign_absent():
    assert have_at_sign("http://example.com/path") == 0


def test_get_length_under_threshold_is_legitimate():
    assert get_length("http://short.com") == 0


def test_get_length_over_threshold_is_phishing():
    long_url = "http://example.com/" + "a" * 60
    assert get_length(long_url) == 1


def test_get_depth_counts_nonempty_segments():
    assert get_depth("http://example.com/a/b/c") == 3


def test_get_depth_ignores_trailing_slash():
    assert get_depth("http://example.com/a/b/") == 2


def test_get_depth_root_path_is_zero():
    assert get_depth("http://example.com") == 0


def test_redirection_detects_double_slash_after_protocol():
    assert redirection("http://example.com//redirect.com") == 1


def test_redirection_ignores_protocol_slashes():
    assert redirection("http://example.com/path") == 0


def test_tiny_url_detects_known_shortener():
    assert tiny_url("http://bit.ly/abc123") == 1


def test_tiny_url_ignores_normal_domain():
    assert tiny_url("http://example.com/abc123") == 0


def test_prefix_suffix_detects_dash_in_domain():
    assert prefix_suffix("http://my-bank-secure.com") == 1


def test_prefix_suffix_ignores_dash_in_path():
    assert prefix_suffix("http://example.com/my-page") == 0


# ---- Domain-based features: test the date logic directly ------------------

def test_domain_age_flags_young_domain_as_phishing():
    creation = datetime.now() - timedelta(days=30)
    expiration = datetime.now() + timedelta(days=30)
    assert domain_age(creation, expiration) == 1


def test_domain_age_accepts_established_domain():
    creation = datetime.now() - timedelta(days=730)
    expiration = datetime.now() + timedelta(days=365)
    assert domain_age(creation, expiration) == 0


def test_domain_age_missing_dates_defaults_to_phishing():
    assert domain_age(None, None) == 1


def test_domain_end_flags_expiring_soon_as_phishing():
    expiration = datetime.now() + timedelta(days=10)
    assert domain_end(expiration) == 1


def test_domain_end_accepts_long_remaining_validity():
    expiration = datetime.now() + timedelta(days=400)
    assert domain_end(expiration) == 0


def test_domain_end_missing_expiration_defaults_to_phishing():
    assert domain_end(None) == 1
