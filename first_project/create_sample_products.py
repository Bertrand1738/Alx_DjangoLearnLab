#!/usr/bin/env python
"""
Create sample products for the book store
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

from book_store.models import Product

def create_sample_products():
    """Create a variety of sample products"""
    
    # Clear existing products
    Product.objects.all().delete()
    print("🗑️ Cleared existing products")
    
    # Sample products data
    products_data = [
        {
            'name': 'Python Crash Course',
            'description': 'A hands-on, project-based introduction to programming in Python. Perfect for beginners who want to learn Python quickly.',
            'price': 29.99,
            'category': 'Programming'
        },
        {
            'name': 'Django for Beginners',
            'description': 'Build websites with Python and Django. Learn the fundamentals of web development with this comprehensive guide.',
            'price': 39.99,
            'category': 'Web Development'
        },
        {
            'name': 'Clean Code',
            'description': 'A handbook of agile software craftsmanship. Learn how to write clean, maintainable code that stands the test of time.',
            'price': 45.99,
            'category': 'Programming'
        },
        {
            'name': 'Data Science Handbook',
            'description': 'Essential tools and techniques for working with data. Covers Python, pandas, matplotlib, and machine learning basics.',
            'price': 54.99,
            'category': 'Data Science'
        },
        {
            'name': 'Machine Learning Basics',
            'description': 'Introduction to machine learning concepts and algorithms. Includes practical examples and real-world applications.',
            'price': 49.99,
            'category': 'Machine Learning'
        },
        {
            'name': 'JavaScript: The Good Parts',
            'description': 'Discover the elegant, powerful, and sometimes surprising features of JavaScript. A must-read for web developers.',
            'price': 32.99,
            'category': 'Web Development'
        },
        {
            'name': 'Design Patterns',
            'description': 'Elements of reusable object-oriented software. Learn the classic design patterns that every programmer should know.',
            'price': 47.99,
            'category': 'Programming'
        },
        {
            'name': 'SQL in 10 Minutes',
            'description': 'Teach yourself SQL in 10 minutes a day. Quick and practical lessons for database beginners.',
            'price': 24.99,
            'category': 'Database'
        },
        {
            'name': 'React Native in Action',
            'description': 'Build mobile apps with React Native. Learn to create cross-platform applications for iOS and Android.',
            'price': 42.99,
            'category': 'Mobile Development'
        },
        {
            'name': 'Git Pocket Guide',
            'description': 'A working introduction to Git version control. Essential commands and workflows for developers.',
            'price': 19.99,
            'category': 'Development Tools'
        },
        {
            'name': 'The Art of Computer Programming',
            'description': 'Donald Knuth\'s legendary work on computer programming algorithms. Volume 1: Fundamental Algorithms.',
            'price': 89.99,
            'category': 'Computer Science'
        },
        {
            'name': 'Deep Learning with Python',
            'description': 'Practical deep learning for coders. Learn to build neural networks with Keras and TensorFlow.',
            'price': 59.99,
            'category': 'Machine Learning'
        }
    ]
    
    # Create products
    created_products = []
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        created_products.append(product)
        print(f"✅ Created: {product.name} - ${product.price}")
    
    print(f"\n🎉 Successfully created {len(created_products)} products!")
    
    # Show summary by category
    categories = Product.objects.values_list('category', flat=True).distinct()
    print(f"\n📊 Products by category:")
    for category in categories:
        count = Product.objects.filter(category=category).count()
        print(f"   {category}: {count} products")
    
    return created_products

if __name__ == "__main__":
    create_sample_products()
