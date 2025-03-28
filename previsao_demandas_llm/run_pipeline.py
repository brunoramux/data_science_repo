import subprocess

def run_pipeline(script_name):
  try:
    # Run the pipeline script
    result = subprocess.run(["python", script_name], check=True, capture_output=True, text=True)
    print(f"Output of {script_name}:\n{result.stdout}")
  except subprocess.CalledProcessError as e:
    print(f"Error occurred while running {script_name}: {e.stderr}")
    
scripts = [
  'carrega_dados.py',
  'conexao_postgres.py',
  'llm.py'
]

for script in scripts:
  run_pipeline(script)
  
print("Pipeline executada com sucesso!")

# This script runs the pipeline by executing each script in the specified order.