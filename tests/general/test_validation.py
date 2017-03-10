#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Bruno Stuyts'

import unittest
import numpy as np
from pyeng.general.validation import ValidationDecorator, validate_float, validate_integer, validate_string, \
    validate_boolean, validate_list, map_args

VALIDATION_DATA = {
    'a': {'type':'float','min_value':0.0,'max_value':1.0},
    'b': {'type':'string','options':('bruno','stuyts'),'regex':None},
    'c': {'type':'float','min_value':None,'max_value':None},
    'd': {'type':'list','elementtype':'float','order':'ascending','unique':True,'empty_allowed':True}
}

class Test_validate_float(unittest.TestCase):

    def test_nonfloat(self):
        example_string = "abcd"
        self.assertRaises(TypeError,validate_float,"example_string",example_string)
        example_dict = {'1': 2.5, '2': 'abc'}
        self.assertRaises(TypeError,validate_float,"example_dict",example_dict)
        example_tuple = (1.0,2.0,3.0)
        self.assertRaises(TypeError,validate_float,"example_tuple",example_tuple)
        example_list = [1.0,2.0,3.0]
        self.assertRaises(TypeError,validate_float,"example_list",example_list)

    def test_nan(self):
        self.assertEqual(validate_float("example_float",np.NaN),True)

    def test_float(self):
        example_float = 1.1
        self.assertEqual(validate_float("example_float",example_float),True)

    def test_min(self):
        value = 5.0
        min_value = 10.0
        self.assertRaises(ValueError,validate_float,"example_float",value,min_value=min_value)

    def test_max(self):
        value = 10.0
        max_value = 5.0
        self.assertRaises(ValueError,validate_float,"example_float",value,max_value=max_value)

    def test_range(self):
        value = 10.0
        max_value = 5.0
        min_value = 1.0
        self.assertRaises(ValueError,validate_float,"example_float",value,min_value=min_value,max_value=max_value)
        value = 0
        self.assertRaises(ValueError,validate_float,"example_float",value,min_value=min_value,max_value=max_value)


class Test_validate_integer(unittest.TestCase):

    def test_noninteger(self):
        example_string = "abcd"
        self.assertRaises(TypeError,validate_integer,"example_string",example_string)
        example_dict = {'1': 2.5, '2': 'abc'}
        self.assertRaises(TypeError,validate_integer,"example_dict",example_dict)
        example_tuple = (1.0,2.0,3.0)
        self.assertRaises(TypeError,validate_integer,"example_tuple",example_tuple)
        example_list = [1.0,2.0,3.0]
        self.assertRaises(TypeError,validate_integer,"example_list",example_list)
        example_nonint = 1.2
        self.assertRaises(TypeError,validate_integer,"example_nonint",example_nonint)

    def test_integer(self):
        example_int = 1
        self.assertEqual(validate_integer("example_int",example_int),True)

    def test_nan(self):
        self.assertEqual(validate_float("example_float",np.NaN),True)

    def test_min(self):
        value = 5
        min_value = 10
        self.assertRaises(ValueError,validate_integer,"example_integer",value,min_value=min_value)

    def test_max(self):
        value = 10
        max_value = 5
        self.assertRaises(ValueError,validate_integer,"example_integer",value,max_value=max_value)

    def test_range(self):
        value = 10
        max_value = 5
        min_value = 1
        self.assertRaises(ValueError,validate_integer,"example_integer",value,min_value=min_value,max_value=max_value)
        value = 0
        self.assertRaises(ValueError,validate_integer,"example_integer",value,min_value=min_value,max_value=max_value)


class Test_validate_boolean(unittest.TestCase):

    def test_nonboolean(self):
        example_string = "abcd"
        self.assertRaises(TypeError,validate_boolean,"example_string",example_string)
        example_dict = {'1': 2.5, '2': 'abc'}
        self.assertRaises(TypeError,validate_boolean,"example_dict",example_dict)
        example_tuple = (1.0,2.0,3.0)
        self.assertRaises(TypeError,validate_boolean,"example_tuple",example_tuple)
        example_list = [1.0,2.0,3.0]
        self.assertRaises(TypeError,validate_boolean,"example_list",example_list)
        example_float = 1.2
        self.assertRaises(TypeError,validate_boolean,"example_nonint",example_float)

    def test_boolean(self):
        example_boolean = True
        self.assertEqual(validate_boolean("example_boolean",example_boolean),True)


class Test_validate_string(unittest.TestCase):

    def test_nonstring(self):
        example_int = 10
        self.assertRaises(TypeError,validate_string,"example_int",example_int)
        example_dict = {'1': 2.5, '2': 'abc'}
        self.assertRaises(TypeError,validate_string,"example_dict",example_dict)
        example_tuple = (1.0,2.0,3.0)
        self.assertRaises(TypeError,validate_string,"example_tuple",example_tuple)
        example_list = [1.0,2.0,3.0]
        self.assertRaises(TypeError,validate_string,"example_list",example_list)
        example_float = 1.2
        self.assertRaises(TypeError,validate_string,"example_nonint",example_float)

    def test_string(self):
        example_string = "Bruno Stuyts"
        self.assertEqual(validate_string("example_string",example_string),True)

    def test_options(self):
        example_list = ('first','second','third')
        example_string = "fourth"
        self.assertRaises(ValueError,validate_string,"example_string",example_string,options=example_list)
        example_list = ['first','second','third']
        example_string = "fourth"
        self.assertRaises(ValueError,validate_string,"example_string",example_string,options=example_list)
        example_string = 'third'
        self.assertEqual(validate_string("example_string",example_string,options=example_list),True)

    def test_regex(self):
        example_regex = "^[a-z]+"
        example_string = "bruno"
        self.assertEqual(validate_string("example_string",example_string,regex=example_regex),True)
        example_string = "Bruno"
        self.assertRaises(ValueError,validate_string,"example_string",example_string,regex=example_regex)
        example_string = "123"
        self.assertRaises(ValueError,validate_string,"example_string",example_string,regex=example_regex)


class Test_validate_list(unittest.TestCase):

    def test_nonlist(self):
        example_int = 10
        self.assertRaises(TypeError,validate_list,"example_int",example_int)
        example_dict = {'1': 2.5, '2': 'abc'}
        self.assertRaises(TypeError,validate_list,"example_dict",example_dict)
        example_string = "bruno"
        self.assertRaises(TypeError,validate_list,"example_string",example_string)
        example_float = 1.2
        self.assertRaises(TypeError,validate_list,"example_float",example_float)

    def test_list(self):
        example_list = [1.0,2.0,3.0]
        self.assertEqual(validate_list("example_list",example_list),True)
        example_tuple = (1.0,2.0,3.0)
        self.assertEqual(validate_list("example_tuple",example_tuple),True)

    def test_elementtype(self):
        example_list = [1.0,2.0,3.0]
        self.assertEqual(validate_list("example_list",example_list,elementtype="float"),True)
        example_list = [1.0,"a",3.0]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,elementtype="float")
        example_list = [1.0,2.2,3.0]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,elementtype="int")
        example_list = [1,2,3]
        self.assertEqual(validate_list("example_list",example_list,elementtype="int"),True)
        example_list = ['a','b','c']
        self.assertEqual(validate_list("example_list",example_list,elementtype="string"),True)
        example_list = ['a',2.2,'c']
        self.assertRaises(ValueError,validate_list,"example_list",example_list,elementtype="string")

    def test_ascending(self):
        example_list = [1.0,2.0,3.0]
        self.assertEqual(validate_list("example_list",example_list,order="ascending"),True)
        example_list = [1.0,3.0,2.0]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,order="ascending")
        example_list = [np.NaN,3.0,2.0]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,order="ascending")
        example_list = [3.0,np.NaN,2.0]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,order="ascending")

    def test_descending(self):
        example_list = [3.0,2.0,1.0]
        self.assertEqual(validate_list("example_list",example_list,order="descending"),True)
        example_list = [2.0,3.0,1.0]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,order="descending")
        example_list = [3.0,2.0,np.NaN]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,order="descending")
        example_list = [3.0,np.NaN,2.0,1.0,]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,order="descending")

    def test_unique(self):
        example_list = [3.0,2.0,1.0]
        self.assertEqual(validate_list("example_list",example_list,unique=True),True)
        example_list = [3.0,3.0,1.0]
        self.assertRaises(ValueError,validate_list,"example_list",example_list,unique=True)

    def test_empty(self):
        example_list = []
        self.assertEqual(validate_list("example_list",example_list),True)
        self.assertRaises(ValueError,validate_list,"example_list",example_list,empty_allowed=False)


class Test_map_args(unittest.TestCase):

    def setUp(self):
        self.validation_data = {
            'a': {'type':'float','min_value':0.0,'max_value':1.0},
            'b': {'type':'string','options':None,'regex':None},
            'c': {'type':'float','min_value':None,'max_value':None},
        }

        def test_func(a, b, c=1.0):
            pass
        self.test_func = test_func

    def test_mapping(self):
        mapped_data = map_args(self.test_func,self.validation_data,0.5,'bruno')
        self.assertEqual(mapped_data['a']['type'],'float')
        self.assertEqual(mapped_data['a']['value'],0.5)
        self.assertEqual(mapped_data['c']['value'],1.0)

    def test_override(self):
        mapped_data = map_args(self.test_func,self.validation_data,0.5,'bruno',a__min=None)
        self.assertEqual(mapped_data['a']['min_value'],None)
        mapped_data = map_args(self.test_func,self.validation_data,0.5,'bruno',a__min=-10.0,a__max=10.0)
        self.assertEqual(mapped_data['a']['min_value'],-10.0)
        self.assertEqual(mapped_data['a']['max_value'],10.0)


class Test_validate(unittest.TestCase):

    def setUp(self):
        @ValidationDecorator(VALIDATION_DATA)
        def test_validated_func(a, b, c=1.0, d=[], **kwargs):

            if not kwargs['validated']:
                raise ValueError("Error during function validation: %s" % kwargs['errorstring'])

            return True
        self.test_validated_func = test_validated_func

        @ValidationDecorator(VALIDATION_DATA)
        def test_fail_silentfunc(a, b, c=1.0, d=[], fail_silently=True, **kwargs):
            try:
                if not kwargs['validated']:
                    raise ValueError("Error during function validation: %s" % kwargs['errorstring'])

                errorval = 1.0 / 0.0
            except Exception as err:
                if fail_silently or fail_silently is None:
                    return np.NaN
                else:
                    raise ValueError("Error during function execution")
        self.test_fail_silentfunc = test_fail_silentfunc

    def test_validate_errors(self):
        self.assertRaises(ValueError,self.test_validated_func,2.0,'bruno')
        self.assertRaises(ValueError,self.test_validated_func,0.5,1.0)
        self.assertRaises(ValueError,self.test_validated_func,0.5,'hendrik')
        self.assertRaises(ValueError,self.test_validated_func,0.5,'bruno',c__min=2.0)
        self.assertRaises(ValueError,self.test_validated_func,0.5,'bruno',c__min=2.0)
        self.assertRaises(ValueError,self.test_validated_func,0.5,'bruno',d=[1.0,'b',3.0])
        self.assertRaises(ValueError,self.test_validated_func,0.5,'bruno',d=[1.0,5.0,3.0])
        self.assertRaises(ValueError,self.test_validated_func,0.5,'bruno',d=[1.0,1.0,3.0])

    def test_validate_correct(self):
        self.assertEqual(bool(self.test_validated_func(0.5,'bruno')),True)
        self.assertEqual(bool(self.test_validated_func(0.5,'bruno',c__min=0.0,c__max=2.0)),True)
        self.assertEqual(bool(self.test_validated_func(0.5,'bruno',c__min=2.0,c__max=3.0,validate=False)),True)
        self.assertEqual(bool(self.test_validated_func(0.5,1.0,validate=False)),True)

    def test_fail_silent(self):
        self.assertRaises(ValueError,self.test_fail_silentfunc,0.0,'bruno',fail_silently=False)
        self.assertEqual(np.isnan(self.test_fail_silentfunc(0.0,'bruno')),True)
