def study_surface(planet):
    if hasattr(planet, 'surface'):
        print(f"Изучение поверхности {planet.name}: {planet.surface}")
    else:
        print(f"Данные о поверхности {planet.name} отсутствуют.")