from django.core.management.base import BaseCommand

from my_auth.models import Department

class Command(BaseCommand):
  def handle(self, *args, **options):
    data = [('Electronics Development department', None), 
            ('Constructor Development department', None), 
            ('Sales department', None), 
            ('Manufacture department', None), 
            ('Project management department', None), 
            ('Purchase department', None), 
            ('Embedded Software Development Department', 'Department of System Software Development (for microcontrollers eg)'), 
            ('Application Software Development Department', 'Department of Application Software Development (desktop, web eg)'), 
            ('Design department', None), 
            ('Marketing department', None)]
    for dev, desc in data:
      Department.objects.create(name=dev, description=desc)