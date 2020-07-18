# TSP_CPLEX_2
 This repository contains sample code for TSP using Python/CPLEX

## Problem Definition
The traveling salesman problem (TSP) consists of a salesman and a set of cities. The salesman has to
visit each one of the cities starting from a certain one (e.g. the hometown) and returning to the
same city. The challenge of the problem ius that the traveling salesman wants to minimize the total
length of the trip. 

https://www.csd.uoc.gr/~hy583/papers/ch11.pdf

## Sample Problem
This problem uses the network example from problem 9.3-1 of the Introduction to Operations Research, 7th edition
textbook by Hillier and Lieberman. 

Textbook pdf: https://notendur.hi.is/kth93/3.20.pdf
  
## Mathematical Formulation
The mathematical formulation is an adaptation of the more general multiple TSP (mTSP) found in the following paper
by Masoumeh Vali and Khodakaram Salimifard:

A Constraint Programming Approach for Solving
Multiple Traveling Salesman Problem: https://ozgurakgun.github.io/ModRef2017/files/ModRef2017_MTSP.pdf 

## Main Files
* `data_arc.csv` = input file for model, distances between cities 
* `TSP.py` = Python model for TSP problem
* `TSP.ipynb` = Jupyter notebook with additional same python model as in TSP.py but with additional notes and images

## Helper Files
* `util.py` = contains helper function used in the `TSP.py` file
* `img_9.3-1_network.png` = image used in Jupyter notebook
* `img_9.3-1_table.png` = image used in Jupyter notebook 

#### Additional notes
* An `output` folder is created when a model script is run. It stores exported csv solutions  

## Instructions
The TSP models in this repository require CPLEX to solve. If you are unable to install CPLEX, you can see a sample of 
the code output in the Jupyter notebook view of this repository or through nbviewer: https://nbviewer.jupyter.org/github/shellei503/TSP_CPLEX_2/blob/master/TSP.ipynb

1. Open TSP.py
2. Update user defined parameters if needed (or leave default values)

* `input_file_name = 'data_arc.csv'`
* `model_name = 'TSP'`
* `output_file_name1 = model_name+'_arc'`
* `output_file_name2 = model_name+'_city'`

3. Run the model using default configurations
4. Review model results in the newly created `output` folder -> `TSP/output`

## Required Environment/Packages/Libraries
* Conda
* Python             (3.7)
* cplex              (12.10.0.1)
* docplex            (2.13.184)

## CPLEX Installation
You must already have CPLEX installed on your machine in order for the following pip install commands to work correctly.  
```
python -m pip install cplex
```
Some models are written using docplex module. Install `docplex` with `pip`
```
python -m pip install docplex
```

## Contact
Please feel free to contact us with any questions, suggestions or comments:
* S. Lei
* slei232@gmail.com
