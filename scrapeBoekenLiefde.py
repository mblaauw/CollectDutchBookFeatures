__author__ = 'MBlaauw'
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")

# Reviews
# https://boekenliefde.nl/edition_reviews_get.api?key=47L0ss6cDInejrV8SpJmPk4AgxEZTpEXy0BNQzvQ&isbn=9789047201441&type=text&outputformat=xml

# Details
# https://boekenliefde.nl/edition_info_get.api?key=47L0ss6cDInejrV8SpJmPk4AgxEZTpEXy0BNQzvQ&isbn=9789047201441&outputformat=xml

# Load inititial ISBN list
isbn_file = open('unqiue_isbn10_list.txt', 'r')
lines = isbn_file.readlines()
lines = [line[:-1] for line in lines]

for eachLine in lines:
    new_url = 'https://boekenliefde.nl/edition_info_get.api?key=47L0ss6cDInejrV8SpJmPk4AgxEZTpEXy0BNQzvQ&isbn=' + str(eachLine) + '&outputformat=xml'
    print new_url


