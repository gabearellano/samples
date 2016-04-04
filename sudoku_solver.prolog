%% The following sudoku solver was written 
 % by Gabriel Arellano (garellano88@gmail.com)
 % To call the solver, load this file and use the following command: 
 %       sudoku(Board).   
 % The Board should be in the following format: an array of length 81
%% that has each row listed in order sequentially.

% needed for ins in check_domain.
:- use_module(library(clpfd)).

%% The divide_array predicate will convert an original array of nine
 % elements into three arrays of three elements each. This is helpful
%% for formatting an array for output when printing.
divide_array(OriginalArray, Array1, Array2, Array3) :-
	    % set up 3 arrays of length 3
	OriginalArray = [E1,E2,E3,E4,E5,E6,E7,E8,E9],
	Array1 = [E1,E2,E3],
	Array2 = [E4,E5,E6],
	Array3 = [E7,E8,E9].

%% The print_nine method will remove 9 elements from a list and print
 % them. In the first version, the corner case of printing the final
 % elements of a Sudoku board is covered; the latter version divides
 % the list into a head and tail - an impossibility with an empty list
 % (leads to a fail). In the second version, the termination case for
 % recursion (Count = 9) reverses the list, since appending elements
 % to a list's head creates a backwards list in the recursive case,
 % otherwise it adds the head of the list to the list to be printed
%% (Nine). Both methods also format the output for easier reading.
print_nine([],Nine,Count,OutRest) :-
	% if the count = 9 and the remaining list is empty
	    % then assign an empty array to the return param
	    % reverse the elements of the backwards list,
	    % format the list for printing,
	    % and print the correctly ordered list;
	Count = 9,
	OutRest = [],
	reverse(Nine,OutNine),

	    % divide array of 9 elements into 3 arrays of 3 el.
	divide_array(OutNine, Block1, Block2, Block3),
	    % print the blocks with spacing for formatting
	print(Block1), print(' '),
	print(Block2), print(' '),
	print(Block3), print(' '),
	print('\n'), !;

	% else an abnormal condition exists -> fail.
	!, fail.

print_nine([Head|Tail],Nine,Count,OutRest) :-
	% if the count is nine,
	    % then assign remaining array to OutRest,
	    % reverse the elements of the backwards list,
	    % and print the correctly ordered list;
	Count = 9,
	OutRest = [Head|Tail],
	reverse(Nine,OutNine),
	
	    % divide array of 9 elements into 3 arrays of 3 el.
	divide_array(OutNine, Block1, Block2, Block3),
	    % print the blocks with spacing for formatting
	print(Block1), print(' '),
	print(Block2), print(' '),
	print(Block3), print(' '),
	print('\n'), !;

	% else update the counter
	    % and append the head to the list to be printed (Nine).
	NewCount is Count+1,
	print_nine(Tail,[Head|Nine],NewCount,OutRest), !.

%% The print_me method recursively prints a sudoku board nine elements
%% at a time.
print_me([], _) :- !.
print_me(Board, Counter) :-
	print_nine(Board,[],0,RestOfBoard),
	% if counter = 3 or 6, print a line for formatting
	((Counter mod 3 =:= 0, Counter =\= 9) -> 
	  NewCount = Counter +1,
	  print('------------------------\n');
	  NewCount = Counter + 1),
	print_me(RestOfBoard, NewCount).


%% The print_board method prints the board with a frame.
print_board(Board) :-
	print('\n\n-------- Board ---------\n'),
	print_me(Board, 1),
	print('========================\n').


%% validate checks each row, column, and square for unique elements.
validate([]) :- !.		
validate([Head|Tail]) :-
	all_different(Head),
	validate(Tail).

%% check_domain checks that all of the elements of Values are contined
%% within the lower and upper bound provided as parameters.
check_domain(Values, LowerBound, UpperBound) :-
	Values ins LowerBound..UpperBound.

%% The evaluate method checks that everything about the provided
 % sudoku board is valid. It enforces the following constraints:
 % 1 - The input is an array of length 81
 % 2 - All elements in the solution are within 1..9
 % 3 - The board has 9 rows, columns, and square regions.
%% 4 - Each set of numbers in #3 has 9 unique elements.
evaluate(Board, Solution) :-
	Solution = Board,

	length(Board, 81),

	check_domain(Solution, 1, 9),

	Board = [A1, A2, A3, A4, A5, A6, A7, A8, A9,
	         B1, B2, B3, B4, B5, B6, B7, B8, B9,
	         C1, C2, C3, C4, C5, C6, C7, C8, C9,
	         D1, D2, D3, D4, D5, D6, D7, D8, D9,
	         E1, E2, E3, E4, E5, E6, E7, E8, E9,
	         F1, F2, F3, F4, F5, F6, F7, F8, F9,
	         G1, G2, G3, G4, G5, G6, G7, G8, G9,
	         H1, H2, H3, H4, H5, H6, H7, H8, H9,
	         I1, I2, I3, I4, I5, I6, I7, I8, I9],
	
	Row1 = [A1, A2, A3, A4, A5, A6, A7, A8, A9],
	Row2 = [B1, B2, B3, B4, B5, B6, B7, B8, B9],
	Row3 = [C1, C2, C3, C4, C5, C6, C7, C8, C9],
	Row4 = [D1, D2, D3, D4, D5, D6, D7, D8, D9],
	Row5 = [E1, E2, E3, E4, E5, E6, E7, E8, E9],
	Row6 = [F1, F2, F3, F4, F5, F6, F7, F8, F9],
	Row7 = [G1, G2, G3, G4, G5, G6, G7, G8, G9],
	Row8 = [H1, H2, H3, H4, H5, H6, H7, H8, H9],
	Row9 = [I1, I2, I3, I4, I5, I6, I7, I8, I9],
	
	Col1 = [A1, B1, C1, D1, E1, F1, G1, H1, I1],
	Col2 = [A2, B2, C2, D2, E2, F2, G2, H2, I2],
	Col3 = [A3, B3, C3, D3, E3, F3, G3, H3, I3],
	Col4 = [A4, B4, C4, D4, E4, F4, G4, H4, I4],
	Col5 = [A5, B5, C5, D5, E5, F5, G5, H5, I5],
	Col6 = [A6, B6, C6, D6, E6, F6, G6, H6, I6],
	Col7 = [A7, B7, C7, D7, E7, F7, G7, H7, I7],
	Col8 = [A8, B8, C8, D8, E8, F8, G8, H8, I8],
	Col9 = [A9, B9, C9, D9, E9, F9, G9, H9, I9],
	
	Cuadro1 = [A1, A2, A3, B1, B2, B3, C1, C2, C3],
	Cuadro2 = [A4, A5, A6, B4, B5, B6, C4, C5, C6],
	Cuadro3 = [A7, A8, A9, B7, B8, B9, C7, C8, C9],
	Cuadro4 = [D1, D2, D3, E1, E2, E3, F1, F2, F3],
	Cuadro5 = [D4, D5, D6, E4, E5, E6, F4, F5, F6],
	Cuadro6 = [D7, D8, D9, E7, E8, E9, F7, F8, F9],
	Cuadro7 = [G1, G2, G3, H1, H2, H3, I1, I2, I3],
	Cuadro8 = [G4, G5, G6, H4, H5, H6, I4, I5, I6],
	Cuadro9 = [G7, G8, G9, H7, H8, H9, I7, I8, I9],

	validate([Row1, Row2, Row3, Row4, Row5, Row6, Row7, Row8,
	Row9, Col1, Col2, Col3, Col4, Col5, Col6, Col7, Col8, Col9,
	Cuadro1, Cuadro2, Cuadro3, Cuadro4, Cuadro5, Cuadro6, Cuadro7,
	Cuadro8, Cuadro9]),
	    %without using label, the final output would show
	    %uninitialized variables where multiple solutions
	    %existed. Using label, these uninitialized variables
	    %became actual numbers.
	label(Solution).

%% The sudoku method is a wrapper for solving a sudoku board and
%% printing it out to the user.
sudoku(Board) :- 
	evaluate(Board,Output),
	print_board(Output), !.
