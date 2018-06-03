# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 12:40:12 2017

@author: IukhymchukS
"""

from collections import OrderedDict
from datetime import datetime

from settings import connector


######################################################################################################
# Loading initial data and combining it to list                                                     #
######################################################################################################

class Employee:
    table_name = 'employee'
    fields = ['idEmp', 'fullname', 'dateOfEmp', 'dob']
    primary_key = ('idEmp', {'auto_increment': True})
    # related_class = [Position, Timeoff, InformalVacation, Vacation]
    labels = OrderedDict({'idEmp': ('Id', 3), 'fullname': ('Full Name', 30),
                          'dateOfEmp': ('Employment Date', 20), 'dob': ('Birthday', 10),
                          })
    objects = []

    def __init__(self, **kwargs):
        """
        Object initialization according main table (with primary key)
        """
        for item in self.fields:
            self.__dict__[item] = kwargs.get(item, None)
        Employee.objects.append(self)

    def __str__(self):
        return self.fullname

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    # def __del__(self):
    #     Employee.objects.remove(self)
    #     del self

    def update_parameters(self, **kwargs):
        self.__dict__.update(**kwargs)

    @classmethod
    def get_related_models(cls, *models):
        """
        Return list of related model for this one
        """
        related_models = []
        for model in models:
            try:
                for fk in model.foreign_keys:
                    if cls.primary_key[0] == fk:
                        related_models.append(model)
            except AttributeError:
                pass
        return related_models



class AttributeTable:

    def __init__(self, **kwargs):
        for item in self.fields:
            self[item] = kwargs.get(item, None)
        self.date_of_change = datetime.today().strftime('%Y-%m-%d')
        self.description = 'Information at date of employment'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def update_parameters(self, **kwargs):
        self.__dict__.update(kwargs)



class Position(AttributeTable):

    table_name = 'position'
    fields = ['idEmp', 'prev_pos', 'date_of_change', 'current_pos', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp', ]
    parent_model = Employee
    labels = OrderedDict({'prev_pos': ('Previous position', 15), 'current_pos': ('Position', 15),
                          'date_of_change': ('Date of change', 15),
                          })


class Timeoff(AttributeTable):

    table_name = 'timeoff'
    fields = ['idEmp', 'date_of_change', 'status', 'description', 'timeoff_available', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp', ]
    parent_model = Employee
    labels = OrderedDict({'date_of_change': ('Date of change', 15), 'status': ('Operation', 15),
                          'description': ('Description', 20), 'timeoff_available': ('Timeoff', 10),
                          })


class InformalVacation(AttributeTable):

    table_name = 'informal_vacation'
    fields = ['idEmp', 'date_of_change', 'description', 'informal_vacation_available', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp', ]
    parent_model = Employee
    labels = OrderedDict({'date_of_change': ('Date of change', 15), 'description': ('Description', 20),
                          'informal_vacation_available': ('Informal Vacation', 10),
                          })


class Vacation(AttributeTable):

    table_name = 'vacation'
    fields = ['idEmp', 'date_of_change', 'description', 'vacation_available', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp', ]
    parent_model = Employee
    labels = OrderedDict({'date_of_change': ('Date of change', 15),
                          'description': ('Description', 20),
                          'vacation_available': ('Vacation', 10),
                          })


class Salary(AttributeTable):

    table_name = 'salary'
    fields = ['idEmp', 'previous', 'date_of_change', 'current', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp', ]
    parent_model = Employee
    labels = OrderedDict({'previous': ('Previous salary', 15),
                          'date_of_change': ('Date of change', 15),
                          'current': ('Current salary', 15),
                          })


class Commission(AttributeTable):

    table_name = 'commission'
    fields = ['idEmp', 'comm_percent', 'date_of_change', 'year', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp', 'year', ]
    labels = OrderedDict({'comm_percent': ('Commission percent', 15),
                          'date_of_change': ('Date of change', 15),
                          'year': ('Year', 10),
                          })

    def __init__(self, **kwargs):
        self.year = datetime.now().year
        super().__init__(**kwargs)


class Result:

    table_name = 'result'
    fields = ['year', 'fact_revenue', 'fact_margin', 'plan_revenue', 'plan_margin']
    primary_key = ('year', {'auto_increment': False})
    foreign_key = []
    labels = OrderedDict({'year': ('Year', 10), 'fact_revenue': ('Actual Revenue', 15),
                          'fact_margin': ('Actual Margin', 15),
                          'plan_revenue': ('Planning Revenue', 15),
                          'plan_margin': ('Planning Margin', 15),
                          })
    objects = []

    def __init__(self, **kwargs):
        """
        Object initialization according main table (with primary key)
        """
        for item in self.fields:
            self.__dict__[item] = kwargs.get(item, None)
        if not self[Result.primary_key[0]]:
            self.year = datetime.now().year
        Result.objects.append(self)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


model_list = [Employee, Position, Timeoff, InformalVacation, Vacation, Salary, Commission, Result]
if __name__ == '__main__':
    pass
