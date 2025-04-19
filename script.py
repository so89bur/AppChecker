import asyncio

from appchecker.appchecker import AppChecker

app_checker = AppChecker(silent_mode=False)


@app_checker.check_health
async def check_cache():
    await asyncio.sleep(2)  # Симуляция времени выполнения проверки
    return False  # Успешная проверка


async def main():
    await app_checker.run_checks()
    results = app_checker.get_results()  # Get the results

    for result in results:
        print(f"{result['name']}: {'Success' if result['success'] else 'Failure'}")


if __name__ == "__main__":
    asyncio.run(main())
