import pytest
from app.utils.validators import validate_phone, validate_name, validate_date


def test_phone_valid():
    assert validate_phone('+37369123456') is True

def test_phone_no_plus():
    assert validate_phone('37369123456') is False

def test_phone_letters():
    assert validate_phone('abc') is False

def test_phone_with_spaces():
    assert validate_phone('+373 69 123 456') is True

def test_phone_with_dashes():
    assert validate_phone('+373-69-123-456') is True


def test_name_valid():
    assert validate_name('Иван') is True

def test_name_too_short():
    assert validate_name('A') is False

def test_name_with_digits():
    assert validate_name('Иван123') is False

def test_name_valid_latin():
    assert validate_name('Ivan') is True

def test_name_too_long():
    assert validate_name('А' * 51) is False


def test_date_valid():
    assert validate_date('24.06.2026') is True

def test_date_wrong_format():
    assert validate_date('2026-06-24') is False

def test_date_impossible():
    assert validate_date('99.99.9999') is False

def test_date_empty():
    assert validate_date('') is False
