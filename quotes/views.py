from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse

# quotes/views.py
from django.shortcuts import render
from django.http import HttpResponse
import random

# Sample data for quotes and images
quotes = [
    "A person's a person, no matter how small.",
    "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. You're on your own. And you know what you know. And YOU are the one who'll decide where to go...",
    "Be who you are and say what you feel, because those who mind don't matter and those who matter don't mind.",
    "Unless someone like you cares a whole awful lot, nothing is going to get better. It's not.",
    "You'll miss the best things if you keep your eyes shut.",
    "To the world you may be one person; but to one person you may be the world.",
]

images = [
    "data:image/jpeg;base64,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",
    "https://www.yourkidtastic.com/wp-content/uploads/2024/03/Happy-Birthday-Dr.-Seuss.jpg",
    "https://cdn.britannica.com/31/249631-050-B41F5793/American-author-and-illustrator-Dr-Seuss-Theodor-Seuss-Geisel-1957.jpg"
]

def index(request):
    # Select a random quote and image
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    
    # Context for the template
    context = {
        'quote': selected_quote,
        'image_url': selected_image
    }
    
    # Render the quote.html template with context
    return render(request, 'quotes/quote.html', context)

def quote(request):
    return index(request)  # Reuse the index view for the random quote

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    context = {
        'bio': "This web application displays quotes from notable individuals.",
        'creator': "Created by [Your Name]",
    }
    return render(request, 'quotes/about.html', context)
