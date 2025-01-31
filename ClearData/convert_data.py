import re


class ConvertData:
    @staticmethod
    def convert_percentage(value):
        if isinstance(value, str):
            value = value.strip()

            # Obsługa formatu "83% (325/393)"
            match = re.match(r"(\d+)% \((\d+)/(\d+)\)", value)
            if match:
                return float(match.group(1)) / 100  # Zwracamy tylko procent, np. 0.83

            # Obsługa standardowych procentów "49%"
            elif "%" in value:
                return float(value.strip("%")) / 100

            # Obsługa ułamków "325/393"
            elif "/" in value:
                num, denom = map(int, value.split("/"))
                return num / denom

        return value  # Jeśli wartość nie wymaga konwersji, zwracamy ją bez zmian
