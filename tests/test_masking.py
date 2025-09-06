import pytest
from logpie.masking.engine import MaskingEngine

@pytest.fixture
def masking_engine():
    return MaskingEngine()

def test_mask_text_email(masking_engine):
    text = "My email is john@example.com and another is jane@domain.net."
    expected = "My email is [EMAIL_MASKED] and another is [EMAIL_MASKED]."
    assert masking_engine.mask_text(text) == expected

def test_mask_text_cpf(masking_engine):
    text = "The CPF is 123.456.789-00 and another is 987.654.321-10."
    expected = "The CPF is [CPF_MASKED] and another is [CPF_MASKED]."
    assert masking_engine.mask_text(text) == expected

def test_mask_text_no_sensitive_data(masking_engine):
    text = "Hello world. Nothing to hide."
    assert masking_engine.mask_text(text) == text

def test_mask_text_mixed_data(masking_engine):
    text = "Email: user@test.com, CPF: 111.222.333-44, Phone: (11) 98765-4321."
    expected = "Email: [EMAIL_MASKED], CPF: [CPF_MASKED], Phone: [PHONE_MASKED]."
    assert masking_engine.mask_text(text) == expected

def test_mask_log_entry_simple(masking_engine):
    log_entry = {"email": "admin@company.com", "ip": "192.168.0.1"}
    expected = {"email": "[EMAIL_MASKED]", "ip": "192.168.0.1"}
    assert masking_engine.mask_log_entry(log_entry) == expected

def test_mask_log_entry_nested(masking_engine):
    log_entry = {
        "event": "user_update",
        "details": {
            "old_email": "foo@bar.com",
            "new_email": "baz@bar.com",
            "id": 123
        }
    }
    expected = {
        "event": "user_update",
        "details": {
            "old_email": "[EMAIL_MASKED]",
            "new_email": "[EMAIL_MASKED]",
            "id": 123
        }
    }
    assert masking_engine.mask_log_entry(log_entry) == expected

def test_mask_log_entry_list(masking_engine):
    log_entry = {"cards": [{"c": "1111-2222-3333-4444"}, {"c": "5555-6666-7777-8888"}]}
    expected = {"cards": [{"c": "[CREDIT_CARD_MASKED]"}, {"c": "[CREDIT_CARD_MASKED]"}]}
    assert masking_engine.mask_log_entry(log_entry) == expected

def test_mask_text_empty_string(masking_engine):
    assert masking_engine.mask_text("") == ""

def test_mask_text_non_string_input(masking_engine):
    assert masking_engine.mask_text(12345) == 12345
