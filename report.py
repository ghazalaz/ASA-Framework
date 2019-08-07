import globals,sys
def main():
    address = ""
    if len(sys.argv) == 2:
        address = sys.argv[1]
    globals.print_device(address)
if __name__ == "__main__":
    main()