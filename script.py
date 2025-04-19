import asyncio

# import asyncpg
# import httpx

from appchecker.appchecker import AppChecker

app_checker = AppChecker(silent_mode=False)


# @app_checker.check_health
# async def check_database():
#     # try:
#     connection = await asyncpg.connect(
#         user="odoo_dev",
#         password="odoo_dev_pass",
#         database="dev",
#         host="127.0.0.1",
#         port="5432",
#     )
#     await connection.close()
#     return True
#     # except Exception as e:
#     #     return False


# @app_checker.check_health
# async def check_external_service():
#     # try:
#     async with httpx.AsyncClient() as client:
#         response = await client.get("https://api.yookassa.ru/v3/payments")
#         return response.status_code < 500
#     # except:
#     #     return False


# @app_checker.check_health
async def check_cache():
    await asyncio.sleep(2)  # Симуляция времени выполнения проверки
    return False  # Успешная проверка


@app_checker.check_health
async def check_cache1():
    await asyncio.sleep(1)  # Симуляция времени выполнения проверки
    return True  # Успешная проверка


async def main():

    app_checker.register_check(check_cache)
    await app_checker.run_checks()
    results = app_checker.get_results()  # Get the results

    for result in results:
        print(f"{result['name']}: {'Success' if result['success'] else 'Failure'}")


if __name__ == "__main__":
    asyncio.run(main())
