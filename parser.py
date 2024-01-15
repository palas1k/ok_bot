import aiohttp
import asyncio
import os

from bs4 import BeautifulSoup

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Auth:
    session: aiohttp.ClientSession = None

    def start_session(self):
        self.session = aiohttp.ClientSession()
        return self.session

    async def session_close(self):
        if self.session is not None:
            await self.session.close()
        self.session = None

    async def perform_login(self, login, password):
        data = {
            'st.redirect': '',
            'st.asr': '',
            'st.posted': 'set',
            'st.fJS': 'on',
            'st.st.screenSize': '1600 x 900',
            'st.st.browserSize': '739',
            'st.st.flashVer': '0.0.0',
            'st.email': login,
            'st.password': password,
        }
        url = "https://ok.ru/dk?cmd=AnonymLogin&st.cmd=anonymMain"
        try:
            conn = self.start_session()
            # r = await conn.post(url=url, data=data)
            r = await self.session.post(url=url, data=data)
            return r
        except Exception as ex:
            raise ex

    async def get(self, url: str):
        conn = self.session
        r = await conn.get(url)
        return await r.text()


class OkParser:

    def __init__(self):
        self.auth_session = Auth()

    async def get_url(self, url: str):
        r = self.auth_session.start_session()
        res = await r.get(url)
        r = await res.text()
        await self.auth_session.session_close()
        return r

    async def get_data(self, login: str, password: str, url: str):
        obj = await self.auth_session.perform_login(login, password)
        obj = await self.auth_session.session.get(url)
        r = await obj.text()
        await self.auth_session.session_close()
        print(r)
        return r

    async def check_post(self) -> str:
        url: str = 'https://ok.ru/profile/587077083456/statuses'
        try:
            r = await self.auth_session.get(url)
            soup = BeautifulSoup(r, "html.parser")
            answer = soup.find("div", {"class": "media-text_cnt_tx"}).text
            return answer
        except Exception as ex:
            raise ex
        finally:
            await self.auth_session.session_close()

    async def get_bio(self, user_id: int):
        url: str = f"https://ok.ru/profile/{user_id}/about"
        r = await self.auth_session.session.get(url)
        text = ''
        soup = BeautifulSoup(r, "html.parser")
        text += soup.find(class_="compact-profile_a").text
        text += soup.find("div", {"class": "user-profile_list"}).get_text(separator='')
        print(text)
        return text


op = OkParser()
asyncio.run(op.auth_session.perform_login('9393968088', 'liserg09vip'))
asyncio.run(op.auth_session.session.get(574056415324))

