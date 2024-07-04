import enum


class IdentityType(enum.Enum):
    INDIVIDUAL = "индивидуальная"
    GROUP = "групповая"


class RegistrationStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    TERMINATED = "TERMINATED"


class InitialIdentificationType(enum.Enum):
    BIRTH = "рождение"
    IMPORT = "импорт"
    OTHER = "другое"


class AnimalGender(enum.Enum):
    MALE = "самец"
    FEMALE = "самка"


class AnimalGroupGender(enum.Enum):
    MALE = "самец"
    FEMALE = "самка"
    UNDEFINED = "неизвестный"


class AnimalIDFormat(enum.Enum):
    UNMM = "UNMM"
    OTHER = "OTHER"


class AnimalLabelType(enum.Enum):
    MAIN = "основное"
    ADDITIONAL = "дополнительное"


class MarkingMeansType(enum.Enum):
    LABEL = "Бирка"  # "Бирка"
    MICROCHIP = "Вживляемый микрочип"  # "Вживляемый микрочип"
    BRAND = "BRAND"  # "Тавро/Клеймо"
    TATTOO = "TATTOO"  # "Татуировка"
    BOLUS = "Болюс"  # "Болюс"
    RING = "Кольцо"  # "Кольцо"
    ELECTRONIC_RING = "Электронное кольцо"  # "Электронное кольцо"
    COLLAR = ("Ошейник",)  # "Ошейник"
    ELECTRONIC_COLAR = "Электронный ошейник"  # "Электронный ошейник"
    WING_TAG = "Крыло-метка"  # "Крыло-метка"
    ELECTRONIC_WING_TAG = "Электронное крыло-метка"  # "Электронное крыло-метка"
    ELECTRONIC_TAG = "Электронная метка"  # "Электронная метка"
    TISSUE_SECTION = "TISSUE_SECTION"  # "Вырез тканей"
    NAMEPLATE = "Табло"  # "Табло"


class VeterinaryEventType(enum.Enum):
    AME = "AME"  # "нанесение средства маркирования"
    AIR = "AIR"  # "выбытие средства маркирования"


class AnimalMarkingEventReason(enum.Enum):
    TERMINATED = "TERMINATED"  # "Прекращение эксплуатации средства маркирования по причине выбытия животного"
    LOSS = "LOSS"  # "Средство маркирования утеряно"
    BROKEN = "BROKEN"  # "Средство маркирования повреждено (сломано)"
    EXPIRATION = "EXPIRATION"  # "Истёк срок действия средства маркирования"
    REMOVED = "REMOVED"  # "Средство маркирования удалено владельцем животного"


class AnimalBreedingValueType(enum.Enum):
    BREEDING = "племенное"  # "Племенное"
    NON_BREEDING = "не племенное"  # "Не племенное"
    UNDEFINED = "другое"  # "Тип не определен"
