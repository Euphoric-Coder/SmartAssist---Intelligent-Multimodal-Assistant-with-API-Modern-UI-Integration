def html_to_str(t="email"):
    while True:
        try:
            # Open and read the HTML file
            h_f = "./" + t + ".html"
            with open(h_f, 'r', encoding='utf-8') as html_file:
                # Read the content of the file into a string
                global html_content
                html_content = html_file.read()

            # Now, html_content contains the HTML content as a string
            break

        except FileNotFoundError:
            print("HTML file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    return html_content

print(html_to_str())
