import math

import shop_list


def get_path(lat, lon, shops):
    diff = -1
    target_mall = None
    distance = 10 ** 15

    for mall in shop_list.MALLS:
        shops = set(shops)
        mall_shops = set(shop.name for shop in mall.shops)
        intersection = shops.intersection(mall_shops)
        if len(intersection) > diff:
            target_mall = mall
            diff = len(intersection)
            distance = distance_calc((lat, lon), (mall.coord[0], mall.coord[0]))
        elif len(intersection)==diff and distance_calc((lat, lon), (mall.coord[0], mall.coord[0]))<distance:
            distance = distance_calc((lat, lon), (mall.coord[0], mall.coord[0]))
            target_mall = mall

    shops_to_visit = [shop for shop in target_mall.shops if shop.name in shops]
    answer = f'Вы можете пойти в торговый центр: {target_mall.name}\n'
    answer += f'Его адрес: {target_mall.address}\n'
    answer += f'Там вы сможете попасть в следующие магазины: {", ".join([shop.name for shop in shops_to_visit])}\n'
    answer += f'Оптимальным маршрутом будет: {" -> ".join(shop.name for shop in sorted(shops_to_visit, key=lambda shop: shop.floor))}'
    return answer

def distance_calc(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d