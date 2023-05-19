CAR_MODELS = set()
CAR_COLORS = set()

with open('profile_service/config_car_model.txt', 'r', encoding='utf-8') as car_models:
    for car_model in car_models:
        CAR_MODELS.add(car_model.strip())

with open('profile_service/config_car_color.txt', 'r', encoding='utf-8') as car_colors:
    for color in car_colors:
        CAR_COLORS.add(color.strip())
