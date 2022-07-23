from woocommerce import API
import asyncio
import aiohttp

#new_branch
#second_commit


wcapi = API(
    url="https://studio-oreol.ru",
    consumer_key="ck_500d8cdf5640d62bd9122afd6382133246c86269",
    consumer_secret="cs_1511c4b1621c96055ec9d780b6656425e7d30b5b",
    version="wc/v3"
)

consumer_key="ck_500d8cdf5640d62bd9122afd6382133246c86269"
consumer_secret="cs_1511c4b1621c96055ec9d780b6656425e7d30b5b"


#print(wcapi.consumer_key)

#r = wcapi.get("products", params={"per_page": 1, "page": 3})

#print(wcapi.post("products", data).json())

data2 = {'meta_data': [{
        'id': 5568,
		'key': '_yoast_wpseo_title',
		'value': 'Картина для современного интерьера Кувшинки12'
	}]
    }

print(wcapi.put("products/707", data2).json())


#print(wcapi.post("products/592/variations/batch", data2).json())

#print(wcapi.get("products/623/variations/659").json())

# /wp-json/wc/v3/products

async def main():
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(consumer_key, consumer_secret)) as session:
        async with session.get('https://studio-oreol.ru/wp-json/wc/v3/products') as resp:
            print(resp.status)
            print(await resp.json())

#asyncio.run(main())

