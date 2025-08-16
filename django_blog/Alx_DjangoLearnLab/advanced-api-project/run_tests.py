"""
Test Runner Script for Django REST Framework API

This script provides easy commands to run different types of tests
and generate reports about test coverage and results.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and print the results."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Running: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def run_all_tests():
    """Run all API tests with detailed output."""
    return run_command(
        "python manage.py test api --verbosity=2",
        "Running All API Tests"
    )

def run_specific_test_class():
    """Run a specific test class."""
    test_classes = [
        "api.test_views.BookAPITestCase",
        "api.test_views.BookAPIEdgeCasesTest", 
        "api.test_views.AuthorModelTest",
        "api.test_views.BookModelTest"
    ]
    
    print(f"\n📋 Available Test Classes:")
    for i, test_class in enumerate(test_classes, 1):
        print(f"   {i}. {test_class.split('.')[-1]}")
    
    try:
        choice = int(input("\nEnter test class number (1-4): "))
        if 1 <= choice <= len(test_classes):
            selected_class = test_classes[choice - 1]
            return run_command(
                f"python manage.py test {selected_class} --verbosity=2",
                f"Running {selected_class.split('.')[-1]} Tests"
            )
        else:
            print("❌ Invalid choice")
            return False
    except ValueError:
        print("❌ Please enter a valid number")
        return False

def run_quick_test():
    """Run a quick smoke test to verify basic functionality."""
    return run_command(
        "python manage.py test api.test_views.BookAPITestCase.test_book_list_view --verbosity=2",
        "Quick Smoke Test - Book List View"
    )

def run_permission_tests():
    """Run only permission-related tests."""
    permission_tests = [
        "api.test_views.BookAPITestCase.test_book_create_view_authenticated",
        "api.test_views.BookAPITestCase.test_book_create_view_unauthenticated", 
        "api.test_views.BookAPITestCase.test_book_delete_view_staff_user",
        "api.test_views.BookAPITestCase.test_book_delete_view_regular_user",
        "api.test_views.BookAPITestCase.test_book_list_create_view_permissions"
    ]
    
    success = True
    for test in permission_tests:
        result = run_command(
            f"python manage.py test {test}",
            f"Permission Test: {test.split('.')[-1]}"
        )
        if not result:
            success = False
    
    return success

def run_filtering_tests():
    """Run only filtering, searching, and ordering tests."""
    filtering_tests = [
        "api.test_views.BookAPITestCase.test_book_filtering_by_title",
        "api.test_views.BookAPITestCase.test_book_filtering_by_author",
        "api.test_views.BookAPITestCase.test_book_filtering_by_publication_year",
        "api.test_views.BookAPITestCase.test_book_searching",
        "api.test_views.BookAPITestCase.test_book_ordering",
        "api.test_views.BookAPITestCase.test_combined_filtering_searching_ordering"
    ]
    
    success = True
    for test in filtering_tests:
        result = run_command(
            f"python manage.py test {test}",
            f"Filtering Test: {test.split('.')[-1]}"
        )
        if not result:
            success = False
    
    return success

def generate_test_report():
    """Generate a comprehensive test report."""
    print(f"\n{'='*60}")
    print("📊 GENERATING COMPREHENSIVE TEST REPORT")
    print(f"{'='*60}")
    
    # Count total tests
    result = subprocess.run(
        "python manage.py test api --dry-run", 
        shell=True, capture_output=True, text=True
    )
    
    if "Ran" in result.stderr:
        # Extract test count from dry run output
        lines = result.stderr.strip().split('\n')
        for line in lines:
            if "Ran" in line:
                test_count = line.split()[1]
                print(f"📈 Total Tests: {test_count}")
                break
    
    # Run all tests and capture results
    print(f"\n🧪 Running full test suite...")
    success = run_all_tests()
    
    if success:
        print(f"\n✅ ALL TESTS PASSED!")
        print(f"🎉 Your API is working correctly!")
    else:
        print(f"\n❌ SOME TESTS FAILED!")
        print(f"🔍 Check the output above for details.")
    
    return success

def show_test_examples():
    """Show examples of how to run specific tests manually."""
    print(f"\n{'='*60}")
    print("📚 MANUAL TEST COMMAND EXAMPLES")
    print(f"{'='*60}")
    
    examples = [
        ("Run all API tests", "python manage.py test api"),
        ("Run with verbose output", "python manage.py test api --verbosity=2"),
        ("Run specific test class", "python manage.py test api.test_views.BookAPITestCase"),
        ("Run specific test method", "python manage.py test api.test_views.BookAPITestCase.test_book_list_view"),
        ("Run tests matching pattern", "python manage.py test api.test_views -k filtering"),
        ("Run with debug info", "python manage.py test api --debug-mode"),
        ("Keep test database", "python manage.py test api --keepdb")
    ]
    
    for description, command in examples:
        print(f"\n🔧 {description}:")
        print(f"   {command}")

def main():
    """Main test runner interface."""
    print("🚀 Django REST Framework API Test Runner")
    print("=" * 60)
    
    options = [
        ("1", "Run All Tests", run_all_tests),
        ("2", "Run Specific Test Class", run_specific_test_class),
        ("3", "Quick Smoke Test", run_quick_test),
        ("4", "Run Permission Tests Only", run_permission_tests),
        ("5", "Run Filtering Tests Only", run_filtering_tests),
        ("6", "Generate Test Report", generate_test_report),
        ("7", "Show Manual Test Examples", show_test_examples),
        ("q", "Quit", lambda: sys.exit(0))
    ]
    
    while True:
        print(f"\n📋 Select an option:")
        for option, description, _ in options:
            print(f"   {option}. {description}")
        
        choice = input(f"\nEnter your choice (1-7, q): ").strip().lower()
        
        for option, description, func in options:
            if choice == option:
                print(f"\n▶️  {description}")
                
                if func():
                    print(f"\n✅ {description} completed successfully!")
                else:
                    print(f"\n❌ {description} encountered issues.")
                
                break
        else:
            if choice:
                print(f"❌ Invalid choice: {choice}")

if __name__ == "__main__":
    # Ensure we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found!")
        print("Please run this script from your Django project directory.")
        sys.exit(1)
    
    main()
