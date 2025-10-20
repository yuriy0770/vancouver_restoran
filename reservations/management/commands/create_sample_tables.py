from django.core.management.base import BaseCommand
from reservations.models import Table


class Command(BaseCommand):
    help = 'Создает примеры столов для ресторана'

    def handle(self, *args, **options):
        tables_data = [
            {"number": 1, "seats": 2, "description": "Романтический столик у окна"},
            {"number": 2, "seats": 2, "description": "Уютный уголок"},
            {"number": 3, "seats": 4, "description": "Стандартный стол"},
            {"number": 4, "seats": 4, "description": "Стол в центре зала"},
            {"number": 5, "seats": 6, "description": "Для большой компании"},
            {"number": 6, "seats": 8, "description": "VIP зона"},
        ]

        created_count = 0
        for table_data in tables_data:
            table, created = Table.objects.get_or_create(
                number=table_data["number"],
                defaults=table_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создан стол #{table.number} ({table.seats} мест)')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {created_count} столов')
        )