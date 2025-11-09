
import subprocess
import zipfile
import shutil
import os
import datetime

# ------------------------
# Helper: timestamped logs
# ------------------------
def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

# ------------------------
# 1. Pull latest code
# ------------------------
def pull_code(repo_path="."):
    log("Pulling latest code from Git...")
    try:
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        log("✅ Git pull successful.")
        return True
    except subprocess.CalledProcessError:
        log("❌ Git pull failed.")
        return False

# ------------------------
# 2. Run unit tests
# ------------------------
def run_tests():
    log("Running unit tests...")
    try:
        result = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests"], check=True)
        log("✅ All tests passed.")
        return True
    except subprocess.CalledProcessError:
        log("❌ Tests failed.")
        return False

# ------------------------
# 3. Package code as ZIP
# ------------------------
def package_code(output_zip="build.zip"):
    log("Packaging code...")
    with zipfile.ZipFile(output_zip, "w") as zipf:
        for root, dirs, files in os.walk("app"):
            for file in files:
                filepath = os.path.join(root, file)
                zipf.write(filepath)
    log(f"✅ Code packaged into {output_zip}")
    return output_zip

# ------------------------
# 4. Deploy to folder
# ------------------------
def deploy(package, deploy_path="deploy"):
    log("Deploying package...")
    os.makedirs(deploy_path, exist_ok=True)

    dest = os.path.join(deploy_path, os.path.basename(package))
    shutil.copy(package, dest)

    log(f"✅ Deployed to {deploy_path}")
    return dest



# ------------------------
# Main Pipeline
# ------------------------
def pipeline():
    log("🚀 Starting CI/CD Pipeline...")

    if not pull_code():
        return log("Pipeline stopped.")

    if not run_tests():
        return log("Pipeline stopped.")

    package = package_code()
    deployed_file = deploy(package)


    log("🎉 CI/CD Pipeline completed successfully!")


if __name__ == "__main__":
    pipeline()