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


%CONSTRAINTS
constraint cumulative([positions[i,2] | i in RETS], size2, size1, width) /\ forall(i in RETS)
 (positions[i,1]+sizes[i,1] <= width);

constraint cumulative([positions[i,1] | i in RETS], size1, size2, l) /\ forall(i in RETS)
 (positions[i,2]+sizes[i,2] <= l);

% two circuits can be:
%  not overlapped on any axis
%  overlapped on the x axis or the y axis
%  but not both axis
       
constraint diffn([positions[i,1] | i in RETS], [positions[i,2] | i in RETS],size1,size2);

% symmetry breaking

% two circuits forming a bigger rectangle in any of the dimensions can be switched

% does the rest of the solution make difference?
% add in lhs of implication [positions[k,1] | k in RETS where k != i /\ k != j] = [s[k,1] | k in RETS where k != i /\ k != j] /\ 
%/*
constraint forall(i,j in RETS where i<j)(
  if ((positions[j,1]+sizes[j,1] == positions[i,1]) /\ (sizes[j,2] == sizes[i,2])) then
    let {
          array[RETS,1..2] of var int: s=positions, constraint s[j,1] = positions[i,1] /\ s[i,1] = positions[j,1]
        } in(
              lex_lesseq(array1d(positions), array1d(s))
            )
  else 
       1>0
  endif
  );

constraint forall(i,j in RETS where i<j)(
  if ((positions[j,2]+sizes[j,2] == positions[i,2]) /\ (sizes[j,1] == sizes[i,1])) then
    let { 
          array[RETS,1..2] of var int: s = positions, constraint s[j,2] = positions[i,2] /\ s[i,2] = positions[j,2]
        } in(
              lex_lesseq(array1d(positions), array1d(s))
            )
  else 
       1>0
  endif
  );


% two circuits which are equal can be switched
constraint forall(i,j in RETS where i<j)(
  if (sizes[j,1] == sizes[i,1] /\ sizes[j,2] == sizes[i,2]) then
    let {
          array[RETS,1..2] of var int: s, constraint s[j,1] = positions[i,1] /\ s[i,1] = positions[j,1] /\
               s[j,2] = positions[i,2] /\ s[i,2] = positions[j,2]
        } in(
              lex_lesseq(array1d(positions), array1d(s))
            )
  else 
       1>0
  endif
  );

%*/

%OBJECTIVE

%search annotations

ann: search_split1 = int_search([positions[i,2] | i in RETS] ++ [positions[i,1] | i in RETS], dom_w_deg, indomain_min, complete);
ann: search_split2 = int_search([l], dom_w_deg, indomain_min, complete);

ann: search_ann_dwd = int_search([l] ++ [positions[i,2] | i in RETS] ++ [positions[i,1] | i in RETS], dom_w_deg, indomain_split, 
complete);

ann: search_ann_ff = int_search([l] ++ [positions[i,2] | i in RETS] ++ [positions[i,1] | i in RETS], first_fail, indomain_min, complete);

ann: search_ann_io = int_search([l] ++ [positions[i,2] | i in RETS] ++ [positions[i,1] | i in RETS], input_order, indomain_min, complete);


% we want to minimize l

%solve :: seq_search([search_split2, search_split1]) minimize l;
solve :: search_ann_io minimize l;
