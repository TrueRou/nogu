import asyncio

from ossapi import OssapiAsync, serialize_model, MatchResponse

import config

api = OssapiAsync(config.osu_api_v2_id, config.osu_api_v2_secret)

async def main():
    a: MatchResponse = await api.match(108321089)
    print(a.events)
    with open("result.json", "w") as file:
        file.write(serialize_model(a))



if __name__ == '__main__':
    asyncio.run(main())