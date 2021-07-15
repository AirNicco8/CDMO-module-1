include "globals.mzn";

% INPUT
int: width; % the board width
int: n_rets; % the number of circuits
set of int: RETS = 1..n_rets; 
array[RETS, 1..2] of int: sizes; % the array of sizes (width, heigth) of the circuits

% BOUNDS

% the minimum length is the maximum height size of the input circuits
int: min_l = max([sizes[i,2] | i in RETS]);

% the maximum length is the sum of the heights of the input circuits
int: max_l = sum([sizes[i,2] | i in RETS]);

% array of vars of position 
%that each circuit will take in the solution
array[RETS, 1..2] of var 0..sum([sizes[i,2]| i in RETS]): positions; 

%the length (height) of the board
var min_l..max_l: l;

%decomposition of the size array
array[RETS] of int: size1 = [sizes[i,1]| i in RETS];
array[RETS] of int: size2 = [sizes[i,2]| i in RETS];

%PREDICATES

% given two x or y and the size checks if they overlap
predicate no_overlap(var int:s1, int:d1, var int:s2, int:d2) =
    s1 + d1 <= s2 \/ s2 + d2 <= s1;

%CONSTRAINTS

%variables constraints
%constraint (l = max([positions[i,2] + sizes[i,2] | i in RETS]) /\ area = width*l);

% checks for each group of horizontally overlapped circuits that their sizes sum is less or equal than the width
% constraint forall(i in RETS)
%    	(sizes[i,1] + sum([sizes[k,1] | k in RETS where i != k /\ not(no_overlap(positions[i,2], sizes[i,2], positions[k,2], sizes[k,2]))]) <= width);
% constraint forall(i in RETS)
%         (sizes[i,1]*sizes[i,2] + sum([sizes[k,1] * sizes[k,2] | k in RETS where i != k /\ not(no_overlap(positions[i,2], sizes[i,2], positions[k,2], sizes[k,2]))]) = sizes[i,2] * width);

constraint cumulative([positions[i,2] | i in RETS], size2, size1, width);

constraint cumulative([positions[i,1] | i in RETS], size1, size2, l);

% two circuits can be:
%  not overlapped on any axis
%  overlapped on the x axis or the y axis
%  but not both axis
constraint forall(i,j in RETS where i != j)
   	(no_overlap(positions[i,1], sizes[i,1], positions[j,1], sizes[j,1]) \/ no_overlap(positions[i,2], sizes[i,2], positions[j,2], sizes[j,2]));	
       
% constraint diffn([positions[i,1] | i in RETS],
%                  [positions[i,2] | i in RETS],
%                  size1,
%                  size2);

constraint forall(i in RETS)
 (positions[i,1]+sizes[i,1] <= width);

constraint forall(i in RETS)
 (positions[i,2]+sizes[i,2] <= l);

% constraint forall(i,j in RETS where (i != j /\ positions[i,1] == positions[j,1] /\ sizes[i,1] == sizes[j,1]))

%OBJECTIVE
%var min_l..max_l: l= max([positions[i,2] + sizes[i,2] | i in RETS]);

%search annotation
ann: search_ann = int_search([l]++array1d(positions), first_fail, indomain_min, complete);
ann: search_ann2 = int_search([positions[i,1] | i in RETS], first_fail, indomain_min, complete);

% we want to minimize l
%solve :: seq_search([search_ann, search_ann2]) minimize l;
solve :: search_ann minimize l;
%solve minimize l;