import os


def rename_files(folder):
    print("Renaming files in the folder: {}".format(folder))
    with os.scandir(folder) as files:
        for file in files:
            if not file.is_dir() and file.name.strip().startswith("_OceanofPDF.com_"):
                old_name = os.path.join(folder, file.name)
                new_name = os.path.join(folder, file.name.replace("_OceanofPDF.com_", ""))
                print ("old_name: {}, new_name: {}".format(old_name, new_name))
                os.rename(old_name, new_name)
            else:
                print("COMPLETELY SKIPPING: {}".format(file.name))


if __name__ == "__main__":
    rename_files("/home/abhay/Downloads/")

# output:
# /usr/bin/python3.13 /home/abhay/Workspace/group-pogramming/rename_files.py
# Renaming files in the folder: /home/abhay/Downloads/PDF/Python
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Visualizing_Quantum_Mechanics_with_Python_-_Stephen_Spicklemire.pdf, new_name: /home/abhay/Downloads/PDF/Python/Visualizing_Quantum_Mechanics_with_Python_-_Stephen_Spicklemire.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Advanced_Python_Programming_-_Robert_Karamagi.pdf, new_name: /home/abhay/Downloads/PDF/Python/Advanced_Python_Programming_-_Robert_Karamagi.pdf
# COMPLETELY SKIPPING: Mastering Basic Algorithms in the Python Language.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_5_Python_Basic_Games_You_Must_Learn_To_Code_-_Ritesh_Kumar.pdf, new_name: /home/abhay/Downloads/PDF/Python/5_Python_Basic_Games_You_Must_Learn_To_Code_-_Ritesh_Kumar.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Python_Mastery_A_Hands-On_Guide_-_Ben_Marriachi.pdf, new_name: /home/abhay/Downloads/PDF/Python/Python_Mastery_A_Hands-On_Guide_-_Ben_Marriachi.pdf
# COMPLETELY SKIPPING: Let Us Python by Yashavant Kanetkar Aditya Kanetkar.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Functional_Python_Programming_-_Steven_F_Lott.pdf, new_name: /home/abhay/Downloads/PDF/Python/Functional_Python_Programming_-_Steven_F_Lott.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Learn_AI_with_Python_-_Gaurav_Leekha.pdf, new_name: /home/abhay/Downloads/PDF/Python/Learn_AI_with_Python_-_Gaurav_Leekha.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Python_Programming_-_Brian_Evenson.pdf, new_name: /home/abhay/Downloads/PDF/Python/Python_Programming_-_Brian_Evenson.pdf
# COMPLETELY SKIPPING: let-us-python-solutions-5th-edition.epub
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Designing_Data_intensive_application_in_Python_-_Aarav_Joshi.pdf, new_name: /home/abhay/Downloads/PDF/Python/Designing_Data_intensive_application_in_Python_-_Aarav_Joshi.pdf
# COMPLETELY SKIPPING: Microservices Patterns_ With examples in Java ( PDFDrive ).pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Learn_OpenCV_with_Python_by_Exercises_-_Jeffrey_Leon_Stroup.pdf, new_name: /home/abhay/Downloads/PDF/Python/Learn_OpenCV_with_Python_by_Exercises_-_Jeffrey_Leon_Stroup.pdf
# COMPLETELY SKIPPING: let-us-python.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Python_in_Depth_Programmers_Guide_-_Nathan_Venture.pdf, new_name: /home/abhay/Downloads/PDF/Python/Python_in_Depth_Programmers_Guide_-_Nathan_Venture.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Useful_Python_-_Stuart_Langridge.pdf, new_name: /home/abhay/Downloads/PDF/Python/Useful_Python_-_Stuart_Langridge.pdf
# COMPLETELY SKIPPING: learn-python3-the-hard-way-nov-15-2018.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Python_Programming_for_Lucrative_Careers_-_Hubie_Chen.pdf, new_name: /home/abhay/Downloads/PDF/Python/Python_Programming_for_Lucrative_Careers_-_Hubie_Chen.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Think_Python_3rd_Ed_Final_Release_-_Allen_B_Downey.pdf, new_name: /home/abhay/Downloads/PDF/Python/Think_Python_3rd_Ed_Final_Release_-_Allen_B_Downey.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Pydonts_-_Write_elegant_Python_code_-_Rodrigo_Girao_Serrao.pdf, new_name: /home/abhay/Downloads/PDF/Python/Pydonts_-_Write_elegant_Python_code_-_Rodrigo_Girao_Serrao.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Python_for_TensorFlow_Pocket_Primer_-_Oswald_Campesato.pdf, new_name: /home/abhay/Downloads/PDF/Python/Python_for_TensorFlow_Pocket_Primer_-_Oswald_Campesato.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_1000_Python_Examples_-_Gabor_Szabo.pdf, new_name: /home/abhay/Downloads/PDF/Python/1000_Python_Examples_-_Gabor_Szabo.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Pythonic_AI_A_beginners_guide_-_Arindam_Banerjee.pdf, new_name: /home/abhay/Downloads/PDF/Python/Pythonic_AI_A_beginners_guide_-_Arindam_Banerjee.pdf
# COMPLETELY SKIPPING: cookie
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Python_3_Using_ChatGPT__GPT-4_-_O_Oswald_Campesato.pdf, new_name: /home/abhay/Downloads/PDF/Python/Python_3_Using_ChatGPT__GPT-4_-_O_Oswald_Campesato.pdf
# COMPLETELY SKIPPING: designing-microservices-with-django.pdf
# COMPLETELY SKIPPING: DATA STRUCTURES THROUGH PYTHON(R20A0503).pdf
# COMPLETELY SKIPPING: The Pythonic Way.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Python_One-Liners_-_Christian_Mayer.pdf, new_name: /home/abhay/Downloads/PDF/Python/Python_One-Liners_-_Christian_Mayer.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Better_Python_Code_-_David_Mertz.pdf, new_name: /home/abhay/Downloads/PDF/Python/Better_Python_Code_-_David_Mertz.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_Introduction_to_Python_and_LLMs_-_Dilyan_Grigorov.pdf, new_name: /home/abhay/Downloads/PDF/Python/Introduction_to_Python_and_LLMs_-_Dilyan_Grigorov.pdf
# old_name: /home/abhay/Downloads/PDF/Python/_OceanofPDF.com_100_Days_of_Coding_in_Python_-_Giuliana_Carullo.pdf, new_name: /home/abhay/Downloads/PDF/Python/100_Days_of_Coding_in_Python_-_Giuliana_Carullo.pdf
#
# Process finished with exit code 0