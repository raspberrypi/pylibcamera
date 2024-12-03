import subprocess


# Run build - expected to fail due to different versions
ret = subprocess.run(("python", "-m", "build"))
if ret.returncode == 0:
    print("Build did not fail, so must be same version - exit script!!!")

lines = []
pyversion_line = None
version_line = None
revision_line = None
with open("pyproject.toml") as f:
    for i, line in enumerate(f.readlines()):
        if "version = " in line:
            pyversion_line = i
        elif "-Drevision" in line:
            revision_line = i
        elif "-Dversion" in line:
            version_line = i
        lines.append(line)
pyproject_orig = lines.copy()

new_version = subprocess.check_output("./check-version.sh", text=True).strip()
old_version = lines[version_line][len("    '-Dversion="):-len("'\n")]
print(f"New version is {new_version}, old version was {old_version}")
if old_version == new_version:
    print("No change - exit script!!!")
lines[version_line] = f"    '-Dversion={new_version}'\n"

new_revision = subprocess.check_output(["git", "-C", "libcamera", "describe", "--tags", "origin/main"], text=True).strip()
old_revision = lines[revision_line][len("    '-Drevision="):-len("',\n")]
print(f"New revision is {new_revision}, old version was {old_revision}")
if old_revision == new_revision:
    print("No change - exit script!!!")
lines[revision_line] = f"    '-Drevision={new_revision}',\n"

old_pyversion = lines[pyversion_line][len("version = '"):-len("'\n")]
new_pyversion = input(f"New pyversion - currently {old_pyversion}: ")
lines[pyversion_line] = f"version = '{new_pyversion}'\n"

with open("pyproject.toml", "w") as f:
    f.writelines(lines)

lines = []
table_end_line = None
with open("README.md") as f:
    for i, line in enumerate(f.readlines()):
        if "| --------------- | -------------------------- | ------------------- |" in line:
            table_end_line = i+1
        lines.append(line)
readme_orig = lines.copy()

new_table_line = f"| {input('System and Date (eg Raspberry Pi Bookworm 22/11/2023): ')} | {new_version} | {new_pyversion} |\n"
lines.insert(table_end_line, new_table_line)

with open("README.md", "w") as f:
    f.writelines(lines)

# Commit changes for build
ret = subprocess.run(("git", "add", "."))
ret = subprocess.run(("git", "commit", "-m", f"Update for libcamera {new_revision}"))

# Run build - should now succeed
ret = subprocess.run(("python", "-m", "build"))

print(f"Finished with ret {ret.returncode}")
if ret.returncode:
    print("Failed - reverting changes")

    with open("pyproject.toml", "w") as f:
        f.writelines(pyproject_orig)

    with open("README.md", "w") as f:
        f.writelines(readme_orig)

    ret = subprocess.run(("git", "reset", "HEAD~1"))
