include "globals.mzn";
include "cumulative.mzn";

int: width; % the board width
int: n_rets; % the number of circuits
set of int: RETS = 1..n_rets; 
array[RETS, 1..2] of int: sizes; % the array of sizes (width, heigth) of the circuits

% array of vars of position 
%that each circuit will take in the solution
array[RETS, 1..2] of var 0..sum([sizes[i,2]| i in RETS]): positions; 

%PREDICATES

% given two x or y and the size checks if they overlap
predicate no_overlap(var int:s1, int:d1, var int:s2, int:d2) =
    s1 + d1 <= s2 \/ s2 + d2 <= s1;

%CONSTRAINTS

% there cannot be circuits wider than the plate
constraint forall(i in RETS)
 (sizes[i,1] < width);

constraint forall(i in RETS)
 (positions[i,1]+sizes[i,1] <= width);

 % checks for each group of horizontally overlapped circuits that their sizes sum is less or equal than the width
% constraint forall(i in RETS)
%    	(sizes[i,1] + sum([sizes[k,1] | k in RETS where i != k /\ not(no_overlap(positions[i,2], sizes[i,2], positions[k,2], sizes[k,2]))]) <= width);
%  constraint forall(i in RETS)
%        (sizes[i,1]*sizes[i,2] + sum([sizes[k,1] * sizes[k,2] | k in RETS where i != k /\ not(no_overlap(positions[i,2], sizes[i,2], positions[k,2], sizes[k,2]))]) <= sizes[i,2] * width);
array[RETS] of int: size2 = [sizes[i,2]| i in RETS];
array[RETS] of int: size1 = [sizes[i,1]| i in RETS];

constraint cumulative([positions[i,1] | i in RETS], size2, size1, width);

% two circuits can be:
%  not overlapped on any axis
%  overlapped on the x axis or the y axis
%  but not both axis
constraint forall(i,j in RETS where i != j)
  	(no_overlap(positions[i,1], sizes[i,1], positions[j,1], sizes[j,1]) \/ no_overlap(positions[i,2], sizes[i,2], positions[j,2], sizes[j,2]));
  	


%OBJECTIVE

% the maximum length of a board is the sum of all the heigths of the circuits
% we take the maximum heigth reached by a placed circuit in the board as l
var 0..sum([sizes[i,2]| i in RETS]): l = max([positions[i,2] + sizes[i,2] | i in RETS]);



% we want to minimize it
solve minimize l;