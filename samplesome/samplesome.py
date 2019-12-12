from __future__ import annotations
import math
import os
import sys
from abc import ABC
from collections import OrderedDict
from typing import List, Callable, Dict, Any, Tuple, Iterable
import random

import numpy
import pandas
from scipy import stats


class Distr(ABC):
    dtype = None

    def __init__(self):
        pass

class DataType(ABC):
    isConditional = False
    isDerivative = False
    conditions: List[Tuple[Callable[[Dict],Any], Callable[[DataType], DataType]]] = []
    cachedConditionalGenerators = {}

    generator: Callable[[], Iterable[Any]] = None
    conditionalGenerator: Callable[[Dict[str, Any]], Iterable[Any]] = None

    def __init__(self, parent = None):
        self.parent = parent

        def default_generator():
            raise Exception("No generator provided")

        self.generator = default_generator

        def default_conditional_generator(fields: Dict[str, Any]):
            condition_index = 0
            for predicate, generator in self.conditions:
                if(predicate(fields)):
                    if(condition_index in self.cachedConditionalGenerators):
                        child_generator = self.cachedConditionalGenerators[condition_index]
                    else:
                        child = self.CreateInstance()
                        child_generator = generator(child)
                        self.cachedConditionalGenerators[condition_index] = child_generator

                    return child_generator.generator
                condition_index += 1

            raise Exception("Not all possible conditions have been provided")

        self.conditionalGenerator = default_conditional_generator

    def CreateInstance(self):
        return DataType(self)

    def Condition(self, predicate: Callable[[Dict],Any], generator: Callable[[DataType], DataType]):
        self.isConditional = True
        self.conditions.append((predicate, generator))
        return self

    def Derivative(self, generator: Callable[[DataType], Any]):
        self.isDerivative = True

        def derivative_generator(fields: Dict[str, Any]):
            value = generator(fields)
            yield value

        self.conditionalGenerator = derivative_generator

        return self

    #def Derivative(self, func: Callable[[Dict],Any]):
    #    return self

    #Computed = Derivative

class String(DataType):
    def __init__(self, parent = None):
        super(String, self).__init__(parent)

    def CreateInstance(self):
        return String(self)

    def Autoincrement(self, prefix: str="", start: int=0):
        def incr():
            i = start
            while(True):
                yield f"{prefix}{str(i)}"
                i+=1

        self.generator = incr()
        return self

    def Const(self, value: str):
        def cst():
            while(True):
                yield value
        self.generator = cst()
        return self

    def Choice(self, values: List[str], weights: List[float]=None):
        def chc():
            while(True):
                yield random.choices(population=values, weights=weights, k=1)[0]
        self.generator = chc()
        return self


class Integer(DataType):

    def __init__(self, parent = None):
        super(Integer, self).__init__(parent)

    def CreateInstance(self):
        return Integer(self)

    def Exponential(self, scale: int):
        def chc():
            while(True):
                yield int(round(numpy.random.exponential(scale=scale, size=1)[0]))
        self.generator = chc()
        return self

    def Uniform(self, min:int, max:int):
        def chc():
            while(True):
                yield random.randint(min, max)
        self.generator = chc()
        return self

    def Choice(self, values: List[int], weights: List[float]=None):
        def chc():
            while(True):
                yield random.choices(population=values, weights=weights, k=1)[0]
        self.generator = chc()
        return self

class Float(DataType):
    def __init__(self, parent = None):
        super(Float, self).__init__(parent)

    def Exponential(self, scale: float):
        def chc():
            while(True):
                yield numpy.random.exponential(scale=scale, size=1)[0]
        self.generator = chc()
        return self

    def Choice(self, values: List[float], weights: List[float]=None):
        def chc():
            while(True):
                yield random.choices(population=values, weights=weights, k=1)
        self.generator = chc()
        return self

    def Gaussian(self, mu: float, sigma: float, minf:float=None, maxf: float=None):
        '''Gaussian distribution'''
        def chc():
            while(True):
                good = False
                while(not good):
                    samp = numpy.random.normal(mu, sigma, 1)[0]
                    good = True
                    if(minf != None and samp <= minf):
                        good=False
                    if(maxf != None and samp >= maxf):
                        good=False
                yield samp

        self.generator = chc()
        return self

    Normal = Gaussian

    def Uniform(self, minf:float, maxf: float):
        '''Uniform distribution'''
        assert maxf > minf
        def chc():
            while(True):
                length = maxf - minf
                yield random.random() * length + minf
        self.generator = chc()
        return self

    def Kde(self, values, minf:float=None, maxf:float=None):
        '''Sampling from KDE built for a given sample'''
        arr = numpy.array(values)
        kernel = stats.gaussian_kde(arr)
        def chc():
            while(True):
                good = False
                while(not good):
                    samp = kernel.resample(1)[0][0]
                    good = True
                    if(minf != None and samp <= minf):
                        good=False
                    if(maxf != None and samp >= maxf):
                        good=False
                yield samp
        self.generator = chc()
        return self

class ModelField():

    def __init__(self, name: str, generator: DataType):
        self.generator = generator
        self.name = name

class Model:

    fields: List[Tuple[str, DataType]] = []

    index = 0

    def __init__(self, name: str=""):
        self.name = name

    def Field(self, name: str, value: DataType):
        assert value != None
        self.fields.append((name, value))
        return self

    def GenerateOne(self) -> dict:
        ret = OrderedDict()
        for name, field in self.fields:
            if(field.isConditional or field.isDerivative):
                value = next(field.conditionalGenerator(ret))
            else:
                value = next(field.generator)
            ret[name] = value
        return ret

    def Generate(self, count:int) -> list:
        assert count >= 0

        ret = []
        for i in range(count):
            ret.append(self.GenerateOne())
        return ret

    def GenerateToCsv(self, count:int, filePath:str):
        import pandas as pd
        ret = self.Generate(count)
        pd.DataFrame.from_dict(ret).to_csv(filePath)