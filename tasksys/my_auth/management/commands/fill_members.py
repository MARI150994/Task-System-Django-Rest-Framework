from django.core.management.base import BaseCommand

from my_auth.models import Department, Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = [('Electronics Development department', 'Junior development engineer', False, False),
                ('Electronics Development department', 'Development engineer', False, False),
                ('Electronics Development department', 'Lead development engineer', False, False),
                ('Electronics Development department', 'Head electronics development', True, False),
                ('Constructor Development department', 'Constructor engineer', False, False),
                ('Constructor Development department', 'Lead constructor engineer', False, False),
                ('Constructor Development department', 'Junior constructor engineer', False, False),
                ('Constructor Development department', 'Head constructor development', True, False),
                ('Project management department', 'Project manager', False, True),
                ('Project management department', 'Junior project manager', False, True),
                ('Project management department', 'Lead project manager', False, True),
                ('Project management department', 'Head project management', True, True),
                ('Embedded Software Development Department', 'Programmer', False, False),
                ('Embedded Software Development Department', 'Tester', False, False),
                ('Embedded Software Development Department', 'Head embedded software', True, False),
                ('Application Software Development Department', 'Programmer', False, False),
                ('Application Software Development Department', 'Lead programmer', False, False),
                ('Application Software Development Department', 'Tester', False, False),
                ('Application Software Development Department', 'Head application software', True, False), ]

        for department_name, name, header, manager in data:
            print(department_name)
            print(Department.objects.get(name=department_name))
            dep = Department.objects.get(name=department_name)
            Role.objects.get_or_create(department=dep, name=name, is_header=header, is_manager=manager)
