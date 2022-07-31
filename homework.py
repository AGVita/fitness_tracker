from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Функция возврата информации о проведенной тренировке."""
        result = (f"Тип тренировки: {self.training_type}; "
                  f"Длительность: {self.duration:.3f} ч.; "
                  f"Дистанция: {self.distance:.3f} км; "
                  f"Ср. скорость: {self.speed:.3f} км/ч; "
                  f"Потрачено ккал: {self.calories:.3f}.")
        return result


class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    M_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        new_obj = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return new_obj


class Running(Training):
    """Тренировка: бег."""
    cof_calorie_1: int = 18
    cof_calorie_2: int = 20

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Функция подсчета истраченных калория для бега."""
        result = ((self.cof_calorie_1 * self.get_mean_speed()
                   - self.cof_calorie_2) * self.weight
                  / self.M_IN_KM * (self.duration * self.M_IN_HOUR))
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cof_calorie_1: float = 0.035
    cof_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 height: float
                 ) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Функция подсчета истраченных калория для ходьбы."""
        result = ((self.cof_calorie_1 * self.weight
                   + (self.get_mean_speed() ** 2 // self.height)
                   * self.cof_calorie_2 * self.weight)
                  * (self.duration * self.M_IN_HOUR))
        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    cof_calorie_1: float = 1.1
    cof_calorie_2: float = 2

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self) -> float:
        """Функция подсчета среднего значения скорости для плавания."""
        result = (self.length_pool * self.count_pool
                  / self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        """Функция подсчета истраченных калорий для плавания."""
        result = ((self.get_mean_speed() + self.cof_calorie_1)
                  * self.cof_calorie_2 * self.weight)
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: dict = {'SWM': Swimming,
                          'RUN': Running,
                          'WLK': SportsWalking,
                          }
    if workout_type in workout_dict.keys():
        return workout_dict.get(workout_type)(*data)
    else:
        """Выводим ошибку в случае, если такого вида тренировки не существует
        """
        raise ValueError(f'Тренировка типа {workout_type} не найдена.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
