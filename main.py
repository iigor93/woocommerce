from woocommerce import API

wcapi = API(
    url="https://studio-oreol.ru",
    consumer_key="ck_500d8cdf5640d62bd9122afd6382133246c86269",
    consumer_secret="cs_1511c4b1621c96055ec9d780b6656425e7d30b5b",
    version="wc/v3"
)

#r = wcapi.get("products", params={"per_page": 1, "page": 3})

#print(wcapi.post("products", data).json())

#print(wcapi.put("products/592", data2).json())
#print(wcapi.post("products/592/variations/batch", data2).json())

print(wcapi.get("products/623").json())
