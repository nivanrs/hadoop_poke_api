import requests
import csv

def fetch_and_save_pokemon_abilities(start_id, end_id, filename):
    abilities = []
    for ability_id in range(start_id, end_id + 1):
        url = f"https://pokeapi.co/api/v2/ability/{ability_id}"
        response = requests.get(url)
        if response.status_code == 200:
            abilities.append(response.json())
        else:
            print(f"Failed to fetch ability with ID {ability_id}")
            return False  # Stop fetching on failure
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "effect", "short_effect"])
        
        for ability in abilities:
            for effect_entry in ability.get('effect_entries', []):
                if effect_entry.get('language', {}).get('name') == 'en':
                    writer.writerow([
                        ability.get('id'),
                        ability.get('name'),
                        effect_entry.get('effect'),
                        effect_entry.get('short_effect')
                    ])
    return True

def main():
    batch_size = 100
    total_abilities = 999
    for start_id in range(1, total_abilities + 1, batch_size):
        end_id = min(start_id + batch_size - 1, total_abilities)
        filename = f"pokemon_abilities_{start_id}_to_{end_id}.csv"
        if not fetch_and_save_pokemon_abilities(start_id, end_id, filename):
            print(f"Stopping at abilities {start_id} to {end_id} due to failure.")
            break
        print(f"Saved abilities {start_id} to {end_id} in {filename}")

if __name__ == "__main__":
    main()