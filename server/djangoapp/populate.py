from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name":"NISSAN", "description":"Great cars. Many options"},
        {"name":"Mercedes", "description":"Luxury cars. Best engineering"},
        {"name":"Audi", "description":"Quality cars. Slogan: Vorsprung durch Technik"},
        {"name":"Kia", "description":"Reliable and affordable cars"},
        {"name":"Toyota", "description":"World-renowned for durability"}
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(CarMake.objects.create(name=data['name'], description=data['description']))


    car_model_data = [
        {"name":"Pathfinder", "type":"SUV", "year":2023, "car_make":car_make_instances[0]},
        {"name":"Qashqai", "type":"SUV", "year":2023, "car_make":car_make_instances[0]},
        {"name":"XTrail", "type":"SUV", "year":2023, "car_make":car_make_instances[0]},
        {"name":"A-Class", "type":"Sedan", "year":2023, "car_make":car_make_instances[1]},
        {"name":"C-Class", "type":"Sedan", "year":2023, "car_make":car_make_instances[1]},
        {"name":"E-Class", "type":"Sedan", "year":2023, "car_make":car_make_instances[1]},
        {"name":"A4", "type":"Sedan", "year":2023, "car_make":car_make_instances[2]},
        {"name":"A6", "type":"Sedan", "year":2023, "car_make":car_make_instances[2]},
        {"name":"A8", "type":"Sedan", "year":2023, "car_make":car_make_instances[2]},
        {"name":"Sorrento", "type":"SUV", "year":2023, "car_make":car_make_instances[3]},
        {"name":"Sportage", "type":"SUV", "year":2023, "car_make":car_make_instances[3]},
        {"name":"Cerato", "type":"Sedan", "year":2023, "car_make":car_make_instances[3]},
        {"name":"Corolla", "type":"Sedan", "year":2023, "car_make":car_make_instances[4]},
        {"name":"Camry", "type":"Sedan", "year":2023, "car_make":car_make_instances[4]},
        {"name":"RAV4", "type":"SUV", "year":2023, "car_make":car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(name=data['name'], car_make=data['car_make'], type=data['type'], year=data['year'])
