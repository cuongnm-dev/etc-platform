"""Critical business test cases mapped from tests/testcases/catalog.json."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from etc_platform.data.validation import validate_content_data
from etc_platform.mcp_server import export
from etc_platform.mcp_server import validate as mcp_validate

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_MINIMAL = REPO_ROOT / "examples" / "minimal" / "content-data.json"


def _load_minimal_content_data() -> dict:
    return json.loads(EXAMPLE_MINIMAL.read_text(encoding="utf-8"))


@pytest.mark.tc_critical
@pytest.mark.tc_data
def test_tc_data_001_minimal_content_data_valid() -> None:
    """TC-DATA-001: minimal sample must pass schema validation."""
    result = validate_content_data(_load_minimal_content_data())
    assert result.valid is True


@pytest.mark.tc_critical
@pytest.mark.tc_data
def test_tc_data_002_missing_project_block_fails() -> None:
    """TC-DATA-002: missing required root block must fail."""
    payload = _load_minimal_content_data()
    payload.pop("project", None)

    result = validate_content_data(payload)
    assert result.valid is False
    assert any("Schema validation failed" in err for err in result.errors)


@pytest.mark.tc_critical
@pytest.mark.tc_api
def test_tc_api_001_validate_rejects_non_dict_payload() -> None:
    """TC-API-001: validate rejects invalid payload type."""
    response = json.loads(mcp_validate(["invalid", "payload"]))
    assert response["valid"] is False
    assert response["error_code"] == "INVALID_ARGS"


@pytest.mark.tc_critical
@pytest.mark.tc_export
def test_tc_export_001_missing_content_data_file_returns_error() -> None:
    """TC-EXPORT-001: legacy mode with missing file returns explicit error."""
    response = json.loads(export("does-not-exist.json", "output"))
    assert response["success"] is False
    assert "not found" in response["error"]


@pytest.mark.tc_export
def test_tc_export_002_invalid_screenshot_filename_rejected() -> None:
    """TC-EXPORT-002: screenshot filename must not allow traversal."""
    content_data = _load_minimal_content_data()
    response = json.loads(
        export(
            content_data,
            screenshots={"../bad.png": "ZmFrZQ=="},
            targets=["hdsd"],
        )
    )
    assert response["success"] is False
    assert "Invalid screenshot filename" in response["error"]


@pytest.mark.tc_api
def test_tc_api_002_validate_response_has_contract_keys() -> None:
    """TC-API-002: validate response preserves stable result contract."""
    response = json.loads(mcp_validate(_load_minimal_content_data()))
    assert {"valid", "errors", "warnings", "stats"}.issubset(response.keys())
