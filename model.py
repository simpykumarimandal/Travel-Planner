import pandas as pd
from geopy.distance import geodesic

def calculate_distance(source_lat, source_long, dest_lat, dest_long):
    if pd.notnull(dest_lat) and pd.notnull(dest_long):
        source_coords = (source_lat, source_long)
        dest_coords = (dest_lat, dest_long)
        distance = geodesic(source_coords, dest_coords).kilometers
        return distance
    else:
        return float('inf')  # Return infinity if destination coordinates are missing

def generate_travel_plan(destination, num_days, budget, interest, num_destinations_per_day):
    dataset_path = r"C:\Users\simkm\Desktop\project2.0\dataset\finalll 1.csv"
    places_dataset = pd.read_csv(dataset_path, encoding='latin1')

    places_dataset = places_dataset[(places_dataset['City'].str.lower() == destination.lower()) &
                                    (places_dataset['Interest'].str.lower() == interest.lower())]

    start_lat = 28.6139
    start_long = 77.2090

    places_dataset['distance'] = places_dataset.apply(
        lambda row: calculate_distance(start_lat, start_long, row['Latitude'], row['Longitude']), axis=1)

    affordable_places = places_dataset[places_dataset['Entrance Fee in INR'] <= budget]
    affordable_places = affordable_places.sort_values(by=['distance', 'Entrance Fee in INR'])

    travel_plan = f"Travel plan for {num_days} days to {destination} with interest in {interest} within a budget of INR {budget}:\n\n"

    places_available = len(affordable_places)
    destination_titles = ["Morning Destination:", "Afternoon Destination:", "Evening Destination:"]

    for day in range(num_days):
        travel_plan += f"Day {day + 1}:\n"
        daily_destinations = affordable_places.iloc[day * num_destinations_per_day: (day + 1) * num_destinations_per_day]

        if len(daily_destinations) == 0:
            travel_plan += "Sorry, we are out of places for today.\n"
            continue

        for i, row in enumerate(daily_destinations.iterrows()):
            travel_plan += destination_titles[i] + '\n'
            travel_plan += f"{row[1]['Name']} - \n"
            travel_plan += f"Google rating: {row[1]['Google review rating']}\n"
            travel_plan += f"Entrance Fee: {row[1]['Entrance Fee in INR']} INR\n"
            travel_plan += f"Distance: {row[1]['distance']:.2f} km\n\n"

    if places_available < num_days * num_destinations_per_day:
        days_without_places = (num_days * num_destinations_per_day) - places_available

    return travel_plan

def main():
    destination = input("Enter the City: ")
    interest = input("Enter your Interest: ")
    num_days = int(input("Enter number of days of the plan: "))
    budget = float(input("Enter your total budget for entrance fees in INR: "))
    num_destinations_per_day = int(input("Enter the number of destinations in one day (1, 2, or 3): "))

    plan = generate_travel_plan(destination, num_days, budget, interest, num_destinations_per_day)
    print(plan)

if __name__ == "__main__":
    main()
