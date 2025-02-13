import csv
import random
from datetime import datetime, timedelta
import json

# Define clothing items by category and climate
clothing_items = {
    'hot_weather': [
        'bikini', 'swimming trunks', 'sunscreen', 'sun hat', 'sunglasses',
        'sandals', 'flip flops', 'tank top', 'short sleeve shirt',
        'shorts', 'summer dress', 'light jacket', 'beach towel',
        'light scarf', 'light cardigan', 'swimming suit'
    ],
    'cold_weather': [
        'winter coat', 'sweater', 'thermal underwear', 'winter boots',
        'gloves', 'wool scarf', 'beanie', 'thick socks', 'long sleeve shirt',
        'jeans', 'winter hat', 'fleece jacket', 'wool socks', 'ear muffs',
        'thermal leggings', 'snow boots', 'hand warmers'
    ],
    'temperate': [
        'light jacket', 'jeans', 'sneakers', 't-shirt', 'dress shirt',
        'pants', 'socks', 'light sweater', 'rain jacket', 'umbrella',
        'cardigan', 'blazer', 'ankle boots', 'closed-toe shoes',
        'light scarf', 'casual dress'
    ],
    'business': [
        'business suit', 'dress shoes', 'tie', 'dress shirt',
        'blazer', 'dress pants', 'dress', 'formal shoes',
        'professional bag', 'belt'
    ],
    'essentials': [
        'toothbrush', 'toothpaste', 'deodorant', 'phone charger',
        'wallet', 'passport', 'underwear', 'socks', 'medications',
        'power adapter', 'toiletry bag', 'face wash', 'shampoo',
        'conditioner', 'brush/comb', 'face moisturizer'
    ]
}

def load_destinations(filename='destinations.json'):
    """Load destination data from JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['cities']

def get_monthly_temp_range(city_data, month):
    """Get the temperature range for a specific city and month."""
    return city_data['temps'][str(month)]

def generate_dates():
    """Generate random trip dates within the next year."""
    start_date = datetime.now() + timedelta(days=random.randint(1, 365))
    duration = random.randint(3, 14)  # Trips between 3 and 14 days
    end_date = start_date + timedelta(days=duration)
    return start_date, end_date

def calculate_clothing_quantities(duration_days, is_business=False):
    """Calculate required quantities of clothing based on trip duration."""
    # Base calculations assuming laundry every 7 days
    weeks = (duration_days + 6) // 7  # Round up to nearest week
    
    # Basic daily items
    quantities = {
        'underwear': duration_days + 1,  # One extra
        'socks': duration_days + 1,
        't-shirt': min(duration_days, 7) if not is_business else min(duration_days // 2, 4),
        'pants': min(duration_days // 2 + 1, 4),
        'shorts': min(duration_days // 2 + 1, 4),
    }
    
    # Business attire
    if is_business:
        quantities.update({
            'dress shirt': min(duration_days - 1, 6),  # One per business day minus travel days
            'dress pants': min(3, duration_days // 2),  # Can rewear
            'dress': min(4, duration_days // 2) if duration_days > 3 else 2,
            'blazer': 1 if duration_days <= 3 else 2,
            'tie': min(duration_days - 1, 5),
            'belt': 1,
            'dress shoes': 1 if duration_days <= 3 else 2
        })
    
    return quantities

def generate_packing_list(gender, age, destination_data, temp, duration_days, luggage_type, is_business=False):
    """Generate a realistic packing list based on travel parameters."""
    items = []
    climate = destination_data['climate']
    
    # Get base quantities
    quantities = calculate_clothing_quantities(duration_days, is_business)
    
    # Add essentials (always packed)
    essential_items = {
        'toothbrush': 1, 'toothpaste': 1, 'deodorant': 1, 'phone charger': 1,
        'wallet': 1, 'passport': 1, 'medications': 1, 'power adapter': 1
    }
    for item, quantity in essential_items.items():
        items.extend([item] * quantity)
    
    # Add toiletries based on duration
    if duration_days > 3 or luggage_type == 'checked':
        toiletries = {
            'shampoo': 1, 'conditioner': 1, 'face wash': 1,
            'face moisturizer': 1, 'brush/comb': 1
        }
        for item, quantity in toiletries.items():
            items.extend([item] * quantity)
    
    # Determine climate-appropriate clothing
    if temp > 25:  # Hot weather
        if gender == 'f':
            items.extend(['bikini'] * min(3, duration_days // 2) if temp > 28 else ['bikini'])
            items.extend(['summer dress'] * min(4, duration_days // 2))
            items.extend(['shorts'] * quantities['shorts'])
            items.extend(['tank top'] * quantities['t-shirt'])
        elif gender == 'm':
            items.extend(['swimming trunks'] * min(2, duration_days // 3))
            items.extend(['shorts'] * quantities['shorts'])
            items.extend(['tank top'] * quantities['t-shirt'])
        else:  # non-binary
            items.extend(['swimming suit'] * min(2, duration_days // 3))
            items.extend(['shorts'] * quantities['shorts'])
            items.extend(['tank top'] * quantities['t-shirt'])
            
    elif temp < 10:  # Cold weather
        winter_items = {
            'sweater': min(4, duration_days // 2),
            'thermal underwear': 2 if duration_days > 3 else 1,
            'winter coat': 1,
            'gloves': 1,
            'wool scarf': 1,
            'beanie': 1,
            'wool socks': min(4, duration_days // 2)
        }
        for item, quantity in winter_items.items():
            items.extend([item] * quantity)
            
    else:  # Temperate weather
        temperate_items = {
            't-shirt': quantities['t-shirt'],
            'jeans': quantities['pants'],
            'light jacket': 1,
            'sneakers': 1
        }
        for item, quantity in temperate_items.items():
            items.extend([item] * quantity)
    
    # Add climate-specific items
    if climate == 'tropical':
        items.extend(['sunscreen'] * (1 + duration_days // 7))
        items.extend(['insect repellent'] * (1 + duration_days // 7))
    elif climate == 'desert':
        items.extend(['sunscreen'] * (2 + duration_days // 5))
        items.extend(['head covering'] * 1)
    
    # Add business attire if it's a business trip
    if is_business:
        business_quantities = {
            'dress shirt': min(duration_days - 1, 6),
            'dress pants': min(3, duration_days // 2),
            'blazer': 1 if duration_days <= 3 else 2,
            'tie': min(duration_days - 1, 5) if gender == 'm' else 0,
            'dress shoes': 1 if duration_days <= 3 else 2,
            'belt': 1
        }
        if gender == 'f':
            business_quantities['dress'] = min(4, duration_days // 2)
        
        for item, quantity in business_quantities.items():
            if quantity > 0:  # Only add items with quantity > 0
                items.extend([item] * quantity)

    # Adjust quantities based on luggage type constraints
    max_items = {
        'hand': 15,
        'carry_on': 25,
        'checked': 40
    }
    
    # Convert to item counts early
    item_counts = {}
    for item in items:
        item_counts[item] = item_counts.get(item, 0) + 1
    
    total_items = sum(item_counts.values())
    
    if total_items > max_items[luggage_type]:
        essential_categories = ['underwear', 'socks', 'medications', 'passport', 'charger']
        
        # Sort items by priority (essential first)
        items_by_priority = {
            'essential': {},
            'non_essential': {}
        }
        
        for item, count in item_counts.items():
            if any(ess in item.lower() for ess in essential_categories):
                items_by_priority['essential'][item] = count
            else:
                items_by_priority['non_essential'][item] = count
        
        # Reduce non-essential items first
        while total_items > max_items[luggage_type]:
            reducible_items = list(items_by_priority['non_essential'].keys())
            if reducible_items:
                item_to_reduce = random.choice(reducible_items)
                if items_by_priority['non_essential'][item_to_reduce] > 1:
                    items_by_priority['non_essential'][item_to_reduce] -= 1
                else:
                    del items_by_priority['non_essential'][item_to_reduce]
                total_items -= 1
            else:
                # If we must reduce essentials
                reducible_essentials = list(items_by_priority['essential'].keys())
                if reducible_essentials:
                    item_to_reduce = random.choice(reducible_essentials)
                    if items_by_priority['essential'][item_to_reduce] > 1:
                        items_by_priority['essential'][item_to_reduce] -= 1
                    total_items -= 1
                else:
                    break
        
        # Combine counts back
        item_counts = {**items_by_priority['essential'], **items_by_priority['non_essential']}
    
    # Format the final packing list
    formatted_items = [f"{count} {item}" for item, count in item_counts.items() if count > 0]
    return ", ".join(formatted_items)

def generate_dataset(num_records, destinations_file='destinations.json'):
    """Generate the specified number of travel packing records."""
    destinations = load_destinations(destinations_file)
    records = []
    
    for i in range(1000):
        user_id = f"U{str(i+1).zfill(4)}"
        gender = random.choice(['f', 'm', 'nb'])
        age = random.randint(18, 75)
        
        # Select random destination
        destination = random.choice(list(destinations.keys()))
        destination_data = destinations[destination]
        
        # Generate dates and get temperature
        start_date, end_date = generate_dates()
        month = start_date.month
        temp_range = get_monthly_temp_range(destination_data, month)
        min_temp, max_temp = temp_range
        avg_temp = sum(temp_range) / 2
        
        # Determine luggage type based on trip duration
        duration = (end_date - start_date).days
        if duration <= 3:
            luggage_type = random.choice(['hand', 'carry_on'])
        else:
            luggage_type = random.choice(['carry_on', 'checked'])
        
        # Generate business trip probability based on destination and age
        is_business = random.random() < 0.3 if 25 <= age <= 65 else False
            
        record = {
            'user_id': user_id,
            'age': age,
            'gender': gender,
            'destination': destination,
            'country': destination_data['country'],
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'min_temp_celsius': min_temp,
            'max_temp_celsius': max_temp,
            'avg_temp_celsius': round(avg_temp, 1),
            'luggage_type': luggage_type,
            'trip_purpose': 'business' if is_business else 'leisure',
            'packed_items': generate_packing_list(
                gender, age, destination_data, avg_temp, duration, 
                luggage_type, is_business
            )
        }
        records.append(record)
    
    return records

def save_to_csv(records, filename='travel_packing_data.csv'):
    """Save the generated records to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    # Generate 100 records
    dataset = generate_dataset(1000)
    save_to_csv(dataset)
    print(f"Generated {len(dataset)} travel packing records.")
