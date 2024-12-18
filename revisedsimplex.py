# -*- coding: utf-8 -*-
"""rsa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eKo2jLQuzbKZUxX4jrpEvYqRILbWBkFg
"""

import numpy as np

def revised_simplex(A, c, b, Eqin, goal='max',M=1000):
    A_rows, A_columns = A.shape
    Eqin_rows, Eqin_columns = Eqin.shape

    if len(c) != A_columns:
        raise ValueError("The length of the cost vector c must be equal to the number of columns in A.")

    if b.size != A_rows:
        raise ValueError("The length of the RHS vector b must be equal to the number of rows in A.")

    if Eqin.size != A_rows:
        raise ValueError("The length of the Eqin vector must be equal to the number of rows in A.")

    if not np.all(np.isin(Eqin, [-1, 0, 1])):
        raise ValueError("Each element of Eqin must be either -1, 0, or 1.")

    if goal not in ['min', 'max']:
        raise ValueError("The goal must be either 'min' for minimization or 'max' for maximization.")


    if(goal=='min'):
      c=-c

    for index,element in enumerate(b):
      if element<0:
        A[index,:]=-A[index,:]
        Eqin[index]=-Eqin[index]
        b[index]=-b[index]


    for index, element in enumerate(Eqin):
        slack_column = np.zeros((A_rows, 1))
        artificial_column=np.zeros((A_rows,1))
        if element == 1:
            slack_column[index] = -1
            artificial_column[index]=1
            A=np.hstack((A,slack_column))
            A=np.hstack((A,artificial_column))
            c=np.append(c,0)
            c=np.append(c,(-1)*M)
        elif element == -1:
            slack_column[index] = 1
            A=np.hstack((A,slack_column))
            c=np.append(c,0)
        elif element == 0:
            artificial_column[index] = 1
            A=np.hstack((A,artificial_column))
            c=np.append(c,(-1)*M)

    B=np.empty((A_rows,0))
    index=A_columns
    bv=[]
    for col in A[:,A_columns:].T:
      col=col.reshape(-1,1)
      if np.any(col==1):
        B = np.hstack((B, col))
        bv.append(index)
      index=index+1

    c_bv=c[bv]
    nbv=[]
    for col_idx in range(A.shape[1]):
      if col_idx not in bv:
        nbv.append(col_idx)

    B_inv = np.linalg.inv(B)

    while True:

        coefficients = np.zeros(len(nbv))
        for i in range(len(nbv)):
            coefficients[i] = (c_bv @ B_inv) @ A[:, nbv[i]] - c[nbv[i]]

        min_coeff, index_min = coefficients.min(), coefficients.argmin()


        if min_coeff >= 0:
            print("Algorithm terminated (Optimal solution found)")
            break


        col = B_inv @ A[:, nbv[index_min]]


        rhs = B_inv @ b
        divs=np.zeros((rhs.size,1))
        for index,element in enumerate(divs):
            if col[index]>0:
              divs[index]=rhs[index]/col[index]
            else:
              divs[index]=np.inf

        if np.all(divs == np.inf):
            print("Problem is unbounded")
            return None

        div_index = divs.argmin()



        Binv_rows,Binv_cols=B_inv.shape
        for i in range(Binv_rows):
          if i!=div_index:
            B_inv[i,:]+=B_inv[div_index,:]*((-1)*(col[i]/col[div_index]))
        B_inv[div_index,:]*=1/col[div_index]


        temp = bv[div_index]
        bv[div_index] = nbv[index_min]
        nbv[index_min] = temp

        c_bv = c[bv]






    optimal_value = (c_bv @ B_inv) @ b
    if goal=='min':
      optimal_value=-optimal_value
    basis_values = B_inv@b
    result_vector=np.zeros((A_columns,1))
    for index,element in enumerate(bv):
      if element<A_columns:
        result_vector[element]=basis_values[index]




    return optimal_value,result_vector


Eqin = np.array(([-1], [-1], [-1]))
b = np.array(([48], [20], [8]))
c = np.array([60, 30, 20])
A = np.array([[8, 6, 1], [4, 2, 1.5], [2, 1.5, 0.5]])

optimal_value,result_vector = revised_simplex(A, c, b, Eqin)
print(optimal_value)
print(result_vector)

Eqin2 = np.array(([-1], [-1], [-1]))
b2 = np.array(([6], [4], [2]))
c2 = np.array([3, 1, 1])
A2 = np.array([[1, 1, 1], [2, 0, -1], [0, 1, 1]])

optimal_value2,result_vector3 = revised_simplex(A2, c2, b2, Eqin2)
print(optimal_value2)
print(result_vector3)

Eqin3 = np.array(([-1], [1], [0]))
b3 = np.array(([11], [3], [-1]))
c3 = np.array([-3, 1, 1])
A3 = np.array([[1, -2, 1], [-4, 1, 2], [2, 0, -1]])

optimal_value3,result_vector3 = revised_simplex(A3, c3, b3, Eqin3,'min')
print(optimal_value3)
print(result_vector3)

import numpy as np

Eqin = np.array(([1], [1], [1], [1]))
b = np.array(([0.2], [0.3], [3], [1.2]))
c = np.array([40,30])
A = np.array([[0.1,0], [0,0.1], [0.5,0.3], [0.1,0.2]])

optimal_value,result_vector=revised_simplex(A,c,b,Eqin,'min')
print("The optimal value is: ")
print(optimal_value)
print("Solution x:")
for index,element in enumerate(result_vector):
  print(f"x{index + 1}: {element[0]}")

import numpy as np

Eqin = np.array(([-1], [-1], [-1]))
b = np.array(([48], [20], [8]))
c = np.array([60, 30, 20])
A = np.array([[8, 6, 1], [4, 2, 1.5], [2, 1.5, 0.5]])

optimal_value,result_vector=revised_simplex(A,c,b,Eqin)
print("The optimal value is: ")
print(optimal_value)
print("Solution x:")
for index,element in enumerate(result_vector):
  print(f"x{index + 1}: {element[0]}")

import numpy as np

Eqin = np.array(([-1], [-1], [-1]))
b = np.array(([6], [4], [2]))
c = np.array([3, 1, 1])
A = np.array([[1, 1, 1], [2, 0, -1], [0, 1, 1]])

optimal_value,result_vector = revised_simplex(A, c, b, Eqin)
print("The optimal value is: ")
print(optimal_value)
print("Solution x:")
for index,element in enumerate(result_vector):
  print(f"x{index + 1}: {element[0]}")

import numpy as np

Eqin = np.array(([-1], [1], [0]))
b = np.array(([11], [3], [-1]))
c = np.array([-3, 1, 1])
A = np.array([[1, -2, 1], [-4, 1, 2], [2, 0, -1]])

optimal_value,result_vector=revised_simplex(A,c,b,Eqin,'min')
print("The optimal value is: ")
print(optimal_value)
print("Solution x:")
for index,element in enumerate(result_vector):
  print(f"x{index + 1}: {element[0]}")

import numpy as np

Eqin = np.array(([-1], [1], [1]))
b = np.array(([4], [6], [6]))
c = np.array([4,4])
A = np.array([[1, 1], [2, 1], [0, 3]])

optimal_value,result_vector=revised_simplex(A,c,b,Eqin)
print("The optimal value is: ")
print(optimal_value)
print("Solution x:")
for index,element in enumerate(result_vector):
  print(f"x{index + 1}: {element[0]}")