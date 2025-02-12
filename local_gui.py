import mailparser
import re
import tkinter as tk
from tkinter import filedialog, scrolledtext
from models import checkUrls, LLM_probablity, predict_spam_probability, predict_phishing_probability
def extract_urls(text):
    """Extract URLs from text using regex."""
    url_pattern = r"https?://[^\s]+"
    return re.findall(url_pattern, text)

def extract_image_links(urls):
    """Filter image links from a list of URLs."""
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp")
    return [url for url in urls if url.lower().endswith(image_extensions)]

def extract_eml_data(file_path):
    """Extract email text, URLs, image links, and attachments from an .eml file."""
    parsed_email = mailparser.parse_from_file(file_path)

    # Extract email text
    email_text = parsed_email.text_plain if parsed_email.text_plain else []
    email_text = "\n".join(email_text) if email_text else parsed_email.body

    # Extract URLs
    urls = extract_urls(email_text)

    # Extract image links
    image_links = extract_image_links(urls)

    # Extract attachments
    attachments = [
        {"filename": att["filename"], "size": len(att["payload"])}
        for att in parsed_email.attachments if att["filename"]
    ]

    # Construct the final dictionary
    data = {
        "emailText": email_text,
        "urls": urls,
        "imageLinks": image_links,
        "attachments": attachments
    }
    return data

def browse_files():
    """Open a file dialog to select .eml files and display extracted data."""
    file_paths = filedialog.askopenfilenames(filetypes=[("Email Files", "*.eml")])
    
    if not file_paths:
        return  # No file selected
    
    result_text.delete("1.0", tk.END)  # Clear previous output

    for file_path in file_paths:
        extracted_data = extract_eml_data(file_path)

        # Display extracted data in the text box
        result_text.insert(tk.END, f"\nFile: {file_path}\n")
        result_text.insert(tk.END, "-" * 60 + "\n")
        result_text.insert(tk.END, f"Email Text:\n{predict_phishing_probability(extracted_data['emailText'])}\n\n")
        result_text.insert(tk.END, f"Email Text:\n{predict_spam_probability(extracted_data['emailText'])}\n\n")
        result_text.insert(tk.END, f"LLM Probablity:\n{LLM_probablity(extracted_data['emailText'])}\n\n")
        if extracted_data['urls']:
            result_text.insert(tk.END, f"URLs:\n{', '.join(checkUrls(extracted_data['emailText'], extracted_data['urls']))}\n\n")
        result_text.insert(tk.END, f"Image Links:\n{', '.join(extracted_data['imageLinks'])}\n\n")

        result_text.insert(tk.END, "Attachments:\n")
        for att in extracted_data["attachments"]:
            result_text.insert(tk.END, f" - {att['filename']} ({att['size']} bytes)\n")

        result_text.insert(tk.END, "\n" + "=" * 80 + "\n\n")

if __name__ == "__main__":
    # Create GUI window
    root = tk.Tk()
    root.title("EML File Extractor")
    root.geometry("800x600")

    # File selection button
    browse_button = tk.Button(root, text="Browse EML Files", command=browse_files, font=("Arial", 12))
    browse_button.pack(pady=10)

    # Scrollable text box for output
    result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30, font=("Arial", 10))
    result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Run the application
    root.mainloop() 
