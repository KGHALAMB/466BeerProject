#Convert user's Untappd profile to CSV

# Open the text file
import csv

with open('del.txt', 'r') as file:
    # Read lines from the file
    lines = file.readlines()

with open('tempUser.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)

    # Write header
    csvwriter.writerow(['Beer Name','Their Rating'
])


    # Iterate over lines
    i = 0
    while i < len(lines):
        beer_info = 0
        # Check if the line contains 'is drinking an'
        if ('is drinking an' in lines[i]):
            beer_info = lines[i].split('is drinking an ')[1].split(' by ')

        elif ('is drinking a' in lines[i]):
            beer_info = lines[i].split('is drinking a ')[1].split(' by ')
            # Extract the type of beer
        if (beer_info):
            if len(beer_info) > 1:
                beer_type = beer_info[0]
            else:
                beer_type = "Unknown"

            # Extract the rating (line after 'View Detailed Check-in')
            j = i + 1
            while j < len(lines):
                if 'View Detailed Check-in' in lines[j]:
                    if j+1 < len(lines):
                        rating = lines[j+1].strip()
                    else:
                        rating = "Unknown"
                    break
                j += 1

            # Output the type of beer and rating
            csvwriter.writerow([beer_type, rating])

            # Skip to the next check-in
            i = j + 1
        else:
            i += 1
