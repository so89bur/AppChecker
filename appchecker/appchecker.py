import shutil
from typing import Callable, List, Optional, Any
from functools import wraps
from halo import Halo


class bcolors:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"


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
        self._results: List[dict] = []

    def register_check(self, func: Callable[[], Any]) -> Callable[[], Any]:
        if not callable(func):
            raise ValueError("Parameter 'func' must be a callable function.")

        self._checks.append(func)
        return func

    def get_results(self) -> List[dict]:
        return self._results

    def clear_results(self) -> None:
        self._results.clear()

    def _log(self, message: str = "") -> None:
        if not self.silent_mode:
            print(message)

    async def run_checks(self) -> None:
        self.display_message(self.on_center("check starts"))
        self._log(f"collected {len(self._checks)} items")
        self._log()
        for check in self._checks:
            result: Optional[bool] = False
            name: str = check.__name__

            self._log(f"Starting {name}...")
            result = await self.load_with_halo(check)

            self._results.append({"name": name, "success": result})

            if result is True:
                self._spinner.succeed(f"[SUCCESS] {name}")
                self._success += 1
            else:
                self._spinner.fail(f"[FAILURE] {name}")
                self._failure += 1

        self.display_results()

    async def load_with_halo(self, check_func: Callable[[], Any]) -> bool:
        with Halo(text="Loading", spinner="dots", enabled=(not self.silent_mode)):
            try:
                result: bool = await check_func()
            except Exception as e:
                print()
                print(e)
                return False
        return result

    def display_results(self) -> None:
        message: str = f"{self._success} [success]"
        message = self.set_color(self.on_center(message), bcolors.OKGREEN)
        if self._failure:
            message = f"{self._failure} [failure]"
            message = self.set_color(self.on_center(message), bcolors.FAIL)
            self.display_message(message, bcolors.FAIL)
        else:
            self.display_message(message, bcolors.OKGREEN)

        if not self._failure:
            self.display_startup_message("All checks success.")
        elif self._failure == len(self._checks):
            self.display_startup_message("All checks failed.")
        else:
            self.display_startup_message("Some checks failed.")

    def display_startup_message(self, message: str) -> None:
        self._log(message)

    def set_color(self, message: str, color: Optional[str] = None) -> str:
        if color:
            return f"{color}{message}{color}"
        return f"{message}"

    def on_center(self, message: str) -> str:
        terminal_width: int = shutil.get_terminal_size().columns
        return message.center(terminal_width)

    def display_message(self, message: str, color: Optional[str] = None) -> None:
        terminal_width: int = shutil.get_terminal_size().columns
        dashes: str = "-" * terminal_width

        self._log(self.set_color(dashes, color))
        self._log(f"{message}")
        self._log(self.set_color(dashes, color))

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
