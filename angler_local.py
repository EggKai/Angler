import argparse
import mailparser
import re, sys, ctypes, os, requests, warnings
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, scrolledtext, messagebox
from models import checkUrls, LLM_probablity, predict_spam_probability, predict_phishing_probability, extractUrls, is_downloadable, TEXT_EXTENSIONS, get_file_extension, predict_malware
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

    email_text = parsed_email.text_plain if parsed_email.text_plain else []
    email_text = "\n".join(email_text) if email_text else parsed_email.body

    urls = extract_urls(email_text)
    image_links = extract_image_links(urls)

    attachments = [
        {"filename": att["filename"], "size": len(att["payload"])}
        for att in parsed_email.attachments if att["filename"]
    ]

    return {
        "emailText": email_text,
        "urls": urls,
        "imageLinks": image_links,
        "attachments": attachments
    }

def check_content(data, verbose=False):
    """Check the verdict using the models and optionally display scores."""
    spam_score = predict_spam_probability(data['emailText'])
    phishing_score = predict_phishing_probability(data['emailText'])
    llm_score = LLM_probablity(data['emailText'])
    urls_checked = checkUrls(data['emailText'], data['urls'])
    file_names, saved_files, attachments = [], [], {}
    if downloadable_links:=list(filter(is_downloadable, data['urls']+ extractUrls(data['emailText']))):
        for file_url in downloadable_links:
            try:
                file_name = os.path.basename(file_url)  # Extract filename from URL
                if get_file_extension(file_name) in TEXT_EXTENSIONS:
                    file_path = os.path.join(r"server/tmp/", file_name)

                    response = requests.get(file_url, stream=True)
                    if response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        file_names.append(file_name)
                        saved_files.append(file_path)
                else:
                    attachments.update({file_name:False})
            except Exception as e:
                warnings.warn(f"Error downloading {file_url}: {e}")
    attachments.update({filename : predict_malware(filepath) for filename, filepath in zip(file_names, saved_files)})
    for file in saved_files:
        if os.path.exists(file):
            os.remove(file)
    if verbose:
        print(f"Spam Score: {spam_score}")
        print(f"Phishing Score: {phishing_score}")
        print(f"LLM Probability Score: {llm_score}")
        if urls_checked:
            print(f"URLs: {urls_checked}")
        if attachments:
            print(f"Attachments: {attachments}")
    return { 
        "Spam Score" : spam_score, 
        "Phishing Score" : phishing_score, 
        "LLM Score" : llm_score, 
        "urls filtered" : urls_checked,
        "attachment filtered" : attachments
    }
def check_verdict(data):
    """Check the verdict using the models and optionally display scores."""
    spam_score = data['Spam Score']
    phishing_score =  data['Phishing Score']
    llm_score =  data['LLM Score']
    urls_checked = data['urls filtered']
    attachments = data['attachment filtered']
    is_malicious = (
        spam_score >= 96
        or phishing_score >= 84
        or llm_score >= 50
        or any(urls_checked.values())
        or any(attachments.values())
    )
    return "Malicious" if is_malicious else "Safe"

    
"""Run the GUI application."""
def browse_files():
    global email_data_store
    """Open a file dialog to select .eml files and display verdicts."""
    file_paths = filedialog.askopenfilenames(filetypes=[("Email Files", "*.eml")])
    
    if not file_paths:
        return  # No file selected
    
    verdict_listbox.delete(0, tk.END)  # Clear previous results
    email_data_store = {}  # Reset stored email data

    for file_path in file_paths:
        extracted_data = extract_eml_data(file_path)
        checked =  check_content(extracted_data)
        verdict = check_verdict(checked)
        filename = file_path.split("/")[-1]  # Extract filename for display

        email_data_store[filename] = extracted_data  # Store data for later viewing
        email_data_store[filename].update(checked)  # Store data for later viewing
        verdict_listbox.insert(tk.END, f"{filename} - Verdict: {verdict}")

def view_details():
    """Open a new window to display full email details when a file is selected."""
    try:
        selected_index = verdict_listbox.curselection()[0]
        selected_text = verdict_listbox.get(selected_index)
        filename = selected_text.split(" - Verdict: ")[0]

        email_details = email_data_store.get(filename, None)
        if not email_details:
            messagebox.showerror("Error", "Email details not found.")
            return

        details_window = tk.Toplevel(root)
        # icon = ImageTk.PhotoImage(Image.open("angler-js/logo.png"))
        # details_window.tk.call('wm', 'iconphoto', details_window._w, icon)

        details_window.title(f"Details - {filename}")
        details_window.geometry("800x500")

        details_text = scrolledtext.ScrolledText(details_window, wrap=tk.WORD, width=100, height=30, font=("Arial", 10))
        details_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        details_text.insert(tk.END, f"File: {filename}\n")
        details_text.insert(tk.END, "-" * 60 + "\n")
        details_text.insert(tk.END, f"Email Text:\n{email_details['emailText']}\n\n")
        if email_details['imageLinks']:
            details_text.insert(tk.END, f"Image Links:\n{', '.join(email_details['imageLinks'])}\n\n")
        details_text.insert(tk.END, f"Spam Score:{email_details['Spam Score']}\n\n")
        details_text.insert(tk.END, f"Phishing Score:{email_details['Phishing Score']}\n\n")
        details_text.insert(tk.END, f"LLM probability Score:{email_details['LLM Score']}\n\n")
        details_text.insert(tk.END, f"URLs:\n{email_details['urls filtered']}\n\n")
        if email_details["attachments"]:
            details_text.insert(tk.END, "Attachments:\n")
            for att in email_details["attachments"]:
                details_text.insert(tk.END, f" - {att['filename']} ({att['size']} bytes)\n")

        details_text.insert(tk.END, "\n" + "=" * 80 + "\n\n")
    except IndexError:
        messagebox.showerror("Error", "Please select an email to view details.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze EML files for spam and phishing threats.")
    parser.add_argument("files", nargs="*", help="Paths to EML files to analyze.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed scores.")

    args = parser.parse_args()

    if args.files:
        for file in args.files:
            try:
                data = extract_eml_data(file)
                checked = check_content(data, args.verbose)
                verdict = check_verdict(checked)
                print(f"{file}: {verdict}")
            except Exception as e:
                print(f"Error processing {file}: {e}")
    else:
        root = tk.Tk()
        root.title("Angler Local")
        root.geometry("600x400")
        icon = ImageTk.PhotoImage(Image.open("angler-js/logo.png"))

        if sys.platform.startswith("win"):
            app_id = "com.sit.kai.angler" #unique ID so that it doesnt display python's process icon
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        root.tk.call('wm', 'iconphoto', root._w, icon)

        browse_button = tk.Button(root, text="Browse EML Files", command=browse_files, font=("Arial", 12))
        browse_button.pack(pady=10)

        global verdict_listbox
        verdict_listbox = tk.Listbox(root, width=80, height=15, font=("Arial", 10))
        verdict_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        details_button = tk.Button(root, text="View Details", command=view_details, font=("Arial", 12))
        details_button.pack(pady=10)

        root.mainloop()
