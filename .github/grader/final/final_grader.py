import os
import subprocess

import sys
import json
import traceback
import numpy as np
import pandas as pd

def main():
    print("--- Running Autograder for Final Exam ---")
    
    # Path setup: Grader is in .github/grader/final/final_grader.py
    # Repo root is 3 directories up
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    main_script_path = os.path.join(base_dir, 'assignments', 'final', 'code', 'main.py')
    expected_dir = os.path.dirname(__file__)
    
    # Change working directory so main.py runs properly (it reads data from '../data/wages.csv')
    os.chdir(os.path.dirname(main_script_path))
    
    # Execute student code
    student_globals = {}
    try:
        print("Executing student code...")
        with open(main_script_path, "r", encoding="utf-8") as f:
            student_code = f.read()
        exec(student_code, student_globals)
        print("Execution completed successfully.")
    except Exception as e:
        print(f"\nExecution encountered an error: {e}")
        traceback.print_exc(limit=2)
        print("\nContinuing grading with available variables...")

    total_score = 0
    max_score = 4
    
    # ---------------- Code Quality ----------------
    print("\n" + " Grading Code Quality ".center(80, "-"))
    try:
        result = subprocess.run(
            ['flake8', main_script_path, '--max-line-length=80'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Code Quality: CORRECT (+1 point)")
            total_score += 1
        else:
            print(f"Code Quality: FAILED. Linting errors found:\n{result.stdout}")
    except Exception as e:
        print(f"Code Quality: FAILED. Error running flake8: {e}")

    # ---------------- Question 1 ----------------
    print("\n" + " Grading Question 1 ".center(80, "-"))
    if 'q1_res' in student_globals:
        try:
            q1_expected_path = os.path.join(expected_dir, 'q1_exp.csv')
            q1_expected = pd.read_csv(q1_expected_path)
            
            q1_student = student_globals['q1_res']
            print("Student output (first 20 rows):")
            print(q1_student.head(20))
            pd.testing.assert_frame_equal(
                q1_student.reset_index(drop=True),
                q1_expected.reset_index(drop=True),
                check_dtype=False,
                atol=1e-3,
                rtol=1e-3
            )
            print("Question 1: CORRECT (+1 point)")
            total_score += 1
        except Exception as e:
            print(f"Question 1: FAILED. Output did not match expected or error during comparison: {e}")
    else:
        print("Question 1: FAILED. 'q1_res' was not found. The script might have crashed before defining it.")

    # ---------------- Question 2 ----------------
    print("\n" + " Grading Question 2 ".center(80, "-"))
    if 'q2_res' in student_globals:
        try:
            q2_expected_path = os.path.join(expected_dir, 'q2_exp.csv')
            q2_expected = pd.read_csv(q2_expected_path)
            q2_student = student_globals['q2_res']
            
            print("Student output (first 20 rows):")
            print(q2_student.head(20))
            
            # Allow some tolerance for floating point comparisons
            pd.testing.assert_frame_equal(
                q2_student.reset_index(drop=True),
                q2_expected.reset_index(drop=True),
                check_dtype=False,
                atol=1e-3,
                rtol=1e-3
            )
            print("Question 2: CORRECT (+1 point)")
            total_score += 1
        except Exception as e:
            print(f"Question 2: FAILED. Output did not match expected or error during comparison: {e}")
    else:
        print("Question 2: FAILED. 'q2_res' was not found. The script might have crashed before defining it.")

    # ---------------- Question 3 ----------------
    print("\n" + " Grading Question 3 ".center(80, "-"))
    if 'q3_res' in student_globals:
        try:
            q3_expected_path = os.path.join(expected_dir, 'q3_exp.csv')
            q3_expected = pd.read_csv(q3_expected_path)
            q3_student = student_globals['q3_res']
            
            print("Student output (first 20 rows):")
            print(q3_student.head(20))
            
            pd.testing.assert_frame_equal(
                q3_student.reset_index(drop=True),
                q3_expected.reset_index(drop=True),
                check_dtype=False,
                atol=1e-3,
                rtol=1e-3
            )
            print("Question 3: CORRECT (+1 point)")
            total_score += 1
        except Exception as e:
            print(f"Question 3: FAILED. Output did not match expected or error during comparison: {e}")
    else:
        print("Question 3: FAILED. 'q3_res' was not found. The script might have crashed before defining it.")

    # Final Score
    print("\n" + "=" * 80)
    print(f"FINAL SCORE: {total_score} / {max_score}".center(80, " "))
    print("=" * 80)

    if total_score < max_score:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
