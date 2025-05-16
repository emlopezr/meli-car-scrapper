import subprocess
import sys

if len(sys.argv) != 4:
  print("Usage: py main.py list_cars.csv details.csv report.csv")
  sys.exit(1)

output1 = sys.argv[1]
output2 = sys.argv[2]
output3 = sys.argv[3]

print(f"\n=== Running list_cars.py, output: {output1} ===")
subprocess.run([sys.executable, "list_cars.py", output1], check=True)

print(f"\n=== Running details.py, input: {output1}, output: {output2} ===")
subprocess.run([sys.executable, "details.py", output1, output2], check=True)

print(f"\n=== Running report.py, input: {output2}, output: {output3} ===")
subprocess.run([sys.executable, "report.py", output2, output3], check=True)

print("\n✅ All scripts completed successfully.")