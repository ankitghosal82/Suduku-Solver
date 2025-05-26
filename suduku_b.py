import streamlit as st
import time
from suduku import SudokuSolver, generate_full_board, remove_cells, estimate_difficulty

st.set_page_config(page_title="Suduku Solver", layout="centered")

st.title("🧠 Suduku Solver & Generator")
st.markdown("Enter values or generate a puzzle, then click Solve to see step-by-step solving.")

# Session state initialization
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(9)] for _ in range(9)]
if 'solved' not in st.session_state:
    st.session_state.solved = False
if 'steps' not in st.session_state:
    st.session_state.steps = []
if 'step_index' not in st.session_state:
    st.session_state.step_index = 0

# Input Grid
def draw_grid():
    grid = []
    for i in range(9):
        cols = st.columns(9)
        row = []
        for j in range(9):
            with cols[j]:
                cell_value = st.number_input(f"{i},{j}", min_value=0, max_value=9,
                                             value=st.session_state.board[i][j],
                                             key=f"{i}-{j}")
                row.append(cell_value)
        grid.append(row)
    return grid

# Action buttons
col1, col2, col3, col4 = st.columns([1,1,1,2])
with col1:
    if st.button("Solve"):
        st.session_state.board = draw_grid()
        solver = SudokuSolver([row[:] for row in st.session_state.board])
        start = time.time()
        solved = solver.solve()
        end = time.time()
        if solved:
            st.session_state.steps = solver.steps
            st.session_state.solved = True
            st.session_state.solve_time = round(end - start, 4)
            st.session_state.recursive_calls = solver.recursive_calls
            st.session_state.backtracks = solver.backtracks
            st.session_state.difficulty = estimate_difficulty(len(solver.steps))
            st.session_state.step_index = 0
        else:
            st.error("❌ No solution found!")

with col2:
    if st.button("Next Step"):
        if st.session_state.solved and st.session_state.step_index < len(st.session_state.steps) - 1:
            st.session_state.step_index += 1

with col3:
    if st.button("Reset"):
        st.session_state.board = [[0 for _ in range(9)] for _ in range(9)]
        st.session_state.solved = False
        st.session_state.steps = []
        st.session_state.step_index = 0

with col4:
    difficulty = st.selectbox("Generate Puzzle", ["Easy", "Medium", "Hard"])
    if st.button("Generate"):
        full = generate_full_board()
        st.session_state.board = remove_cells(full, difficulty.lower())
        st.session_state.solved = False
        st.session_state.steps = []
        st.session_state.step_index = 0

# Display board
st.write("### Sudoku Board")
grid = draw_grid()

# Show step-by-step solution
if st.session_state.solved:
    st.write(f"### Step {st.session_state.step_index + 1} / {len(st.session_state.steps)}")
    step_board = st.session_state.steps[st.session_state.step_index]
    for row in step_board:
        st.write(" ".join(str(n) if n != 0 else "." for n in row))

    st.success(f"✅ Solved in {st.session_state.solve_time} seconds")
    st.info(f"📊 Recursive Calls: {st.session_state.recursive_calls}, Backtracks: {st.session_state.backtracks}")
    st.warning(f"🧩 Estimated Difficulty: {st.session_state.difficulty}")

