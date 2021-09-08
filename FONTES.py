Created by Roberto Sá on 26/04/2021


import random
import pulp as plp
import pandas as pd



#PASSO 1: DEFINIR A DIMENSÃO DAS MATRIZES
n = 10
m = 5

#PASSO 2: ALOCAR COEFICIENTE PARA AS MATRIZES
set_I = range(1, n+1)
set_J = range(1, m+1)
c = {(i,j): random.normalvariate(0,1) for i in set_I for j in set_J}
a = {(i,j): random.normalvariate(0,5) for i in set_I for j in set_J}
l = {(i,j): random.randint(0,10) for i in set_I for j in set_J}
u = {(i,j): random.randint(10,20) for i in set_I for j in set_J}
b = {j: random.randint(0,30) for j in set_J}



#PASSO 3: CRIO O 'OBJETO' PARA SER OTIMIZADO
opt_model = plp.LpProblem(name="MIP Model")

#PASSO 4: CÓDIGO ABAIXO DEFINIÇÃO DO VALOR DE CADA VARIÁVEL

'''''
# if x is Continuous
x_vars  = {(i,j):
plp.LpVariable(cat=plp.LpContinuous,
               lowBound=l[i,j], upBound=u[i,j],
               name="x_{0}_{1}".format(i,j))
for i in set_I for j in set_J}
# if x is Binary
x_vars  = {(i,j):
plp.LpVariable(cat=plp.LpBinary, name="x_{0}_{1}".format(i,j))
for i in set_I for j in set_J}
# if x is Integer
x_vars  = {(i,j):
plp.LpVariable(cat=plp.LpInteger,
               lowBound=l[i,j], upBound= u[i,j],
               name="x_{0}_{1}".format(i,j))
for i in set_I for j in set_J}
'''''


#PASSO 5 DEFINIR O SINAL " <  >  <=   >=  = "


# Less than equal constraints
''''
constraints = {j : opt_model.addConstraint(
plp.LpConstraint(
             e=plp.lpSum(a[i,j] * x_vars[i,j] for i in set_I),
             sense=plp.LpConstraintLE,
             rhs=b[j],
             name="constraint_{0}".format(j)))
       for j in set_J}
# >= constraints
constraints = {j : opt_model.addConstraint(
plp.LpConstraint(
             e=plp.lpSum(a[i,j] * x_vars[i,j] for i in set_I),
             sense=plp.LpConstraintGE,
             rhs=b[j],
             name="constraint_{0}".format(j)))
       for j in set_J}
# == constraints
constraints = {j : opt_model.addConstraint(
plp.LpConstraint(
             e=plp.lpSum(a[i,j] * x_vars[i,j] for i in set_I),
             sense=plp.LpConstraintEQ,
             rhs=b[j],
             name="constraint_{0}".format(j)))
       for j in set_J}
'''''

#PASSO 6: MONTAR A LINHA OBJETIVO

objective = plp.lpSum(x_vars[i,j] * c[i,j]
                    for i in set_I
                    for j in set_J)

#PASSO 7: DEFINIR SE O PROBLEMA É MAXIMIZAÇÃO OU MINIMIZAÇÃO

'''''
# for maximization
opt_model.sense = plp.LpMaximize
# for minimization
opt_model.sense = plp.LpMinimize


opt_model.setObjective(objective)
'''''

#PASSO 8: SOLUCIONAR O PROBLEMA(SOLVER)

'''''
# solving with CBC
opt_model.solve()
# solving with Glpk
opt_model.solve(solver = GLPK_CMD())
'''''


#PASSO 9: UTILIZAR A BIBLIOTECA PANDAS PARA O PÓS PROCESSAMENTO

'''''
opt_df = pd.DataFrame.from_dict(x_vars, orient="index", 
                                columns = ["variable_object"])
opt_df.index = 
     pd.MultiIndex.from_tuples(opt_df.index, 
                               names=["column_i", "column_j"])
opt_df.reset_index(inplace=True)
# Gurobi
opt_df["solution_value"] = 
  opt_df["variable_object"].apply(lambda item: item.X)
# CPLEX
opt_df["solution_value"] = 
  opt_df["variable_object"].apply(lambda item: item.solution_value)
# PuLP
opt_df["solution_value"] = 
  opt_df["variable_object"].apply(lambda item: item.varValue)
opt_df.drop(columns=["variable_object"], inplace=True)
opt_df.to_csv("./optimization_solution.csv")
'''''