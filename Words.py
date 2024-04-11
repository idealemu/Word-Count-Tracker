import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys

def get_date():
    return datetime.now().strftime("%d-%m-%Y")

def get_word_count():
    try:
        word_count = int(input("Enter the total word count for today: "))
        return word_count
    except ValueError:
        print("Please enter a valid integer.")
        return get_word_count()

def load_data(filename):
    try:
        with open(filename, 'r') as file:
            data = [line.strip().split(',') for line in file.readlines()]
        return {date: int(word_count) for date, word_count in data}
    except FileNotFoundError:
        return {}

def save_data(filename, data):
    with open(filename, 'w') as file:
        for date, word_count in data.items():
            file.write(f"{date},{word_count}\n")

def calculate_average(data):
    sorted_dates = sorted(data.keys())
    
    # Check if the last two elements are equal, and if so, exclude the last one from the calculation
    if len(sorted_dates) > 1 and data[sorted_dates[-1]] == data[sorted_dates[-2]]:
        del sorted_dates[-1]
    
    total_days = len(sorted_dates) - 1  # Total days excluding the first day and possibly the last one
    
    total_changes = sum(data[date] - data[sorted_dates[idx - 1]] for idx, date in enumerate(sorted_dates) if idx > 0 and data[date] != data[sorted_dates[idx - 1]])
    
    return total_changes / total_days if total_days > 0 else 0

def plot_word_count(data):
    dates = [datetime.strptime(date, "%d-%m-%Y") for date in data.keys()]
    word_counts = list(data.values())

    current_day = get_date() 
    if current_day not in data:
        previous_day = (datetime.strptime(current_day, "%d-%m-%Y") - timedelta(days=1)).strftime("%d-%m-%Y")
        if previous_day in data:
            data[current_day] = data[previous_day]
        else:
            data[current_day] = 0

    # Add current day's data to the plot
    current_day_datetime = datetime.strptime(current_day, "%d-%m-%Y")
    dates.append(current_day_datetime)
    word_counts.append(data[current_day])

    plt.figure(figsize=(10, 5))
    plt.plot(dates, word_counts, marker='o', linestyle='-', color='blue')  # Plot word counts
    
    # Circle current day's point with a red circle
    current_day_index = dates.index(current_day_datetime)
    plt.plot(dates[current_day_index], word_counts[current_day_index], marker='o', markersize=8, linestyle='', color='red')
    
    plt.title('Thesis Word Counter')
    plt.xlabel('Date')
    plt.ylabel('Word Count')
    plt.grid(True)
    
    # Set x-axis ticks to show one tick per day from April 1st to May 30th
    start_date = datetime.strptime("01-04-2024", "%d-%m-%Y")
    end_date = datetime.strptime("30-05-2024", "%d-%m-%Y")
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    plt.xticks(date_range, [date.strftime("%d-%m") for date in date_range], rotation=90)

    # Calculate and add label for average change in word count per day
    average = calculate_average(data)
    plt.text(0.05, 0.95, f'Average change per day: {average:.2f}', fontsize=14, transform=plt.gcf().transFigure, verticalalignment='top', ha='left')


    # Calculate and add label for remaining days until May 20th
    days_left_20 = (datetime.strptime("20-05-2024", "%d-%m-%Y") - datetime.now()).days
    plt.text(0.05, 0.9, f'Days until 20/5: ', fontsize=12, color='black', transform=plt.gcf().transFigure, verticalalignment='top', ha='left')
    plt.text(0.21, 0.9, f'{days_left_20}', fontsize=14, color='black', transform=plt.gcf().transFigure, verticalalignment='top', ha='left')

    # Calculate and add label for remaining days until May 30th
    days_left_30 = (datetime.strptime("30-05-2024", "%d-%m-%Y") - datetime.now()).days
    plt.text(0.05, 0.85, f'Days until 30/5: ', fontsize=12, color='black', transform=plt.gcf().transFigure, verticalalignment='top', ha='left')
    plt.text(0.21, 0.85, f'{days_left_30}', fontsize=14, color='red', transform=plt.gcf().transFigure, verticalalignment='top', ha='left')

    # Add some spacing
    plt.subplots_adjust(top=0.75, bottom=0.2)

    # Add expected progression lines
    expected_end_date = datetime.strptime("20-05-2024", "%d-%m-%Y")
    total_days = (expected_end_date - start_date).days
    target_word_count = 500 * 40

    expected_word_count = [(idx / total_days) * target_word_count for idx, date in enumerate(date_range) if date <= datetime.strptime("20-05-2024", "%d-%m-%Y")]
    plt.plot([date for date in date_range if date <= datetime.strptime("20-05-2024", "%d-%m-%Y")], expected_word_count, linestyle='--', color='green', label='Expected Progression')

    expected_word_count = [target_word_count for idx, date in enumerate(date_range) if date >= datetime.strptime("20-05-2024", "%d-%m-%Y")]
    plt.plot([date for date in date_range if date >= datetime.strptime("20-05-2024", "%d-%m-%Y")], expected_word_count, linestyle='--', color='green')

    plt.tight_layout()
    plt.legend()
    plt.show()

#----------------------------------------
def main():
    filename = "word_count_data.txt"
    data = load_data(filename)

    if len(sys.argv) > 1 and (sys.argv[1] == 'update' or sys.argv[1] == 'u'):
        today = get_date()
        if today in data:
            print(f"Word count for {today} already exists. Updating...")
        word_count = get_word_count()
        data[today] = word_count
        save_data(filename, data)
        print(f"Word count for {today} updated successfully.")

    plot_word_count(data)

if __name__ == "__main__":
    main()
