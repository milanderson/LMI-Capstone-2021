import DocExtract
import re
import string
import pandas as pd


# allDocs = DocExtract.DocExtract()
# allDocs.get_text(doc_type='all', test=True)


def hasTOC(dictionary):
    """

    :param dictionary:
    :return:
    """

    TOC = []
    noTOC = []

    string = re.compile("Table of Contents|TABLE OF CONTENTS")

    for i, text in enumerate(dictionary["cleaned_text_list"]):
        # Change text from str type to list type
        text = text.lstrip("[")
        text = text.rstrip("]")
        text = text.split("',")

        noMatch = []
        match = []
        new_text = []
        for j, k in enumerate(text):
            # Search for table of contents, append to appropriate list
            k = k.lstrip("'")
            k = k.replace(" '", "", 1)
            search = re.search(string, k)
            new_text.append(k)

            # Search for table of contents, append to appropriate list
            search = re.search(string, k)

            if not search:
                noMatch.append(j)
            else:
                match.append(j)
        if match:
            TOC.append((new_text, dictionary["cleaned_text"][i], match[0]))
        elif noMatch:
            noTOC.append(new_text)
        else:
            print("There was an error in the matching process. Both lists are empty.")

    return TOC, noTOC


def sectionSegmentation(docs, TOC=True):
    """

    :param docs:
    :param TOC:
    :return:
    """

    # segmenting text with a Table of Contents
    if TOC:
        final_segmented_text = []
        unsegmented_count = 0
        for text, cleaned_text, index in docs:

            # Pull the first section index to know when the Table of contents ends
            # Cleans any extra periods or numbers after the text
            first_section = re.sub(r'\s*[\.]+\s*[0-9]+', '', text[index + 1].lower())
            print(f"The first section title is: {first_section}")

            # Finds first mention of first section after the TOC
            section_index = [c for c, k in enumerate(text) if re.search(first_section, k.lower(), re.MULTILINE)]
            if len(section_index) == 1:
                print("Beginning of first section not found. Trying again. . .")
                first_section = re.sub(r'[^a-zA-Z.\d\s]', '', first_section)
                first_section = re.sub(r'\s\s', ' ', first_section)
                print(f"The (cleaner) first section title is: {first_section}")
                section_index = [c for c, k in enumerate(text) if re.search(first_section, k.lower(), re.MULTILINE)]

            # Looking for Enclosure in the first section title - create unique case for these since they always fail
            if re.match(r"enclosure", first_section):
                print("Enclosure format detected. Attempting one more time. . .")
                first_section = first_section.split()
                enclosure = re.compile(first_section[0].strip() + " " + first_section[1].strip())
                section_index = [c for c, k in enumerate(text) if re.search(enclosure, k.lower())]

            try:
                # Separate Table of Contents
                table_of_contents = text[(index + 1):section_index[1]]
            except IndexError:
                print("First section could not be found - Table of Contents could not be separated.")
                print("Document unable to be segmented.")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
                unsegmented_count += 1
                continue

            # Create list of sections from Table of Contents
            sections = []
            i = 0
            for line in table_of_contents:
                pattern = re.compile('\s*[\.]+\s+[0-9]+')
                if re.search(pattern, line):
                    sections.append(re.sub(pattern, '', line).rstrip(string.digits))
                    i += 1
                else:
                    try:
                        if re.search(pattern, table_of_contents[i + 1]):
                            new_line = line + re.sub(pattern, '', table_of_contents[i + 1]).rstrip(string.digits)
                            print(new_line)
                            sections.append(new_line)
                            i += 2
                    except:
                        continue

            # Remove tables or figures from the sections
            table_figure = re.compile("TABLE|Table|table|FIGURE|Figure|figure")
            sections = [section.lower() for section in sections if not re.search(table_figure, section)]

            # Used cleaned_text to first separate out preamble and table of contents
            try:
                segmented_text = {"Preamble": cleaned_text[:index]}
                print("Added Preamble to the segmented_text.")
                segmented_text["Table of Contents"] = cleaned_text[index:section_index[1]]
                print("Added Table of Contents to the segmented_text.")

                cleaned_text = cleaned_text[section_index[1]:]

                # Create dictionary to hold section indices
                section_indices = {}

                for section in sections:
                    pattern = re.compile(section)
                    index = [text.span() for text in re.finditer(pattern, cleaned_text.lower())]
                    section_indices[section] = index

                # Begin section segmentation
                previous_section_end = None
                segmented_text = {}

                for i, section in enumerate(sections):
                    if i == 0:
                        start = section_indices[section][0][1]
                        end = section_indices[sections[i + 1]][0][1]

                        segmented_text[section] = cleaned_text[start:end]
                        print(f"Added {section} to the segemented_text")
                        previous_section_end = end
                    elif i < (len(sections) - 1) and i > 0:
                        index = section_indices[section]
                        # handling the case when there wasn't an index found
                        if len(index) == 0:
                            continue
                        else:
                            count = 0
                            # handling the case when the next sections index is empty
                            if section_indices[sections[i + 1]]:
                                pass
                            else:
                                count += 1
                                check = True
                                while check:
                                    if section_indices[sections[i + 1 + count]]:
                                        check = False
                                    else:
                                        count += 1
                                    if count == 4:
                                        break

                            start = index[0][0]
                            # adding count to the indexing to account for missing sections
                            end = section_indices[sections[i + 1 + count]][0][0]

                            segmented_text[section] = cleaned_text[start:end]
                            print(f"Added {section} to the segemented_text")
                            previous_section_end = end
                    elif i == (len(sections) - 1):
                        index = section_indices[section]
                        # handling the case where section index is empty
                        if len(index) == 0:
                            start = previous_section_end
                            segmented_text[section] = cleaned_text[start:]
                            print(f"Added {section} to the segemented_text")
                        else:
                            start = index[0][0]
                            segmented_text[section] = cleaned_text[start:]
                            print(f"Added {section} to the segemented_text")
            except:
                unsegmented_count += 1
                print("Document unable to be segmented.")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
                continue

            final_segmented_text.append(segmented_text)
            print("Document Complete")
            print("\n")
            print("------------------------------------------------------------------------------")
            print("\n")

        return final_segmented_text, unsegmented_count

    else:
        final_segmented_text = []
        unsegmented_count = 0
        for i, text in enumerate(docs):
            # Create pattern for common section beginnings
            # Numbers (1., 1.1., etc.), or
            # Letters [(a), (b), etc.), or
            # Mix (E1., E1.1., etc.)
            pattern = re.compile(
                r'\d{1,8}\.(?:\d{1,8}\.)*|\s*(?:\([a-z][)]{1}\s+)|[A-Z]\d{1,8}\.(?:\d{1,8}\.)*|[a-z]\.\s+|[A-Z]+\s+[0-9]\s+|PART [IV]+')

            section_index = [j for j, k in enumerate(text) if re.match(pattern, k)]
            section_text = [text[j] for j in section_index]

            sections = []
            for j in section_text:
                section = re.findall(pattern, j)
                sections.append(section[0])

            segmented_text = {}
            try:
                segmented_text["Preamble"] = " ".join(text[:section_index[0]])
                print("Added Preamble to the segmented_text")

                for j, k in enumerate(section_index):
                    start = k
                    if j < (len(section_index) - 1):
                        end = section_index[j + 1]
                        segmented_text[sections[j]] = " ".join(text[start:end])
                        print(f"Added {sections[j]} to the segemented_text")
                    else:
                        segmented_text[sections[j]] = " ".join(text[start:])
                        print(f"Added {sections[j]} to the segemented_text")

                final_segmented_text.append(segmented_text)
                print("Document Complete")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
            except:
                unsegmented_count += 1
                print("Document unable to be segmented.")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
        return final_segmented_text, unsegmented_count


def flatten(t):
    """
    Function courtesy of Alex Martelli (edited by wjandrea) on the stackoverflow article found here:
    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
    :param lst: Nested list (list of list)
    :return: Flattened list.
    """
    return [item for sublist in t for item in sublist]


if __name__ == "__main__":
    allDocs = pd.read_csv("full_dataframe.csv", index_col=0)

    TOC, noTOC = hasTOC(allDocs)

    segmented_noTOC, unsegmented_count_noTOC = sectionSegmentation(noTOC, TOC=False)
    segmented_TOC, unsegmented_count_TOC = sectionSegmentation(TOC, TOC=True)

    print("\n")
    print("-------------------------------------------------------------")
    print(f"Number of segmented documents: {len(segmented_noTOC)}")
    print(f"Number of unsegmented documents: {unsegmented_count_noTOC}")
    print("-------------------------------------------------------------")
    print("\n")
    print("-------------------------------------------------------------")
    print(f"Number of segmented documents: {len(segmented_TOC)}")
    print(f"Number of unsegmented documents: {unsegmented_count_TOC}")
    print("-------------------------------------------------------------")
