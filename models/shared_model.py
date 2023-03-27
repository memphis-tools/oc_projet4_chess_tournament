from datetime import date, datetime


class Information:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if "date" in self._name:
            return instance.__dict__[self._name].strftime("%Y-%m-%d")
        else:
            return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if isinstance(instance, datetime):
            instance.__dict__[self._name] = date.fromisoformat(value.strftime("%Y-%m-%d"))
        else:
            instance.__dict__[self._name] = value
