# application/tools/db.py

#import base64
import copy
import urllib

from google.cloud import datastore

client = datastore.Client()


class Property:
    def __init__(self, code=None, indexed=True, default=None):
        self._name = None
        self._code = code
        self._indexed = indexed
        self._default = default     # Set to 0 for numeric values


class MetaModel(type):
    """ metaclass for Model """
    def __new__(cls, cls_name, bases, attrs):
        new_attrs = {}
        _properties = {}
        codes = []
        for name, attr in attrs.items():
            if isinstance(attr, Property):
                if attr._code in codes:
                    raise Exception(
                        'Error! Duplicate property code.', attr._code)
                else:
                    codes.append(attr._code)
                    _properties[name] = attr
            else:
                new_attrs[name] = attr
        new_attrs['_properties'] = _properties
        return type.__new__(cls, cls_name, bases, new_attrs)


class Model(metaclass=MetaModel):
    
    def __init__(self, name=None):

        kind = self.__class__.__name__
        if name:
            self.key = client.key(kind, name)
        else:
            self.key = client.key(kind)

        for name, prop in self._properties.items():
            if name in dir(self):
                raise Exception('Error! Duplicate attribute name.', name)
            else:
                setattr(self, name, prop._default)

    def add(self, attrs):
        self.__dict__.update(attrs)

    def put(self):
        excludes = []
        values = {}
        for name, prop in self._properties.items():
            if prop._indexed is False:
                excludes.append(prop._code)
            values[prop._code] = getattr(self, name)
        entity = datastore.Entity(
            self.key,
            exclude_from_indexes=excludes,
        )
        entity.update(values)
        client.put(entity)
        return entity.key

    @classmethod
    def get(cls, id):
        instance = cls(id)
        entity = client.get(instance.key)
        if entity:
            for name, prop in  instance._properties.items():
                if prop._code in entity:
                    instance.__dict__[name] = entity[prop._code]
        else:
            instance = None
        return instance


    @classmethod
    def delete(cls, id):
        key = client.key(cls.__name__, id)
        client.delete(key)
        return "ok"


    @classmethod
    def delete_multi(cls, keys):
        client.delete_multi(keys)
        return "ok"


    @classmethod
    def search(cls, params, **options):
        
        curs = None
        limit = 5
        
        query = client.query()
        query.kind = cls.__name__
        properties = cls._properties

        _params = copy.deepcopy(params)
        _params.update(options)

        for key, vals in _params.items():
            vals = vals if isinstance(vals, list) else [vals]
            # filter #
            if key in properties and properties[key]._indexed:
                default = properties[key]._default
                code = properties[key]._code
                for val in vals:
                    val = int(val) if isinstance(default, int) else val
                    query.add_filter(code, "=", val)

            # order #
            if key == 'order':
                orders = []
                for order in vals:
                    sign = ""
                    if order[0] == "-":
                        sign = "-"
                        order = order[1:]
                    if order in properties and properties[order]._indexed:
                        orders.append(sign + properties[order]._code)
                query.order = orders

            # cursor #
            if key == 'curs':
                #curs = q_params['curs'][0].encode('utf-8')
                curs = vals[0].encode('utf-8')

            # limit #
            if key == 'limit':
                #limit = int(q_params['limit'][0])
                limit = int(vals[0])

        query_iter = query.fetch(start_cursor=curs, limit=limit)

        results = []
        for entity in query_iter:
            instance = cls()
            instance.key = entity.key
            for name, prop in  instance._properties.items():
                if prop._code in entity:
                    setattr(instance, name, entity[prop._code])
            results.append(instance)

        q_string = None
        if query_iter.next_page_token:
            params['curs'] = query_iter.next_page_token.decode('utf-8')
            q_string = "?" + urllib.parse.urlencode(params, doseq=True)

        return (results, q_string)


    @classmethod
    def gql(cls, q_str, **q_options):
        """ GQL Format
        SELECT [* | <column list> | __key__]
          [FROM <kind>]
          [WHERE <condition> [AND <condition> ...]]
          [ORDER BY <column> [ASC | DESC] [, <column> [ASC | DESC] ...]]
          [LIMIT <count>]
        https://googleapis.github.io/google-cloud-python/latest/datastore/queries.html
        """
        _properties = cls._properties
        query = client.query()

        for word in ['FROM', 'WHERE', 'ORDER', 'LIMIT', 'OFFSET']:
            q_str = q_str.replace(word, '\n' + word)

        clauses = q_str.splitlines()
        for clause in clauses:
            word = clause.split()[0]

            if word == 'SELECT':
                columns = clause[6:].replace(' ', '').split(',')
                if columns[0] == '__key__':
                    query.keys_only()
                elif columns[0] != '*':
                    codes = []
                    for column in columns:
                        if column in _properties:
                            code = _properties[column]._code
                            codes.append(code)
                    query.projection = codes

            if word == 'FROM':
                query.kind = clause[4:].strip()

            if word == 'WHERE':
                conditions = clause[5:].split('AND')
                for condition in conditions:
                    vals = condition.split()
                    column = vals[0]
                    operator = vals[1]
                    value = vals[2]
                    if value.startswith("'"):
                        value = value.replace("'", "")
                    elif value.isdecimal():
                        value = int(value)
                    if column in _properties:
                        code = _properties[column]._code
                        query.add_filter(code, operator, value)

            if word == 'ORDER':
                items = clause[8:].split(',')
                orders = []
                for item in items:
                    vals = item.split()
                    column = vals[0]
                    if column in _properties:
                        order = _properties[column]._code
                        if len(vals) == 2 and vals[1] == 'DESC':
                            order = '-' + order
                        orders.append(order)
                query.order = orders

            if word == 'LIMIT':
                q_options['limit'] = int(clause[5:].strip())

        query_iter = query.fetch(**q_options)

        results = []
        for entity in query_iter:
            instance = cls()
            instance.key = entity.key
            for name, prop in  instance._properties.items():
                if prop._code in entity:
                    setattr(instance, name, entity[prop._code])
            results.append(instance)

        next_cursor = query_iter.next_page_token

        return (results, next_cursor)


    @classmethod
    def fetch(cls, keys_only=False, **q_options):
        """ Datastore fetch
        keys_only = True/False
        q_options = {
            'curs': next_cursor,
            'limit': 10,
            'order': "-created",
        }
        can't use filter
        url_query = "?" + urllib.parse.urlencode(q_options, doseq=True)
        """

        curs = None
        limit = 10

        query = client.query()
        query.kind = cls.__name__
        properties = cls._properties

        if keys_only:
            query.keys_only()

        for key, val in q_options.items():

            # order #
            if key == 'order':
                if val[0] == "-":
                    sign = "-"
                    name = val[1:]
                else:
                    sign = ""
                    name = val
                if name in properties and properties[name]._indexed:
                    order = sign + properties[name]._code
                    query.order = order

            # cursor #
            if key == 'curs':
                curs = val

            # limit #
            if key == 'limit':
                limit = int(val)

        query_iter = query.fetch(start_cursor=curs, limit=limit)

        #if keys_only:
        #    results = [entity.key for entity in query_iter]
        #else:

        results = []
        for entity in query_iter:
            instance = cls()
            instance.key = entity.key
            for name, prop in  instance._properties.items():
                if prop._code in entity:
                    setattr(instance, name, entity[prop._code])
            results.append(instance)

        url_query = None
        if query_iter.next_page_token:
            q_options['curs'] = query_iter.next_page_token.decode('utf-8')
            #url_query = "?" + urllib.parse.urlencode(q_options, doseq=True)

        return (results, q_options)        #url_query)

        
        '''
        curs = None
        limit = 5
        
        query = client.query()
        query.kind = cls.__name__
        properties = cls._properties

        _params = copy.deepcopy(params)
        _params.update(options)

        for key, vals in _params.items():
            vals = vals if isinstance(vals, list) else [vals]
            # filter #
            if key in properties and properties[key]._indexed:
                default = properties[key]._default
                code = properties[key]._code
                for val in vals:
                    val = int(val) if isinstance(default, int) else val
                    query.add_filter(code, "=", val)

            # order #
            if key == 'order':
                orders = []
                for order in vals:
                    sign = ""
                    if order[0] == "-":
                        sign = "-"
                        order = order[1:]
                    if order in properties and properties[order]._indexed:
                        orders.append(sign + properties[order]._code)
                query.order = orders

            # cursor #
            if key == 'curs':
                #curs = q_params['curs'][0].encode('utf-8')
                curs = vals[0].encode('utf-8')

            # limit #
            if key == 'limit':
                #limit = int(q_params['limit'][0])
                limit = int(vals[0])

        query_iter = query.fetch(start_cursor=curs, limit=limit)

        results = []
        for entity in query_iter:
            instance = cls()
            instance.key = entity.key
            for name, prop in  instance._properties.items():
                if prop._code in entity:
                    setattr(instance, name, entity[prop._code])
            results.append(instance)

        q_string = None
        if query_iter.next_page_token:
            params['curs'] = query_iter.next_page_token.decode('utf-8')
            q_string = "?" + urllib.parse.urlencode(params, doseq=True)

        return (results, q_string)
        '''
