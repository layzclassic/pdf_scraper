import re
import pandas as pd
import PyPDF2
import os

def extract_info_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        data_list = []

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            person_matches = re.findall(r'\n([A-Za-z\s]+?),\s([A-Za-z\s]+?),\s’\d+', text)
            address_matches = re.findall(r'(\d+[\w\s\d.,]+)\nTel:', text)
            phone_matches = re.findall(r'Tel:\s(.+?)\n', text)
            email_matches = re.findall(r'([\w\.-]+@[\w\.-]+)', text)
            website_matches = re.findall(r'(https?://(?:www\.)?\w+\.\w+(?:\.\w+)?)', text)

            for i in range(len(person_matches)):
                last_name = person_matches[i][0].strip()
                first_name_candidates = person_matches[i][1].split()  # Split the second word into candidates
                first_name = ""

                for name in first_name_candidates:
                    if len(name.split()) > 1:
                        first_name = name.split()[-1]  # Use the last word if more than two words with a space
                        break
                    elif name[0].isupper():
                        first_name = name
                        break

                if not first_name:
                    if re.search(r'[A-Z].*[A-Z]', person_matches[i][1]):
                        name_parts = re.findall(r'[A-Z][a-z]*', person_matches[i][1])
                        if len(name_parts) >= 2:
                            first_name = name_parts[1] + person_matches[i][1].split(name_parts[1])[1]
                    else:
                        first_name = person_matches[i][1]

                name = f"{last_name}, {first_name}"

                address = address_matches[i].strip() if i < len(address_matches) else 'nan'
                phone_number = phone_matches[i].strip() if i < len(phone_matches) else 'nan'
                email = email_matches[i].strip() if i < len(email_matches) else 'nan'
                website = website_matches[i].strip() if i < len(website_matches) else 'nan'

                if email != 'nan':
                    print(f"Scraped email: {email}")

                data = {
                    'Last Name': last_name,
                    'First Name': first_name,
                    'Address': address,
                    'Phone Number': phone_number,
                    'Email': email,
                    'Website': website,
                    'Media Outlets': 'nan'
                }
                data_list.append(data)

        return data_list

def save_to_csv(data_list, base_name, file_path):
    filename = f"{base_name}.csv"
    count = 1

    while os.path.exists(os.path.join(file_path, filename)):
        count += 1
        suffix = f"_{count}"
        filename = f"{base_name}{suffix}.csv"

    file_path = os.path.join(file_path, filename)
    df = pd.DataFrame(data_list)
    df.to_csv(file_path, index=False)
    print(f"Data saved to: {file_path}")

# Provide the path to your PDF file
pdf_file_path = r'C:\Users\t490s\PycharmProjects\pdf_scraper\files\travel_writer_list_raw.pdf'

# Extract information from the PDF
data_list = extract_info_from_pdf(pdf_file_path)

# Provide the base name and file path to save the CSV file
base_name = 'pdf_data'
file_path = r'C:\Users\t490s\PycharmProjects\pdf_scraper\files'

# Save the data to a CSV file
save_to_csv(data_list, base_name, file_path)


# r'C:\Users\t490s\PycharmProjects\pdf_scraper\files\travel_writer_list_raw.pdf'
# file_path = r'C:\Users\t490s\PycharmProjects\pdf_scraper\files'
