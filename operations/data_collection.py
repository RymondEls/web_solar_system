def collect_data(body):
    print(f"Сбор данных о {body.name}:")
    print(f"Масса: {body.mass} кг")
    print(f"Положение: {body.position} м")
    print(f"Скорость: {body.velocity} м/с")
    if hasattr(body, 'atmosphere'):
        print(f"Атмосфера: {body.atmosphere}")
    if hasattr(body, 'surface'):
        print(f"Поверхность: {body.surface}")