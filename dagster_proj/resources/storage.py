from dagster import ConfigurableResource
import os

class MyStorage(ConfigurableResource):
    path: str

    def get_last_update_time(self):
        return os.path.getmtime(self.path)