# -*- coding: UTF-8 -*-
class JSONMixin:
    def to_json(self, exclude_columns=None):
        if exclude_columns is None:
            exclude_columns = {}
        d = {}
        for column in self.__table__.columns:
            if unicode(column.name) in exclude_columns:
                continue
            d[column.name] = getattr(self, column.name)
        return d
