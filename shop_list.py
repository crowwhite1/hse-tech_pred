class Shop:
    name: str
    floor: int

    def __init__(self, name, floor):
        self.name = name
        self.floor = floor


class Mall:
    name: str
    address: str
    coord: tuple[int, int]
    shops: list[Shop]

    def __init__(self, name,address, coord, shops):
        self.name = name
        self.address = address
        self.coord = coord
        self.shops = shops


MALLS = [
    Mall("Европейский","Москва. Площадь Киевского Вокзала, 2", (55.744263, 37.565527), [
        Shop("GRASSE PERFUMERIE", 0),
        Shop("Lime", 2),
        Shop("Золотое Яблоко", 1),
        Shop("ДНС", 0),
    ])
]
