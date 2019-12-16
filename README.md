# SampleSome
DSL-like data sampling library for Python 3.
## Example - Zoo datase
Let's assume that we need to generate a dataset containing of animals in the zoo. Each animal has: Id, ZooName, Type, Name, DaysInZoo, Weight, Age, Popularity (number of guests per day).
Samplesome library provides a fluent-style API to generate a table of data. THere are three steps:
1. Create a model;
2. Configure fields by providing name, type and generator;
3. Generate data;
### Create a model
Firstly, creating a model is as simple as:
```python
animal = Model("Animal")
```
### Configure fields
We can use the following field types:
- String
- Integer
- Float
#### Autoincrement field
Lets generate values like: A_1, A_2, ...
```python
animal.Field("Id", String().Autoincrement("A_", 1))
```
#### Constant value generator
Zoo name will be fixed:
```python
animal.Field("ZooName", String().Const("Jardin des plantes"))
```
#### Random choice from a set of values
```python
animal.Field("Type", String().Choice(['Bear', 'Kangoo', 'Pig', 'Snake', 'Cat']))
```
*Weights also can be provided.*
#### Derivative fields
Derivative field computed from the fields declared before. We will generate names for animals comprising some random alias and animal type, which was already generated.
```python
from random import choice
aliases = ['Angry', 'Shiny', 'Chatty', 'Sad']
animal.Field("Name", String().Derivative(lambda fields: f"{choice(aliases)} {fields['Type']}"))
```
#### Parametrized probability distibution
```python
animal \
    .Field("Popularity", Integer().Exponential(scale=20.0)) \
    .Field("DaysInZoo", Integer().Normal(mu=150, sigma=50))
```
#### Conditional fields
Condition is a special type of derivative field, which allows defining a predicate and corresponding generator. We know that the weight of an animal depends on its type.
```python
animal.Field("Weight", Float()
						 .Condition(lambda fields: fields["Type"] == 'Bear', lambda f: f.Normal(mu=50, sigma=10, minf=10))
						 .Condition(lambda fields: fields["Type"] == 'Kangoo', lambda f: f.Normal(mu=30, sigma=5, minf=5))
						 .Condition(lambda fields: fields["Type"] in ['Pig', 'Cat'], lambda f: f.Normal(mu=5, sigma=1, minf=1))
						 .Condition(lambda fields: fields["Type"] == 'Snake', lambda f: f.Exponential(scale=2, minf=1))
						 .Condition(lambda fields: True, lambda f: f.Const(NAN)))
```
Take into account that min and max values may be limited to [minf:maxf].
#### Probability distibution can be defined in form of KDE
```python
animal.Field("Age", Float().Kde([1.2, 2.3, 3.3, 3.2, .4, 5.6, 1.1, 1.0, 2.0, 2.1, 3.5, 6.7, 4.4, 7.7, 2.2, 5.5, 6.6, 1.2, 3.4, 9.0, 0.1, 3.2, 1.3, 2.5, 2.7], minf=0))
```
### Data generation
Generate 1000 animals and export as csv:
animal.GenerateToCsv(1000, "FLO.csv")
