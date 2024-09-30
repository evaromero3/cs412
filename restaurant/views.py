from django.shortcuts import render
import random
import time

# Create your views here.
def main(request):
    # Render the main.html template
    return render(request, 'restaurant/main.html')

def order(request):
    '''Show the web page with the form.'''

    # Generate a daily special
    daily_specials = {
        'Pollo Sudado': 14.00,
        'Carne Asada': 16.00,
        'Arepa Con Huevo': 11.00,
    }

    # Pick a random daily special
    daily_special, special_price = random.choice(list(daily_specials.items()))

    # Pass the daily special to the template
    context = {
        'daily_special': daily_special,
        'special_price': special_price
    }

    template_name = "restaurant/order.html"
    return render(request, template_name, context)

def confirmation(request):
    '''Process the form submission and generate a result.'''
    template_name = "restaurant/confirmation.html"
    
    if request.POST:
        # Read form data into Python variables:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        instructions = request.POST['instructions']
        food = request.POST.getlist('food')
        extras = request.POST.getlist('extras')

        # Daily special information:
        daily_special = request.POST.get('daily_special')
        special_price = float(request.POST.get('special_price', 0))

        # Fixed food prices:
        food_prices = {
            'Beef Empanada': 9.00,
            'Chicken Empanada': 9.00,
            'Sancocho': 12.00,
            'Bandeja Paisa': 18.00,
            'Pollo Sudado': 14.00,
            'Carne Asada': 16.00,
            'Arepa Con Huevo': 11.00,
    }
    # Extras prices:
        extras_prices = {
            'Fried Egg': 1.50,
            'Chorizo': 2.00,
            'Arepa': 1.75
        }

        # If the daily special is selected, add its price:
        if daily_special and daily_special in food:
            food_prices[daily_special] = special_price

        # Calculate total based on selected items:
        total = 0.0
        for item in food:
            if item == daily_special:
                total += special_price
            else:
                total += food_prices.get(item, 0)

        # Add extras to the total:
        for extra in extras:
            total += extras_prices.get(extra, 0)

        # Format the total cost:
        total_cost_formatted = f"{total:.2f}"

        # Calculate ready time:
        current_time = time.time()
        ready_time_minutes = random.randint(30, 60)
        ready_time_seconds = 60 * ready_time_minutes
        ready_time = time.ctime(current_time + ready_time_seconds)

        # Package up data for the response:
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'instructions': instructions,
            'food': food,
            'ready_time': ready_time,
            'total': total_cost_formatted,
            'daily_special': daily_special,  # Include daily special in the confirmation
            'special_price': special_price
        }

    return render(request, template_name, context=context)