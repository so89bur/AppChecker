import shutil
import time
from dataclasses import dataclass
from functools import wraps
from typing import Callable, List, Optional, Any

from halo import Halo


class bcolors:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"


@dataclass
class CheckResult:
    name: str
    success: bool


class AppChecker:
    def __init__(
        self,
        silent_mode: bool = False,
    ) -> None:
        if not isinstance(silent_mode, bool):
            raise ValueError("Parameter 'silent_mode' must be a boolean value.")

        self.silent_mode = silent_mode
        self._checks: List[Callable[[], Any]] = []
        self._spinner: Halo = Halo(
            text="Loading", spinner="dots", enabled=(not self.silent_mode)
        )
        self._success: int = 0
        self._failure: int = 0
        self._results: List[CheckResult] = []
        self._process_time = 0
        self.terminal_width: int = 0

    def register_check(self, func: Callable[[], Any]) -> Callable[[], Any]:
        if not callable(func):
            raise ValueError("Parameter 'func' must be a callable function.")

        self._checks.append(func)
        return func

    def get_results(self) -> List[CheckResult]:
        return self._results

    def clear_results(self) -> None:
        self._results.clear()

    def _log(self, message: str = "") -> None:
        if not self.silent_mode:
            print(message)

    async def run_checks(self) -> None:
        start_time = time.perf_counter()
        self._terminal_width: int = shutil.get_terminal_size().columns
        self._display_message(self._on_center("check starts"))
        self._log(f"collected {len(self._checks)} items")
        self._log()
        for check in self._checks:
            result: Optional[bool] = False
            name: str = check.__name__

            self._log(f"Starting {name}...")
            result = await self._load_with_halo(check)

            self._results.append(CheckResult(name=name, success=result))

            if result is True:
                self._spinner.succeed(f"[SUCCESS] {name}")
                self._success += 1
            else:
                self._spinner.fail(f"[FAILURE] {name}")
                self._failure += 1
        self._process_time = time.perf_counter() - start_time
        self._display_results()

    async def _load_with_halo(self, check_func: Callable[[], Any]) -> bool:
        with Halo(text="Loading", spinner="dots", enabled=(not self.silent_mode)):
            try:
                result: bool = await check_func()
            except Exception as e:
                print()
                print(e)
                return False
        return result

    def _display_results(self) -> None:
        _time_s = round(self._process_time, 2)
        if self._failure:
            message = f"{self._failure} [failure] in {_time_s}s"
            message = self._set_color(self._on_center(message), bcolors.FAIL)
            self._display_message(message, bcolors.FAIL)
        else:
            message: str = f"{self._success} [success] in {_time_s}s"
            message = self._set_color(self._on_center(message), bcolors.OKGREEN)
            self._display_message(message, bcolors.OKGREEN)

        if not self._failure:
            self._display_startup_message("All checks success.")
        elif self._failure == len(self._checks):
            self._display_startup_message("All checks failed.")
        else:
            self._display_startup_message("Some checks failed.")

    def _display_startup_message(self, message: str) -> None:
        self._log(message)

    def _set_color(self, message: str, color: Optional[str] = None) -> str:
        if color:
            return f"{color}{message}{color}"
        return f"{message}"

    def _on_center(self, message: str) -> str:
        return message.center(self._terminal_width)

    def _display_message(self, message: str, color: Optional[str] = None) -> None:
        dashes: str = "-" * self._terminal_width

        self._log(self._set_color(dashes, color))
        self._log(f"{message}")
        self._log(self._set_color(dashes, color))

    def check_health(self, func: Callable[[], Any]) -> Callable[[], Any]:

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> bool:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                self._log()
                self._log(e)
                return False

        self.register_check(wrapper)
        return wrapper
