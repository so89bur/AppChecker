# AppChecker

`AppChecker` is an asynchronous tool for performing application health checks during startup. It can be particularly useful in applications like FastAPI, where it helps confirm that your dependencies are running and operational, including database access, RabbitMQ connectivity, and that your application is ready to respond to HTTP requests. 

With `AppChecker`, you can easily register health check functions and manage their execution, making it a great fit for microservices and other applications that require health checks.

## Installation

You can install `AppChecker` using pip:

```bash
pip install appchecker
```

using `uv`:

```bash
uv add appchecker
```

## Example Usage
Each custom health check function, such as `check_cache`, should return either `True` for a successful check or `False` for a failed check. Here’s an example of how to use AppChecker for checking your application:

```python
import asyncio
from appchecker import AppChecker  # Import the AppChecker

# Create an instance of AppChecker
app_checker = AppChecker()

@app_checker.check_health
async def check_cache():
    await asyncio.sleep(2)  # Simulate the time taken to perform the check
    return True  # Successful check

async def main():
    await app_checker.run_checks()  # Run all checks

if __name__ == "__main__":
    asyncio.run(main())  # Start the asyncio event loop
```

## Alternative Usage

In addition to using the decorator for registering health checks, you can also register checks using the register_check method directly. Here's how you can do it:
```python

app_checker = AppChecker()

async def check_cache():
    await asyncio.sleep(2)
    return True

# Register the health check function
app_checker.register_check(check_cache)

await app_checker.run_checks()  # Run all checks
```


## Example Output

When you run your checks, you’ll see output similar to this in the console:
```bash
---------------------------------------------------------------------------
                              check starts
---------------------------------------------------------------------------
collected 1 items

Starting check_cache...
✔ [SUCCESS] check_cache
---------------------------------------------------------------------------
                              1 [success]
---------------------------------------------------------------------------
All checks success.
```

## Silent Mode

You can run the `AppChecker` in silent mode, which suppresses all console output. This can be useful if you want to only obtain results from the checks without any other output.

### Enabling Silent Mode

To enable silent mode, simply pass `silent_mode=True` when creating an instance of `AppChecker`:

```python
import asyncio
from appchecker import AppChecker

# Create an instance of AppChecker with silent mode enabled
app_checker = AppChecker(silent_mode=True)

@app_checker.check_health
async def check_cache():
    await asyncio.sleep(2)  # Simulate the time taken to perform the check
    return True  # Successful check (return False for a failed check)

async def main():
    await app_checker.run_checks()  # Run all checks
    results = app_checker.get_results()  # Get the results

    for result in results:
        print(f"{result.name}: {'Success' if result.success else 'Failure'}")

if __name__ == "__main__":
    asyncio.run(main())  # Start the asyncio event loop
```
In this example, all console output during the checks will be suppressed, and you can use the `get_results()` method to view the results without any extra information cluttering your console.


## How It Works

AppChecker allows you to register health check functions using the check_health decorator. Each health check function should be asynchronous and return a result (e.g., True for a successful check or raise an exception for a failed check).

When you call app_checker.run_checks(), all registered functions are invoked in sequence, and the results are displayed on the screen.

## Features

- Asynchronous: Uses asynchronous functions for checks, which do not block the main execution flow.
- Flexibility: Easily add new checks by wrapping them in the decorator.
- Result Display: Conveniently displays the results of checks, including successful and failed checks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contribution

If you have suggestions for improving AppChecker, feel free to create a Pull Request or open Issues in the repository.
