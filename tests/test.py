import pytest
from appchecker import AppChecker


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
