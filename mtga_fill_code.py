from asyncio import run, create_task, gather
from aiohttp import ClientSession
from re import findall
from json import dumps, loads

with open("code.json") as f:
    CODE = loads(f.read())["code"]


async def fetch(session, url, data):
    """
    This is an asynchronous function that uses the data provided to send post requests to the specified URL and return response text and status code.

    Args:
      session: The session parameter is an instance of the AIOHTTP.ClientSession class,
               which is used to cross multiple request management and persistence HTTP connection.
               It allows effective connection pools and reuse, which can improve performance and reduce resource use.
      url: The code of the code requested by the code to it。
      data: `data` The parameter is a dictionary that contains data to be sent in the HTTP Post request.
            Before sending in the request, use the `dumps ()` function in the `json` module to convert it to JSON string。

    Returns:
      A meta -group contains the value of the response obtained by using the given data to
      the specified URL by using the given data to the specified URL by using the given data.
    """
    async with session.post(url, data=dumps(data)) as response:
        return data["code"], await response.text()


async def main():
    """
    This is an asynchronous Python function that logs in to the website, retrieves the CSRF token,
    and then use the token to exchange the code list through the API.
    """
    async with ClientSession(base_url="https://myaccounts.wizards.com") as session:
        async with session.get("/login") as rep:
            login_page = await rep.text()
        csrf = findall('\$scsrf-token":"(.*)",\$', login_page)[0]
        data = {
            "username": "fill your email here",
            "password": "fill your password here",
            "remember": False,
            "_csrf": csrf,
        }
        async with session.post("/api/login", data=dumps(data)) as rep:
            login_done = await rep.text()
            print(login_done)
        code_api = "/api/redemption"

        code_data = lambda code: {"code": code, "_csrf": csrf}

        tasks = [create_task(fetch(session, code_api, code_data(code))) for code in CODE]
        results = await gather(*tasks)
        for result in results:
            print(result)


if __name__ == "__main__":
    run(main())
