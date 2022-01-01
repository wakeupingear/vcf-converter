import vobject


def parse_vcard(path):
    result = []
    with open(path, "r") as f:
        for vcard in vobject.readComponents(f):
            result.append(vcard)
    return result


def __main__():
    data = parse_vcard("./Contacts.vcf")
    f = open("output.txt", "w")
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
            and "chandlerschool.org" in entry.contents["email"][0].value
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
                or item == "x-android-custom"
            ):
                continue
            val = entry.contents[item][0].value
            if item == "tel":
                val.replace("-", "").replace(" ", "")
                if val[0:1] == "+":
                    val = val[2:]
            data += " " + val
        data.replace("  ", " ").replace(";", "")
        f.write(data + "\n")
    f.close()


if __name__ == "__main__":
    __main__()
