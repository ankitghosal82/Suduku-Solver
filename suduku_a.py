import streamlit as st
import pandas as pd

# Sudoku solver functions (your existing logic)
def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

# Streamlit UI
st.title("🧩 Interactive Sudoku Solver")

st.write("Enter your Sudoku puzzle using the inputs below (0 = empty cell).")

# Input grid: 9x9 number inputs
board = []
for i in range(9):
    cols = st.columns(9)
    row = []
    for j in range(9):
        val = cols[j].number_input("", min_value=0, max_value=9, value=0, key=f"{i}-{j}")
        row.append(val)
    board.append(row)

if st.button("Solve Sudoku"):
    original_board = [r[:] for r in board]  # Deep copy to remember original clues
    if solve_sudoku(board):
        st.success("Sudoku solved!")

        df = pd.DataFrame(board)

        # Styling function: highlight cells solved by the program (blue & bold)
        def highlight_cell(val, row, col):
            if original_board[row][col] == 0:
                return 'color: blue; font-weight: bold; font-size: 18px;'
            else:
                return 'color: black; font-weight: normal; font-size: 18px;'

        def highlight_df(row):
            return [highlight_cell(val, row.name, col) for col, val in enumerate(row)]

        styled_df = df.style.apply(highlight_df, axis=1)
        st.dataframe(styled_df, width=450, height=450)

    else:
        st.error("No solution exists for the given puzzle.")
