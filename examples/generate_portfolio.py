#----------------------------------------------
# The script generates a portfolio of IR swaps 
# without fixed component (for simplicity)
#----------------------------------------------
import random
import sys
sys.path.append("..")
from samplesome.samplesome import *


#----------------------------------------
# Init random generator
# by default Python 3 used Mersenne Twister
#----------------------------------------
random.seed(44)

#----------------------------------------
# Create a model
#----------------------------------------
floatTadeGenerator = Model("FloatTrade")

#----------------------------------------
# Autoincrement field: T_1, T_2, ...
#----------------------------------------
floatTadeGenerator.Field("TradeId", String().Autoincrement("T_", 1))

#----------------------------------------
# Derivative field computed from the 
# fields declared before: T_1_FLO, T_2_FLO, ...
#----------------------------------------
floatTadeGenerator.Field("ComponentId", String().Derivative(lambda fields: fields["TradeId"] + "_FLO"))

#----------------------------------------
# Field with constant value
#----------------------------------------
floatTadeGenerator.Field("ComponentType", String().Const("FLO"))

#----------------------------------------
# Random choice from a set of values
# weights also can be provided
#----------------------------------------
floatTadeGenerator.Field("NettingSet", String().Choice(['NS1', 'NS2', 'NS3', 'NS4']))

#----------------------------------------
# Fluid api usage is supported
#----------------------------------------
floatTadeGenerator \
	.Field("Party", String().Choice(["MYORG", "MYORG1", "MYORG2"])) \
	.Field("CounterParty", String().Choice(["BANK1", "BANK2"])) \
	.Field("Book", String().Choice(['BOOK1', 'BOOK2', 'BOOK3'])) \
	.Field("Buy", String().Choice(["false", "true"])) \
	.Field("PeriodLength", Integer().Choice([1, 3, 12])) \
	.Field("Currency", String().Const("EUR")) \
	.Field("DiscountIndex", String().Choice(['EUR:EONIA:1D', 'EUR:EURIBOR:3M'])) \
	.Field("FloatIndex", String().Choice(['EUR:EONIA:1D', 'EUR:EURIBOR:1Y', 'EUR:EURIBOR:3M',
													   'EUR:EURIBOR:6M', 'EUR:TAG:1Y', 'EUR:TAM:1Y']))

#----------------------------------------
# Condition is a special type of Derivative field
# <Predicate, Meta-field> -> in meta field you can declare
#----------------------------------------
floatTadeGenerator.Field("CollateralSet", String()
						 .Condition(lambda fields: fields["Party"] == "MYORG" and fields["CounterParty"] == "BANK2",
									lambda s: s.Const('MYORG_BANK2_CSA'))
						 .Condition(
						   lambda fields: fields["Party"] == "MYORG", lambda s: s.Choice([
								'MYORG_CSA1_CSA', 'MYORG_CSA2_CSA', 'MYORG_CSA3_CSA', 'MYORG_CSA4_CSA']))
						 .Condition(lambda fields: fields["Party"] == "MYORG1", lambda f: f.Choice(['MYORG1_DEF_CSA']))
						 .Condition(lambda fields: True, lambda f: f.Const("noCSA")))

#----------------------------------------
# Use a parametrized distibution
#----------------------------------------
floatTadeGenerator.Field("NumberOfPeriods", Integer().Exponential(scale=20.0))
floatTadeGenerator.Field("Spread", Float().Normal(mu=0.0017, sigma=0.003, ))

#----------------------------------------
# ... or a KDE
#----------------------------------------
floatTadeGenerator.Field("Notional", Float().Kde(
   [
	  1.71000000e+08, 1.00000000e+07, 7.50000000e+07, 2.00000000e+07,
	  1.30000000e+08, 1.30000000e+08, 2.17000000e+08, 7.50000000e+07,
	  1.00000000e+07, 3.62000000e+08, 2.60000000e+08, 1.71000000e+08,
	  1.45000000e+08, 3.50000000e+07, 2.50000000e+07, 5.00000000e+06,
	  1.00000000e+07, 1.00000000e+06, 2.60000000e+07, 3.00000000e+06,
	  4.00000000e+08, 1.50000000e+08, 2.10000000e+08, 2.00000000e+07,
	  1.15000000e+08, 5.00000000e+07, 2.00000000e+07, 4.36759259e+07,
	  4.26944444e+07, 4.22037037e+07, 4.12222222e+07, 3.82777778e+07,
	  3.77870370e+07, 2.99351852e+07, 2.40462963e+07, 1.81574074e+07,
	  8.34259259e+06, 4.90740740e+05, 1.50000000e+07, 1.00000000e+08,
	  1.75000000e+08, 5.00000000e+05, 7.50000000e+07, 1.00000000e+06,
	  1.60000000e+07, 7.50000000e+06, 2.60000000e+07, 3.00000000e+07,
	  1.00000000e+07, 1.50000000e+07, 2.50000000e+07, 1.40000000e+07,
	  8.48919297e+06, 8.90771018e+06, 9.34686030e+06, 9.80766051e+06,
	  1.18895144e+07, 1.00000000e+07, 5.00000000e+07, 2.00000000e+07,
	  2.00000000e+07, 2.50000000e+07, 1.50000000e+07, 2.00000000e+07,
	  1.50000000e+07, 1.50000000e+07, 6.00000000e+07, 1.09993631e+06,
	  9.00875560e+05, 4.72397290e+05, 1.97500000e+06, 1.95000000e+06,
	  1.92500000e+06, 1.87500000e+06, 1.82500000e+06, 1.70000000e+06,
	  1.65000000e+06, 1.25000000e+06, 9.50000000e+05, 6.50000000e+05,
	  1.50000000e+05, 2.08555843e+06, 1.70812492e+06, 8.95699270e+05,
	  3.11851831e+06, 2.87262692e+06, 2.37344281e+06, 1.34477210e+06,
	  5.45950310e+05, 1.66666667e+06, 1.33333333e+06, 6.66666670e+05,
	  8.56066988e+07, 8.37289338e+07, 8.16635165e+07, 7.93918060e+07,
	  6.77946497e+07, 5.56854886e+07, 3.95685232e+07, 1.86933246e+07,
	  1.76868145e+07, 1.66377023e+07, 1.55442492e+07, 1.06893520e+07,
	  6.48333951e+06, 1.72234083e+06, 2.26739700e+06, 2.19200600e+06,
	  2.03010100e+06, 1.65644200e+06, 1.32593900e+06, 9.45021000e+05,
	  1.76723000e+05, 1.00000000e+07, 5.00000000e+08, 1.10000000e+08,
	  1.00000000e+07, 1.15000000e+08, 2.50000000e+07, 4.00000000e+07,
	  1.00000000e+07, 2.50000000e+07, 3.00000000e+07, 3.00000000e+07,
	  1.50000000e+07, 1.00000000e+07, 6.00000000e+07, 1.50000000e+07,
	  2.50000000e+07, 2.00000000e+07, 1.40000000e+07, 1.50000000e+07,
	  1.00000000e+07, 2.00000000e+07, 4.36759259e+07, 4.26944444e+07,
	  4.22037037e+07, 4.12222222e+07, 3.82777778e+07, 3.77870370e+07,
	  2.99351852e+07, 2.40462963e+07, 1.81574074e+07, 8.34259259e+06,
	  4.90740740e+05, 4.00000000e+07, 2.50000000e+07, 1.00000000e+07,
	  1.00000000e+07, 3.00000000e+07, 2.50000000e+07, 3.00000000e+07,
	  2.00000000e+07, 5.00000000e+07, 2.50000000e+08, 7.50000000e+07,
	  5.00000000e+05, 1.75000000e+08, 5.18000000e+08, 5.00000000e+05,
	  5.00000000e+05, 7.50000000e+06, 1.60000000e+07, 5.00000000e+06,
	  1.10000000e+08, 5.00000000e+06, 2.08555843e+06, 1.70812492e+06,
	  8.95699270e+05, 1.66666667e+06, 1.33333333e+06, 6.66666670e+05,
	  1.97500000e+06, 1.95000000e+06, 1.92500000e+06, 1.87500000e+06,
	  1.82500000e+06, 1.70000000e+06, 1.65000000e+06, 1.25000000e+06,
	  9.50000000e+05, 6.50000000e+05, 1.50000000e+05, 3.11851831e+06,
	  2.87262692e+06, 2.37344281e+06, 1.34477210e+06, 5.45950310e+05,
	  1.09993631e+06, 9.00875560e+05, 4.72397290e+05, 8.48919297e+06,
	  8.90771018e+06, 9.34686030e+06, 9.80766051e+06, 1.18895144e+07,
	  1.10000000e+08, 2.60000000e+07, 2.60000000e+07, 1.86933246e+07,
	  1.76868145e+07, 1.66377023e+07, 1.55442492e+07, 1.06893520e+07,
	  6.48333951e+06, 1.72234083e+06, 4.00000000e+08, 1.10000000e+08,
	  3.00000000e+06, 5.00000000e+07, 1.50000000e+07, 1.15000000e+08,
	  3.25000000e+08, 2.50000000e+07, 5.00000000e+08, 1.20000000e+08,
	  6.00000000e+07, 1.50000000e+07, 7.00000000e+06, 1.50000000e+07,
	  3.00000000e+06, 2.00000000e+07, 5.00000000e+06, 1.00000000e+06,
	  3.75000000e+08, 8.56066988e+07, 8.37289338e+07, 8.16635165e+07,
	  7.93918060e+07, 6.77946497e+07, 5.56854886e+07, 3.95685232e+07,
	  1.00000000e+08, 2.26739700e+06, 2.19200600e+06, 2.03010100e+06,
	  1.65644200e+06, 1.32593900e+06, 9.45021000e+05, 1.76723000e+05,
	  1.00000000e+07, 1.50000000e+08, 1.00000000e+07, 2.22000000e+08,
	  3.00000000e+07, 2.50000000e+08, 2.00000000e+07, 1.50000000e+07,
	  6.00000000e+07, 3.00000000e+06, 1.50000000e+07, 7.00000000e+06,
	  2.60000000e+07, 5.00000000e+06, 3.75000000e+08, 2.22000000e+08,
	  3.70000000e+07, 3.00000000e+07, 2.80000000e+08, 1.50000000e+08,
	  9.89763377e+07, 2.11216566e+08, 3.37279860e+08, 1.77984795e+08,
	  1.78630029e+08, 3.13558550e+08, 3.01361122e+08, 2.64392569e+08,
	  2.51912939e+08, 1.49316582e+08, 6.90769486e+07, 3.15503703e+08,
	  2.90925964e+08, 2.78495119e+08, 1.76524322e+08, 9.67334353e+07,
	  1.40399148e+07, 5.79870782e+07, 5.81506018e+07, 6.16320267e+07,
	  2.30327679e+08, 2.30854440e+08, 4.54277416e+08, 4.54277416e+08,
	  4.35349190e+08, 2.83923385e+08, 1.70354031e+08, 5.67846770e+07,
	  9.76899652e+07, 6.54566197e+08, 9.67960662e+08, 4.44540399e+08,
	  1.90517314e+08, 1.18961079e+09, 1.10463859e+09, 8.49721993e+08,
	  1.69944398e+08, 1.89830703e+07, 7.50887415e+07, 4.29078523e+07,
	  1.07269631e+07, 1.12577159e+08, 1.13015917e+08, 1.67163193e+08,
	  1.95469462e+08, 1.50000000e+08, 3.00000000e+07, 2.80000000e+08,
	  4.52000000e+08, 4.52000000e+08, 1.50000000e+07, 1.50000000e+07,
	  8.00000000e+07, 8.00000000e+07, 1.10000000e+08, 2.70000000e+07,
	  2.70000000e+07, 7.20000000e+07, 7.20000000e+07, 3.62187500e+07,
	  3.65611983e+07, 4.68866547e+08, 9.88047500e+07, 6.65945464e+08,
	  5.65587482e+08, 4.07425435e+08, 2.39673772e+08, 1.07931875e+08,
	  5.56450388e+08, 4.28967604e+08, 2.94084030e+08, 1.51187570e+08,
	  5.00000000e+07, 1.03312500e+08, 9.29812502e+07, 6.19875001e+07,
	  7.12500002e+06, 1.78125000e+07, 1.42500000e+07, 2.85000001e+07,
	  3.16308177e+07, 6.32616354e+06, 1.00000000e+07, 1.50000000e+08,
	  1.50000000e+08, 5.00000000e+07, 1.00000000e+07, 5.00000000e+07,
	  5.00000000e+07, 1.00000000e+08, 1.00000000e+08, 1.00000000e+07,
	  1.00000000e+07, 3.70000000e+07
   ], minf=0))

#----------------------------------------
# Generate 1000 trades and export as csv
#----------------------------------------
ret = floatTadeGenerator.Generate(1000)
import pandas as pd
df = pd.DataFrame.from_dict(ret)
print(df.to_string())
df.to_csv("FLO.csv")
