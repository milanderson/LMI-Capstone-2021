import DocExtract
import re
import string


allDocs = DocExtract.DocExtract()
allDocs.get_text(doc_type='all', test=True)


def hasTOC(dictionary):
    """

    :param dictionary:
    :return:
    """
    TOC = []
    noTOC = []

    string = re.compile("Table of Contents|TABLE OF CONTENTS")

    for i, text in enumerate(dictionary["cleaned_text_list"]):
        noMatch = []
        match = []
        for j, k in enumerate(text):
            # Search for table of contents, append to appropriate list
            search = re.search(string, k)

            if not search:
                noMatch.append(j)
            else:
                match.append(j)
        if match:
            TOC.append((text, dictionary["cleaned_text"][i], match[0]))
        elif noMatch:
            noTOC.append(text)
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
                continue

            # Create list of sections from Table of Contents
            sections = []
            for i, line in enumerate(table_of_contents):
                pattern = re.compile('\s*[\.]+\s+[0-9]+')
                if re.search(pattern, line):
                    sections.append(re.sub(r'\s*[\.]+\s+[0-9]+', '', line).rstrip(string.digits))
                else:
                    if re.search(pattern, table_of_contents[i + 1]):
                        sections.append(line + re.sub(r'\s*[\.]+\s+[0-9]+', '', table_of_contents[i + 1]) \
                                        .rstrip(string.digits))
                        table_of_contents.pop(i + 1)

            # Remove tables or figures from the sections
            table_figure = re.compile("TABLE|Table|table|FIGURE|Figure|figure")
            sections = [section for section in sections if not re.search(table_figure, section)]

            # Used cleaned_text to first separate out preamble and table of contents
            segmented_text = {"Preamble": cleaned_text[:index]}
            print("Added Preamble to the segmented_text.")
            segmented_text["Table of Contents"] = cleaned_text[index:section_index[1]]
            print("Added Table of Contents to the segmented_text.")

            cleaned_text = cleaned_text[section_index[1]:]

            # Create dictionary to hold section indices
            section_indices = {}

            for section in sections:
                pattern = re.compile(section.lower())
                index = [text.span() for text in re.finditer(pattern, cleaned_text.lower())]
                section_indices[section] = index

            # Begin section segmentation
            previous_section_end = None
            segmented_text = {}

            for i, section in enumerate(sections):
                if i == 0:
                    start = section_indices[section][0][1]
                    end = section_indices[sections[i+1]][0][1]

                    segmented_text[section] = cleaned_text[start:end]
                    print(f"Added {section} to the segemented_text")
                    previous_section_end = end
                elif i < (len(sections)-1) and i > 0:
                    index = section_indices[section]
                    # handling the case when there wasn't an index found
                    if len(index) == 0:
                        continue
                    else:
                        count = 0
                        # handling the case when the next sections index is empty
                        if section_indices[sections[i+1]]:
                            pass
                        else:
                            count += 1
                            check = True
                            while check:
                                if section_indices[sections[i+1+count]]:
                                    check = False
                                else:
                                    count += 1
                                if count == 4:
                                    break

                        start = index[0][0]
                        # adding count to the indexing to account for missing sections
                        end = section_indices[sections[i+1+count]][0][0]

                        segmented_text[section] = cleaned_text[start:end]
                        print(f"Added {section} to the segemented_text")
                        previous_section_end = end
                elif i == (len(sections)-1):
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

            final_segmented_text.append(segmented_text)
            print("Document Complete")
            print("\n")
            print("------------------------------------------------------------------------------")
            print("\n")

        return final_segmented_text

    else:
        final_segmented_text = []
        for i, text in enumerate(docs):
            # Create pattern for common section beginnings
            # Numbers (1., 1.1., etc.), or
            # Letters [(a), (b), etc.), or
            # Mix (E1., E1.1., etc.)
            pattern = re.compile(r'\d{1,8}\.(?:\d{1,8}\.)*|\s*(?:\([a-z][)]{1}\s+)|[A-Z]\d{1,8}\.(?:\d{1,8}\.)*|[a-z]\.\s+|[A-Z]+\s+[0-9]\s+|PART [IV]+')

            section_index = [j for j, k in enumerate(text) if re.match(pattern, k)]
            section_text = [text[j] for j in section_index]

            sections = []
            for j in section_text:
                section = re.findall(pattern, j)
                sections.append(section[0])

            segmented_text = {}
            segmented_text["Preamble"] = " ".join(text[:section_index[0]])
            print("Added Preamble to the segmented_text")

            for j, k in enumerate(section_index):
                start = k
                if j < (len(section_index) - 1):
                    end = section_index[j+1]
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

        return final_segmented_text

def flatten(t):
    """
    Function courtesy of Alex Martelli (edited by wjandrea) on the stackoverflow article found here:
    https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
    :param lst: Nested list (list of list)
    :return: Flattened list.
    """
    return [item for sublist in t for item in sublist]

if __name__ == "__main__":
    TOC, noTOC = hasTOC(allDocs.docs_dict)

    segmented_TOC = sectionSegmentation(TOC, TOC=True)
    segmented_noTOC = sectionSegmentation(noTOC, TOC=False)

    print(len(segmented_noTOC))
    print(len(segmented_TOC))
