#!/usr/bin/env python3


class System:

    req_components = ()

    @classmethod
    def check(cls, entity):
        """Check if entity has necessary components."""
        to_check = list(cls.req_components)
        for component in entity:
            for type in to_check:
                if isinstance(entity, type):
                    to_check.remove(type)
                    break
        if len(to_check) > 0:
            return False
        else:
            return True
