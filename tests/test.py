import pytest
from unittest.mock import patch

from appchecker import AppChecker, CheckResult


async def mock_check_success():
    return True


async def mock_check_failure():
    return False


async def mock_check_with_exception():
    raise Exception("Error occurred")


@pytest.mark.asyncio
async def test_register_check():
    checker = AppChecker()
    checker.register_check(mock_check_success)

    assert len(checker._checks) == 1
    assert checker._checks[0] == mock_check_success


@pytest.mark.asyncio
async def test_run_checks_success():
    checker = AppChecker()
    checker.register_check(mock_check_success)

    await checker.run_checks()

    assert checker._success == 1
    assert checker._failure == 0


@pytest.mark.asyncio
async def test_run_checks_failure():
    checker = AppChecker()
    checker.register_check(mock_check_failure)

    await checker.run_checks()

    assert checker._success == 0
    assert checker._failure == 1


@pytest.mark.asyncio
async def test_run_checks_exception_handling():
    checker = AppChecker()
    checker.register_check(mock_check_with_exception)

    await checker.run_checks()

    assert checker._success == 0
    assert checker._failure == 1


@pytest.mark.asyncio
async def test_multiple_checks():
    checker = AppChecker()
    checker.register_check(mock_check_success)
    checker.register_check(mock_check_failure)

    await checker.run_checks()

    assert checker._success == 1
    assert checker._failure == 1


@pytest.mark.asyncio
async def test_get_results():
    app_checker = AppChecker()

    app_checker.register_check(mock_check_success)
    await app_checker.run_checks()

    results = app_checker.get_results()

    assert len(results) == 1
    assert isinstance(results[0], CheckResult)
    assert results[0].name == "mock_check_success"
    assert results[0].success is True


@pytest.mark.asyncio
async def test_clear_results():
    app_checker = AppChecker()

    app_checker.register_check(mock_check_success)
    app_checker.register_check(mock_check_failure)
    await app_checker.run_checks()

    assert len(app_checker.get_results()) == 2

    app_checker.clear_results()

    assert len(app_checker.get_results()) == 0


@pytest.mark.asyncio
async def test_check_health():
    app_checker = AppChecker()

    @app_checker.check_health
    async def check_with_exception():
        raise Exception("Deliberate failure")

    await app_checker.run_checks()
    results = app_checker.get_results()

    assert len(results) == 1
    assert results[0].name == "check_with_exception"
    assert results[0].success is False


@pytest.mark.asyncio
@patch("builtins.print")
async def test_silent_mode(mock_print):

    app_checker = AppChecker(silent_mode=True)
    app_checker.register_check(mock_check_success)

    await app_checker.run_checks()
    assert mock_print.mock_calls == []

    results = app_checker.get_results()

    assert len(results) == 1
    assert results[0].name == "mock_check_success"
    assert results[0].success is True


@pytest.mark.asyncio
@patch("builtins.print")
async def test_silent_mode_off(mock_print):

    app_checker = AppChecker(silent_mode=False)
    app_checker.register_check(mock_check_success)

    await app_checker.run_checks()

    mock_print.assert_called()
