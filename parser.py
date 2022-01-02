import vobject
import os
import sys


def parse_vcard(path):
    result = []
    with open(path, "r") as f:
        for vcard in vobject.readComponents(f):
            result.append(vcard)
    return result


def __main__():
    if len(sys.argv) < 2:
        print("Usage: python parser.py <file> <optional-args>")
        exit(1)
    data = parse_vcard(sys.argv[1])
    f = open("output.txt", "w")
    print("Parsing data")
    for entry in data:
        if "fn" in entry.contents:
            data = entry.contents["fn"][0].value
        elif "n" in entry.contents:
            data = entry.contents["n"][0].value
        else:
            continue
        if data == "" or data[0:1] == "#":
            continue
        if (
            "email" in entry.contents
            and len(entry.contents.keys()) < 6
            and (
                "chandlerschool.org" in entry.contents["email"][0].value
                or "hwemail.com" in entry.contents["email"][0].value
            )
        ):
            continue
        for item in entry.contents:
            if (
                item == "fn"
                or item == "n"
                or item == "version"
                or item == "photo"
                or item == "adr"
                or item == "org"
            ):
                continue
            val = entry.contents[item][0].value
            if item == "x-android-custom":
                val = "/ " + (
                    val.replace("vnd.android.cursor.item/nickname", "")
                    .replace(";1", "")
                    .replace(";", "")
                )
            elif item == "tel":
                val = val.replace("-", "").replace(" ", "")
                if val[0:1] == "+":
                    val = val[2:]
            data += " " + val
        data = data.replace("  ", " ").replace(";", "")
        f.write(data + "\n")
    f.close()
    print("Converting to index")

    os.system("node import.js ./output.txt " + "".join(sys.argv[2:]))


if __name__ == "__main__":
    __main__()
