def study_atmosphere(planet):
    if hasattr(planet, 'atmosphere'):
        print(f"Изучение атмосферы {planet.name}: {planet.atmosphere}")
    else:
        print(f"У {planet.name} нет атмосферы.")