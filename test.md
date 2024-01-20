Report for even better solution: - Sudoku.hs:
  - Added a new function `solve3` which is similar to `solve2` but uses the `fix` function
  - Added a new function `fix` which takes a function and an argument and applies the function repeatedly until the result doesn't change
  - Added a new definition for `single` function which checks if a list has only one element
  - Added a new definition for `solve3` function which filters valid grids after collapsing and applying the `prune` function using `fix` function
  - Added a new definition for `fix` function which applies a function repeatedly until the result doesn't change
Report for Better solution: Changes in Sudoku.hs:
- Modified import statement to include `(\\)` function from `Data.List` module.
- Added `prune` function, which applies `pruneBy` function to matrix by calling it on `boxs`, `cols`, and `rows`.
- Added `reduce` function, which reduces choices in a row by removing singles.
- Added `minus` function, which subtracts one list of choices from another using `(\\)` function if first list is not a single choice.
- Added `single` function, which checks if a list contains only one element.
- Added `solve2` function, which filters valid grids after collapsing and pruning matrix.
- Removed `solve3` function.
Report for Simple: Changes in Sudoku.hs:
- Added a new type `Choices` which is a list of `Value`
- Added a `choices` function that converts a `Grid` into a `Matrix Choices`
- Added a `solve` function that filters valid grids from the result of collapsing the choices
- Added a `cp` function that generates all possible combinations of a list of lists
- Added a `collapse` function that generates all possible combinations of a matrix of lists

## Summary

- The "even better solution" pull request introduces a new function `solve3` which uses the `fix` function to solve the Sudoku puzzle. It also adds a new definition for the `single` function and a new definition for the `fix` function.
- The "better solution" pull request modifies the import statement, adds the `prune`, `reduce`, `minus`, `single`, and `solve2` functions, and removes the `solve3` function.
- The "simple" pull request adds the `Choices` type, the `choices`, `solve`, `cp`, and `collapse` functions.

## Key Points

- The "even better solution" pull request introduces a more efficient way to solve the Sudoku puzzle using the `fix` function.
- The "better solution" pull request improves the code by adding functions for pruning and reducing choices, as well as filtering valid grids.
- The "simple" pull request simplifies the code by introducing a new type and functions for generating combinations and solving the puzzle.

## Impact

- The "even better solution" pull request improves the efficiency of solving the Sudoku puzzle.
- The "better solution" pull request improves the code by adding more functionality and making it more readable.
- The "simple" pull request simplifies the code and makes it easier to understand and maintain.
