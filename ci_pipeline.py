import subprocess
import sys

# 1. Basic command execution
def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            check=True  # Raise exception on non-zero exit code
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None

# Example: Check disk space
repo = input("enter repo link : ")
git_clone = run_command( f"git clone  {repo}")
