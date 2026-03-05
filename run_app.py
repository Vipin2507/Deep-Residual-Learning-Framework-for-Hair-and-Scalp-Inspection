"""
Hair & Scalp Disease Prediction Application Launcher
This script launches the Django application automatically
"""
import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    print("=" * 60)
    print("  HAIR & SCALP DISEASE PREDICTION SYSTEM")
    print("=" * 60)
    print()
    
    # Get the directory where this script is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = Path(sys._MEIPASS)
    else:
        # Running as script
        base_dir = Path(__file__).parent.resolve()
    
    django_dir = base_dir / "minor"
    manage_py = django_dir / "manage.py"
    
    # Check if manage.py exists
    if not manage_py.exists():
        print("❌ Error: Django project not found!")
        print(f"   Looking for: {manage_py}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("✅ Django project found")
    print(f"📂 Project directory: {django_dir}")
    print()
    
    # Change to Django directory
    os.chdir(django_dir)
    
    # Run migrations
    print("🔄 Setting up database...")
    try:
        subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], 
                      check=True, capture_output=True)
        print("✅ Database ready")
    except subprocess.CalledProcessError as e:
        print("⚠️  Database setup warning (continuing anyway)")
    
    print()
    print("🚀 Starting Django server...")
    print("📍 Server will run at: http://127.0.0.1:8000")
    print()
    print("=" * 60)
    print("  APPLICATION IS STARTING...")
    print("  Your browser will open automatically in 3 seconds")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANT: Keep this window open while using the app!")
    print("   To stop the server, press Ctrl+C")
    print()
    
    # Start Django server in a subprocess
    try:
        # Wait a moment before opening browser
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://127.0.0.1:8000")
        
        # Start Django server (this will block)
        subprocess.run([sys.executable, "manage.py", "runserver", "127.0.0.1:8000"])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("✅ Application closed successfully")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
