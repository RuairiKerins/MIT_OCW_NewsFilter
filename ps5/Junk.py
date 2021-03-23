def load_input(filename):
    with open(filename) as infile:
        B, L, D = infile.readline().strip().split(" ")
        scores = [int(x) for x in infile.readline().strip().split(" ")]
        libraries = []
        index = 0
        while True:
            line1 = infile.readline().strip()
            line2 = infile.readline().strip()
            if not line2:
                break
            book_count, signup_time, scan_rate = line1.split(" ")
            books = [int(x) for x in line2.split()]
            libraries.append(
                Library(index, int(book_count), int(signup_time), int(scan_rate), books))
            index += 1
    return int(B), int(L), int(D), scores, libraries