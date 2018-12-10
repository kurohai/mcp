from munch import Munch
from munch import unmunchify
from flask_restplus import Model
from flask_restplus import OrderedModel
from flask_restplus import Resource
from pytuya import Device as TuyaDevice
import simplejson

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


# class Outlet(Device):
#     """docstring for OutletDevice"""
#     def __init__(self, dev_id, address, local_key=None):
#         dev_type = 'outlet'
#         super(OutletDevice, self).__init__(dev_id, address, local_key=None)
#         self.ip = ip
#         self.dev_id = dev_id
#         self.localkey = localkey



class OutletDevice(TuyaDevice, Munch):
    """docstring for OutletDevice"""

    def __init__(self, dev_id, address, local_key=None, name='', **kwargs):
        dev_type = 'outlet'
        super(OutletDevice, self).__init__(dev_id, address, local_key, dev_type)
        self.name = name or address
        self.address = address
        # self.dev_id = dev_id
        self.local_key = local_key
        if 'group' in kwargs.keys():
            self.group = kwargs.pop('group')
        else:
            self.group = 'NoGroup'

    # def __repr__(self):
        # for k, v in self.
        # return str(Munch(self).toDict())

class OutletGroup(Munch):
    """docstring for OutletGroup"""
    def __init__(self, name):
        super(OutletGroup, self).__init__()
        self.name = name
        self.devices = Munch()

    def add_device(self, device):
        self.devices[device.name] = device

    def list_devices(self):
        print self.devices.toDict()
        return unmunchify(self.devices)

    def get_device(self, name):
        return self.toDict()

    def get_group_by_name(self, name):
        if self.name == name:
            return self

    def add_group(self, group):
        self[group.name] = group



class GroupList(Munch):
    """docstring for GroupList"""
    def __init__(self, name):
        super(GroupList, self).__init__()
        self.name = name

    def add_group(self, group):
        self[group.name] = group




# class OutletDevice(Device, Munch):
#     """docstring for OutletDevice"""

#     def __init__(self, dev_id, address, local_key=None):
#         dev_type = 'device'
#         super(OutletDevice, self).__init__(dev_id, address, local_key, dev_type)


#     def get(self):
#         for todo in self.todos:
#             if todo['id'] == id:
#                 return todo
#         api.abort(404, "Todo {} doesn't exist".format(id))

#     def create(self, data):
#         todo = data
#         todo['id'] = self.counter = self.counter + 1
#         self.todos.append(todo)
#         return todo

#     def update(self, id, data):
#         todo = self.get(id)
#         todo.update(data)
#         return todo

#     def delete(self, id):
#         todo = self.get(id)
#         self.todos.remove(todo)
