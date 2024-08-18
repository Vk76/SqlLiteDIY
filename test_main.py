import subprocess


def run_script(commands):
    # Run the command-line utility in a subprocess
    raw_output = None
    with subprocess.Popen(['./main'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) as process:
        # Send the commands to the utility
        for command in commands:
            process.stdin.write(command + '\n')

        # Capture the entire output
        raw_output, _ = process.communicate()
        
        process.stdin.close()  # Close the input to signal EOF

    # Split the output into lines and return it
    return raw_output.splitlines()


def test_inserts_and_retrieves_a_row():
    # Send commands to insert a row and retrieve it
    result = run_script([
        "insert 1 user1 person1@example.com",
        "select",
        ".exit",
    ])
    
    # Compare the output to the expected result
    assert result == [
        "db > Executed.",
        "db > (1, user1, person1@example.com)",
        "Executed.",
        "db > ",
    ]
    
def test_print_error_message_when_table_is_full():
    inputs = []
    for i in range(1,1402):
        inputs.append(f"insert {i} user{i} person{i}@example.com ")
    inputs.append(".exit")
    
    result = run_script(inputs)
    
    assert result[-2] == "db > Error : Table full."
    
    
def test_allows_inserting_strings_of_maximum_length():
    # Define maximum length strings
    long_username = "a" * 32
    long_email = "a" * 255

    # Create the script to be executed
    script = [
        f"insert 1 {long_username} {long_email}",
        "select",
        ".exit",
    ]

    # Run the script
    result = run_script(script)

    # Expected output
    expected_result = [
        "db > Executed.",
        f"db > (1, {long_username}, {long_email})",
        "Executed.",
        "db > ",
    ]

    # Assert that the result matches the expected output
    assert result == expected_result


def test_prints_error_message_if_strings_are_too_long():
    long_username = "a" * 33
    long_email = "a" * 256
    script = [
        f"insert 1 {long_username} {long_email}",
        "select",
        ".exit",
    ]
    result = run_script(script)

    expected_result = [
        "db > String is too long.",
        "db > Executed.",
        "db > ",
    ]

    assert result == expected_result
    
    
def test_prints_error_message_if_id_is_negative():
    script = [
        "insert -1 cstack foo@bar.com",
        "select",
        ".exit",
    ]
    result = run_script(script)

    expected_result = [
        "db > ID must be positive.",
        "db > Executed.",
        "db > ",
    ]

    assert result == expected_result
