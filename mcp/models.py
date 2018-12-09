from bunch import Bunch
from bunch import bunchify
from flask_restplus import Model
from flask_restplus import OrderedModel
from flask_restplus import Resource

device_count = int()


class ModelMixin(object):
    """docstring for ModelMixin"""

    def __init__(self):
        super(ModelMixin, self).__init__(*args, **kwargs)

    def _new_id(self):
        global device_count
        device_count += 1
        return device_count

    def _format_device_name(self, n):
        n = str(n)
        n = n.lower()
        n = n.strip()
        n = n.replace(' ', '-')
        n = n.replace('_', '-')
        return n


class Device(OrderedModel, ModelMixin):
    """docstring for Device"""

    def __init__(self, name, *args, **kwargs):
        super(Device, self).__init__(name, *args, **kwargs)
        for k, v in kwargs.items():
            self[self._format_device_name(k)] = v
        self.id = self._new_id()

    def __unicode__(self):
        return str(self.items())

    def __str__(self):
        return self.__unicode__()


class DeviceList(Model, ModelMixin):
    """docstring for DeviceList"""

    def __init__(self, group_name, *kwarg, **kwargs):
        super(DeviceList, self).__init__(group_name)
        self.group_name = self._format_device_name(group_name)
        self.device_count = int()

    def add_device(self, device):
        self.device_count += 1
        device.id = self.device_count
        self[device.name] = device

    def get_device(self, device_name):
        return self[device_name]
