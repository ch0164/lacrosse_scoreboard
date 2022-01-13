from code_generator import CodeGenerator

if __name__ == "__main__":
    # Filename and code to test out CodeGenerator class.
    test_file = "test.cpp"
    code = [
        "#include <iostream>",
        "",
        "int main(void) {",
        "std::cout << \"Hello World\" << std::endl;",
        "}"
    ]

    # Open the output file and write code to it using CodeGenerator object.
    with open(test_file, "w") as file:
        cpp = CodeGenerator(test_file, file)
        cpp.write_file(code)
