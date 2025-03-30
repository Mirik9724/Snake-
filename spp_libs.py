import subprocess
import sys

# Список библиотек для установки
required_packages = [
    "python-dotenv",
    "pygame"
]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def is_package_installed(package):
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", package])
        return True
    except subprocess.CalledProcessError:
        return False

def install_missing_packages(packages):
    for package in packages:
        if not is_package_installed(package):
            print(f"Устанавливается: {package}")
            install(package)
        else:
            print(f"{package} уже установлен.")

# Устанавливаем только неустановленные библиотеки
install_missing_packages(required_packages)