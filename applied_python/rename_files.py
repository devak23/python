import os

ALLOWED_EXTENSIONS = ['.pdf', '.PDF', '.epub', '.EPUB']

def rename_files(folder):
    print("Renaming files in the folder: {}".format(folder))
    files = [f for f in os.listdir(folder)
             if is_extn_allowed(f)]

    for f in files:
        new_name = f.replace("_OceanofPDF.com_","").replace("_"," ").replace("-"," ").replace("   "," ")
        old_file_path = os.path.join(folder, f)
        new_file_path = os.path.join(folder, new_name)
        if not os.path.exists(new_file_path):
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {old_file_path} to {new_file_path}")


def is_extn_allowed(f):
    return [xtn for xtn in ALLOWED_EXTENSIONS if f.endswith(xtn)]


if __name__ == "__main__":
    rename_files("/home/abhay/Downloads/")

# output:
# Renaming files in the folder: /home/abhay/Downloads/
# Renamed: /home/abhay/Downloads/Grokking_Web_Application_Security_-_Malcolm_McDonald.pdf to /home/abhay/Downloads/Grokking Web Application Security - Malcolm McDonald.pdf
# Renamed: /home/abhay/Downloads/Grokking_Machine_Learning_-_Luis_Serrano.pdf to /home/abhay/Downloads/Grokking Machine Learning - Luis Serrano.pdf
# Renamed: /home/abhay/Downloads/Learning_Functional_Programming_Managing_Code_Complexity_-_Jack_Widman.pdf to /home/abhay/Downloads/Learning Functional Programming Managing Code Complexity - Jack Widman.pdf
# Renamed: /home/abhay/Downloads/Regular_Expressions_Machinery_-_Staffan_Noteberg.pdf to /home/abhay/Downloads/Regular Expressions Machinery - Staffan Noteberg.pdf
# Renamed: /home/abhay/Downloads/Grokking_Concurrency_-_Kirill_Bobrov.pdf to /home/abhay/Downloads/Grokking Concurrency - Kirill Bobrov.pdf
# Renamed: /home/abhay/Downloads/Rust Essentials A Comprehensive Guide - Aarav_Joshi.pdf to /home/abhay/Downloads/Rust Essentials A Comprehensive Guide - Aarav Joshi.pdf
# Renamed: /home/abhay/Downloads/OBJECT_ORIENTED_AND_FUNCTIONAL_PROGRAMMING_-_Pena_Leonel.pdf to /home/abhay/Downloads/OBJECT ORIENTED AND FUNCTIONAL PROGRAMMING - Pena Leonel.pdf
# Renamed: /home/abhay/Downloads/Selected Writings on Computing - Dijkstra, Edsger W._5544.pdf to /home/abhay/Downloads/Selected Writings on Computing - Dijkstra, Edsger W. 5544.pdf
# Renamed: /home/abhay/Downloads/Grokking_Streaming_Systems_-_Josh_Fischer.pdf to /home/abhay/Downloads/Grokking Streaming Systems - Josh Fischer.pdf
# Renamed: /home/abhay/Downloads/grokking_artificial_intelligence_algorithms_-_Rishal_Hurbans.pdf to /home/abhay/Downloads/grokking artificial intelligence algorithms - Rishal Hurbans.pdf
# Renamed: /home/abhay/Downloads/JavaScript_QuickStart_Guide_-_Robert_Oliver.pdf to /home/abhay/Downloads/JavaScript QuickStart Guide - Robert Oliver.pdf
# Renamed: /home/abhay/Downloads/Charles Petzold-Code_ The Hidden Language of Computer Hardware and Software-Microsoft Press (2000).pdf to /home/abhay/Downloads/Charles Petzold-Code  The Hidden Language of Computer Hardware and Software-Microsoft Press (2000).pdf
# Renamed: /home/abhay/Downloads/Grokking_The_Java_Developer_Interview__Mor_-_Jatin_Arora.pdf to /home/abhay/Downloads/Grokking The Java Developer Interview  Mor - Jatin Arora.pdf
# Renamed: /home/abhay/Downloads/Grokking_Algorithms_Blueprint_Advanced_-_William_Turner.pdf to /home/abhay/Downloads/Grokking Algorithms Blueprint Advanced - William Turner.pdf
# Renamed: /home/abhay/Downloads/Clean Code With Java - Best practices 101- Aarav_Joshi.pdf to /home/abhay/Downloads/Clean Code With Java - Best practices 101- Aarav Joshi.pdf
# Process finished with exit code 0