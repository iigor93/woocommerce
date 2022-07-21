from django.shortcuts import render
import asyncio
import aiohttp
from woocom.config import wcapi


async def request_to_site(id_, all_variations):
    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(wcapi.consumer_key, wcapi.consumer_secret)) as session:
        async with session.get(f"https://studio-oreol.ru/wp-json/wc/v3/products/{id_}/variations") as resp:
            
            all_variations.append(await resp.json())
    
    return all_variations


def main(request):
    
    if request.method == 'POST':
        v_id = request.POST.get('short_desc_id')
        description = request.POST.get('name_desc')
        short_description = request.POST.get('name_shor_desc')
        
        title = request.POST.get('title_textarea').strip()
        title_description = request.POST.get('title_d_textarea').strip()
        
        description_id = request.POST.get('yoast_description')
        title_id = request.POST.get('yoast_title')
        
        
        data_save = {}

        if description:
            data_save['description'] = description
        if short_description:
            data_save['short_description'] = short_description
            
            
        meta_data = []
            
        if title:
            meta_data.append({'id': title_id, 'key': '_yoast_wpseo_title', 'value': title})
        
        if title_description:
            meta_data.append({'id': description_id, 'key': '_yoast_wpseo_metadesc', 'value': title_description})
            
            
            
        if title_description:
            data_save['title_description'] = title_description
        if description_id:
            data_save['description_id'] = description_id
        if meta_data:
            data_save['meta_data'] = meta_data
        
            
        if data_save:
            
            r = wcapi.put(f"products/{v_id}", data_save).json()

    page = 1 if request.GET.get('page') is None else request.GET.get('page')
    
    raw_data = wcapi.get("products", params={"per_page": 10, "page": int(page)})
    
    data = raw_data.json()
    
    all_variations = []
    all_variation_attr = []
    
    async def func_main(data, all_variations):
    
        background_tasks = set()
        
        for item in data:
            task = asyncio.create_task(request_to_site(item.get('id'), all_variations))
            background_tasks.add(task)
            
        for item2 in background_tasks:
            await item2

    # asyncio.run(func_main(data, all_variations))
    
    for all_item in all_variations:    
        for item in all_item:
            temp_dict = {}
            
            temp_dict['id'] = item.get('id')
            temp_dict['price'] = item.get('price')
            temp_dict['regular_price'] = item.get('regular_price')
            attributes_val = item.get('attributes')
            temp_dict['option'] = attributes_val[0].get('option')
            temp_dict['stock_status'] = item.get('stock_status')
            temp_dict['sale_price'] = item.get('sale_price')
            
            temp_dict['date_on_sale_from'] = item.get('date_on_sale_from')[:10] if item.get('date_on_sale_from') else None
            
            temp_dict['date_on_sale_to'] = item.get('date_on_sale_to')[:10] if item.get('date_on_sale_to') else None

            all_variation_attr.append(temp_dict)
            
    headers = raw_data.headers
    
    total_pages = headers.get('X-WP-TotalPages')
    
    try:
        total_pages = int(total_pages) + 1
    except (ValueError, TypeError):
        print('err int')

    context = {'user': 'igor', 'data': data, 'total_pages': range(1, total_pages), 'page': page, 'all_variations': all_variation_attr}
    return render(request, 'woocom/Main.html', context)


def detail(request, d_id):
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        short_description = request.POST.get('short_description')
        
        regular_price = request.POST.get('regular_price')
        sale_price = request.POST.get('sale_price')
        v_id = request.POST.get('v_id')
        
        stock = request.POST.get('stock')
        
        date_on_sale_from = request.POST.get('date_on_sale_from')
        if date_on_sale_from:
            date_on_sale_from += ' 00:00:00'
        
        date_on_sale_to = request.POST.get('date_on_sale_to')
        if date_on_sale_to:
            date_on_sale_to += ' 23:59:59'
        
        sale_cancel = request.POST.get('sale_cancel')
        
        data = {}
        
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if short_description:
            data['short_description'] = short_description
  
        if data:
            r = wcapi.put(f"products/{d_id}", data).json()
        
        data_price = {}
        
        if regular_price:
            data_price['regular_price'] = regular_price
        if sale_price:
            data_price['sale_price'] = sale_price
        if date_on_sale_from:
            data_price['date_on_sale_from'] = date_on_sale_from
        if date_on_sale_to:
            data_price['date_on_sale_to'] = date_on_sale_to
            
        if stock == 'instock':
            data_price['stock_status'] = 'instock'
        if stock == 'onbackorder':
            data_price['stock_status'] = 'onbackorder'
        
        if sale_cancel == 'true':
            data_price['sale_price'] = ""
            data_price['date_on_sale_from'] = ""
            data_price['date_on_sale_to'] = ""
            data_price['date_on_sale_from_gmt'] = ""
            data_price['date_on_sale_to_gmt'] = ""

        if data_price:
            r = wcapi.put(f"products/{d_id}/variations/{v_id}", data_price).json()

    instant = wcapi.get(f"products/{d_id}").json()
    options = wcapi.get(f"products/{d_id}/variations").json()
    
    context = {'options': options, 'instant': instant}
    
    return render(request, 'woocom/detail.html', context)
