# Пока что заглушки для методов кодирования-декодирования


class Hamming:
    @staticmethod
    def encode(data: bytes) -> bytes:
        """Кодирует любую байтовую сроку по Хэммингу (ниче особенного)"""
        return data

    @staticmethod
    def decode(data: bytes) -> bytes:
        """Возвращает корректную раскодированную строку (ошибки УЖЕ исправлены)"""
        return data
