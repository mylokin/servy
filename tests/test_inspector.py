from __future__ import absolute_import

import unittest

import servy.inspector


class Empty(object):
    pass


class Dummy(object):
    def fn(self):
        pass


class Map(object):
    m = {'fn': lambda x: x}


class Service(servy.inspector.Container):
    def __call__(self):
        pass

srv = Service()


class Inception(object):
    service = srv

    class A1(servy.inspector.Container):
        class A2(servy.inspector.Container):
            class A3(servy.inspector.Container):
                class A4(servy.inspector.Container):
                    class A5(servy.inspector.Container):
                        @classmethod
                        def fn(cls):
                            pass


class ServiceDetection(unittest.TestCase):
    def test_lambda(self):
        assert servy.inspector.Inspector.is_procedure(lambda x: x)

    def test_method(self):
        assert servy.inspector.Inspector.is_procedure(Dummy().fn)

    def test_callable_class_service(self):
        assert not servy.inspector.Inspector.is_procedure(Service())

    def test_type(self):
        assert not servy.inspector.Inspector.is_procedure(dict)

    def test_int(self):
        assert not servy.inspector.Inspector.is_procedure(1)

    def test_string(self):
        assert not servy.inspector.Inspector.is_procedure("1")

    def test_dummy_class(self):
        assert not servy.inspector.Inspector.is_procedure(Dummy)


class ContainerDetection(unittest.TestCase):
    def test_dict(self):
        assert servy.inspector.Inspector.is_container({})

    def test_service_class(self):
        assert servy.inspector.Inspector.is_container(Service)

    def test_service_class_instance(self):
        assert servy.inspector.Inspector.is_container(Service())

    def test_dummy_class(self):
        assert not servy.inspector.Inspector.is_container(Dummy)


class PublicMethodsDetection(unittest.TestCase):
    def test_double_underscores(self):
        items = {
            '__private': None,
        }
        assert servy.inspector.Inspector.get_public(items.items()) == {}

    def test_single_underscores(self):
        items = {
            '_private': None,
        }
        assert servy.inspector.Inspector.get_public(items.items()) == {}


class Analyze(unittest.TestCase):
    def test_dummy_object(self):
        containers, services = servy.inspector.Inspector.analyze(Dummy)
        assert containers == {}
        assert services == {'fn': Dummy.fn}

    def test_dummy_instance_object(self):
        dummy = Dummy()
        containers, services = servy.inspector.Inspector.analyze(dummy)
        assert containers == {}
        assert services == {'fn': dummy.fn}

    def test_empty_object(self):
        containers, services = servy.inspector.Inspector.analyze(Empty)
        assert containers == {}
        assert services == {}

    def test_map(self):
        containers, services = servy.inspector.Inspector.analyze(Map)
        assert containers == {'m': Map.m}
        assert services == {}

    def test_map_instance(self):
        m = Map()
        containers, services = servy.inspector.Inspector.analyze(m)
        assert containers == {'m': m.m}
        assert services == {}

    def test_dict(self):
        container = {'fn': lambda x: x}
        containers, services = servy.inspector.Inspector.analyze(container)
        assert containers == {}
        assert services == {'fn': container['fn']}


class ServiceFinder(unittest.TestCase):
    def test_dummy(self):
        services = servy.inspector.Inspector.find(Dummy)
        assert services == {'fn': Dummy.fn}

    def test_dummy_instance(self):
        dummy = Dummy()
        services = servy.inspector.Inspector.find(dummy)
        assert services == {'fn': dummy.fn}

    def test_empty(self):
        services = servy.inspector.Inspector.find(Empty)
        assert services == {}

    def test_map(self):
        services = servy.inspector.Inspector.find(Map)
        assert services == {'m.fn': Map.m['fn']}

    def test_service(self):
        services = servy.inspector.Inspector.find(Inception)
        assert services == {}
