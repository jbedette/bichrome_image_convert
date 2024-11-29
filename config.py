import subprocess
import sys
import platform


def install_package(package):
    """
    Install a Python package using pip.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"'{package}' installed successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to install '{package}'. Please install it manually.")


def check_and_install_tkinter():
    """
    Check and install tkinter if necessary (Linux only).
    """
    system = platform.system()
    if system == "Linux":
        try:
            import tkinter
            print("tkinter is already installed.")
        except ImportError:
            print("tkinter is not installed. Attempting to install it...")
            # Check the Linux distribution and install tkinter using the appropriate package manager
            distro = platform.linux_distribution()[0].lower()
            if "ubuntu" in distro or "debian" in distro:
                subprocess.run(["sudo", "apt", "install", "-y", "python3-tk"], check=True)
            elif "fedora" in distro or "redhat" in distro:
                subprocess.run(["sudo", "dnf", "install", "-y", "python3-tkinter"], check=True)
            elif "arch" in distro:
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "tk"], check=True)
            else:
                print("Please install 'tkinter' manually for your Linux distribution.")
    else:
        print("tkinter is included by default on non-Linux systems.")


def main():
    # Ensure pip is up-to-date
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip updated successfully.")
    except subprocess.CalledProcessError:
        print("Failed to update pip. Please update it manually.")

    # Install required Python packages
    required_packages = ["pillow"]
    for package in required_packages:
        install_package(package)

    # Check for tkinter on Linux systems
    check_and_install_tkinter()

    print("\nSetup completed successfully!")


if __name__ == "__main__":
    main()
