from parsing_telegram_channels import parsing_info_from_channels
from database_functions.db_functions import save_data_to_database

# Open the file in read mode
with open("channels.txt", "r") as file:
    # Read lines from the file and store them in a list
    list_urls = file.readlines()

# Strip newline characters from each line and store in a new list
list_urls = [line.strip() for line in list_urls]


def parsing_end_save():
    list_dict = parsing_info_from_channels(list_urls)
    save_data_to_database(list_dict)


if __name__ == '__main__':
    parsing_end_save()
