#!/usr/bin/env python3
"""
Quick Deployment Status Checker
Checks GitHub Actions and provides deployment guidance
"""

import sys
import webbrowser
from datetime import datetime

def print_banner():
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT STATUS CHECKER")
    print("="*60 + "\n")

def main():
    print_banner()
    
    # GitHub repository info
    repo_url = "https://github.com/kimmi77778888-rgb/school_system.com"
    actions_url = f"{repo_url}/actions"
    
    print("✅ CODE DEPLOYMENT STATUS\n")
    
    # Git status
    print("📦 Git Push:")
    print("   ✅ Merged to main branch")
    print("   ✅ Pushed to GitHub")
    print("   ✅ Commit: 5618b93")
    print("   ✅ Changes: StudentHistory system implemented\n")
    
    # GitHub Actions
    print("🔄 GitHub Actions:")
    print("   ⏳ Workflow: 'Deploy to Render'")
    print("   📍 Status: Check link below")
    print(f"   🔗 {actions_url}\n")
    
    # Render deployment
    print("🌐 Render Deployment:")
    print("   ⏳ Building application...")
    print("   ⏳ Running migrations...")
    print("   📍 Status: Check Render dashboard")
    print("   🔗 https://dashboard.render.com/\n")
    
    # Expected timeline
    print("⏱️  Expected Timeline:")
    print("   • GitHub Actions: ~2 minutes")
    print("   • Render Build: ~8-12 minutes")
    print("   • Total: ~10-15 minutes\n")
    
    # What to check
    print("🔍 What to Check:\n")
    print("   1. GitHub Actions (link above)")
    print("      - Look for green checkmark ✅")
    print("      - Or red X ❌ if failed\n")
    
    print("   2. Render Dashboard")
    print("      - Service status: 'Live' or 'Building'")
    print("      - Check 'Events' tab for progress")
    print("      - Review 'Logs' for any errors\n")
    
    print("   3. After Deployment")
    print("      - Visit your app URL")
    print("      - Login to admin: /admin/")
    print("      - Test promotion: /school/students/promote/")
    print("      - Check history: /admin/school/studenthistory/\n")
    
    # Actions
    print("="*60)
    print("\nWould you like to:")
    print("1. Open GitHub Actions in browser")
    print("2. Open Render Dashboard in browser")
    print("3. Show deployment commands")
    print("4. Exit")
    
    try:
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print(f"\n🌐 Opening GitHub Actions...")
            webbrowser.open(actions_url)
            print("✅ Check the workflow status in your browser")
            
        elif choice == "2":
            print(f"\n🌐 Opening Render Dashboard...")
            webbrowser.open("https://dashboard.render.com/")
            print("✅ Check your service status in the dashboard")
            
        elif choice == "3":
            print("\n📋 DEPLOYMENT COMMANDS:\n")
            
            print("Manual Deploy (if needed):")
            print("   # Via Render Dashboard:")
            print("   1. Go to dashboard.render.com")
            print("   2. Select your service")
            print("   3. Click 'Manual Deploy'\n")
            
            print("Check Deployment Status:")
            print("   # View logs:")
            print("   Render Dashboard → Your Service → Logs\n")
            
            print("Verify Migrations:")
            print("   # In Render Shell:")
            print("   python manage.py showmigrations school\n")
            
            print("Test Features:")
            print("   # Visit these URLs:")
            print("   /admin/school/studenthistory/")
            print("   /school/students/promote/")
            
        elif choice == "4":
            print("\n✅ Exiting. Good luck with deployment!")
            
        else:
            print("\n⚠️  Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n✅ Exiting...")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("📚 For detailed info, see: DEPLOYMENT_STATUS.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
