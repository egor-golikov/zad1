from emulator import ShellEmulator

if __name__ == "__main__":
    emulator = ShellEmulator("config.ini")
    print("Welcome to the Shell Emulator! Type 'exit' to quit.\n")

    while True:
        command = input(emulator.prompt())
        result = emulator.run_command(command)
        if result == "exit":
            emulator.cleanup()
            print("Goodbye!")
            break
        else:
            print(result)
