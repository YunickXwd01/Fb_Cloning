
import os
import sys
import platform
import subprocess

def git_pull():
    """Check for updates from git repository"""
    print("\033[1;36m[1/3] 🔄 Checking for updates...\033[0m")
    
    # Check if .git directory exists
    if not os.path.exists(".git"):
        print("\033[1;33m⚠ Not a git repository, skipping update check\033[0m")
        return True
    
    try:
        # Check if git is installed
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        
        # Fetch latest changes
        print("\033[1;37mFetching updates...\033[0m")
        fetch_result = subprocess.run(["git", "fetch"], 
                                    capture_output=True, 
                                    text=True)
        
        if fetch_result.returncode != 0:
            print("\033[1;33m⚠ Failed to fetch updates\033[0m")
            return True
        
        # Check if there are updates
        status_result = subprocess.run(["git", "status", "-uno"],
                                     capture_output=True,
                                     text=True)
        
        if "Your branch is behind" in status_result.stdout:
            print("\033[1;32m🔄 Updates available! Pulling latest changes...\033[0m")
            pull_result = subprocess.run(["git", "pull"],
                                       capture_output=True,
                                       text=True)
            if pull_result.returncode == 0:
                print("\033[1;32m✅ Successfully updated to latest version!\033[0m")
                return True
            else:
                print(f"\033[1;31m❌ Failed to update: {pull_result.stderr}\033[0m")
                return False
        else:
            print("\033[1;32m✅ Already up to date!\033[0m")
            return True
            
    except FileNotFoundError:
        print("\033[1;33m⚠ Git not installed, skipping update check\033[0m")
        return True
    except Exception as e:
        print(f"\033[1;31m❌ Error checking updates: {e}\033[0m")
        return True

def check_64bit():
    """Check if device is 64-bit"""
    print("\033[1;36m[2/3] 🔍 Checking device architecture...\033[0m")
    
    # Get architecture info
    arch = platform.machine().lower()
    print(f"\033[1;37mDevice architecture: {arch}\033[0m")
    
    # 64-bit architecture identifiers
    x64_archs = ['x86_64', 'amd64', 'x64', 'arm64', 'aarch64', 'armv8', 'arm64-v8a']
    
    # Check if architecture is 64-bit
    is_64bit = any(x64_arch in arch for x64_arch in x64_archs)
    
    # Additional checks
    if not is_64bit:
        # Check python build
        if hasattr(sys, 'maxsize'):
            is_64bit = sys.maxsize > 2**32
            print(f"\033[1;37mPython pointer size: {sys.maxsize}\033[0m")
    
    # Get more detailed info
    try:
        import struct
        pointer_size = struct.calcsize("P") * 8
        print(f"\033[1;37mPointer size: {pointer_size}-bit\033[0m")
        if pointer_size == 64:
            is_64bit = True
    except:
        pass
    
    return is_64bit

def check_requirements():
    """Check if required files exist"""
    print("\033[1;36m[3/3] 📁 Checking required files...\033[0m")
    
    required_files = ["main.cpython-312.so"]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"\033[1;32m✅ Found: {file}\033[0m")
        else:
            print(f"\033[1;31m❌ Missing: {file}\033[0m")
            all_exist = False
    
    # Check for checker.txt (will be created if missing)
    if not os.path.exists("checker.txt"):
        print("\033[1;33m⚠ checker.txt not found (will be created)\033[0m")
    
    return all_exist

def install_dependencies():
    """Install required Python packages"""
    print("\033[1;36m📦 Installing required packages...\033[0m")
    
    packages = [
        "yt-dlp",
        "requests",
        "colorama"
    ]
    
    for package in packages:
        try:
            # Try to import first
            if package == "yt-dlp":
                import_name = "yt_dlp"
            else:
                import_name = package
            
            __import__(import_name)
            print(f"\033[1;32m✅ {package} already installed\033[0m")
        except ImportError:
            # Install if not found
            print(f"\033[1;33mInstalling {package}...\033[0m")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package, "-q"], 
                             check=True, capture_output=True)
                print(f"\033[1;32m✅ {package} installed successfully\033[0m")
            except subprocess.CalledProcessError as e:
                print(f"\033[1;31m❌ Failed to install {package}\033[0m")
                return False
    
    return True

def run_main_module():
    """Run the main Cython module"""
    print("\033[1;36m🚀 Starting Facebook Tool...\033[0m")
    print("\033[1;36m════════════════════════════════════════════════\033[0m")
    
    try:
        # Import the compiled module
        import main
        
        # Check if main module has the required functions
        if hasattr(main, 'check_subscription'):
            # Run the tool
            main.main()
        else:
            print("\033[1;31m❌ Error: main module doesn't have required functions\033[0m")
            return False
            
    except ImportError as e:
        print(f"\033[1;31m❌ Error importing main module: {e}\033[0m")
        print("\033[1;33mMake sure 'main.cpython-312.so' exists in current directory\033[0m")
        return False
    except Exception as e:
        print(f"\033[1;31m❌ Error running main module: {e}\033[0m")
        return False
    
    return True

def main():
    """Main entry point"""
    try:
        # Step 1: Git pull for updates
        if not git_pull():
            print("\033[1;33m⚠ Continuing with current version...\033[0m")
        
        print()  # Blank line
        
        # Step 2: Check if device is 64-bit
        if not check_64bit():
            print()
            print("\033[1;31m════════════════════════════════════════════════\033[0m")
            print("\033[1;31m❌ UNSUPPORTED DEVICE\033[0m")
            print("\033[1;31m════════════════════════════════════════════════\033[0m")
            print("\033[1;31mThis tool requires a 64-bit Android device.\033[0m")
            print("\033[1;31mYour device appears to be 32-bit.\033[0m")
            print("\033[1;31mPlease use a 64-bit Android device.\033[0m")
            print("\033[1;31m════════════════════════════════════════════════\033[0m")
            input("\n\033[1;33mPress Enter to exit...\033[0m")
            return
        
        print("\033[1;32m✅ Device is 64-bit, continuing...\033[0m")
        print()  # Blank line
        
        # Step 3: Check required files
        if not check_requirements():
            print("\033[1;31m❌ Missing required files. Cannot continue.\033[0m")
            input("\n\033[1;33mPress Enter to exit...\033[0m")
            return
        
        # Step 4: Install dependencies
        if not install_dependencies():
            print("\033[1;33m⚠ Some packages failed to install, but we can try to continue...\033[0m")
        
        print()  # Blank line
        
        # Step 5: Run the main module
        success = run_main_module()
        
        if not success:
            print()
            print("\033[1;31m════════════════════════════════════════════════\033[0m")
            print("\033[1;31m❌ TOOL FAILED TO START\033[0m")
            print("\033[1;31m════════════════════════════════════════════════\033[0m")
            print("\033[1;33mTroubleshooting steps:\033[0m")
            print("\033[1;33m1. Make sure you have Python 3.12 installed\033[0m")
            print("\033[1;33m2. Check if 'main.cpython-312.so' exists\033[0m")
            print("\033[1;33m3. Run: pip install yt-dlp requests colorama\033[0m")
            print("\033[1;31m════════════════════════════════════════════════\033[0m")
        
        # Wait before exit
        input("\n\033[1;33mPress Enter to exit...\033[0m")
        
    except KeyboardInterrupt:
        print("\n\n\033[1;33m⚠ Tool interrupted by user\033[0m")
    except Exception as e:
        print(f"\n\033[1;31m❌ Unexpected error: {e}\033[0m")
        input("\n\033[1;33mPress Enter to exit...\033[0m")

if __name__ == "__main__":
    main()
