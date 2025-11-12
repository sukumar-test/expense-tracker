student_library = []
while True:
    user_input = input("1. Take new book\n2. Return book\n3. Replace book\nEnter your choice: ")
    if user_input == "1":
        book_name = input("Enter book name: ")
        student_library.append(book_name)
        print("Student took books: ", student_library)
    elif user_input == "2":
        book_name = input("Enter name of the book you want to return: ")
        student_library.remove(book_name)
        print("Current books student have: ", student_library)
    elif user_input == "3":
        book_name = input("Enter name of the book you want to replace: ")
        book_index = student_library.index(book_name)
        student_library[book_index] = book_name + "_replaced"
        print("Current books student have: ", student_library)
    else:
        print("Select proper choice from 1, 2, 3")