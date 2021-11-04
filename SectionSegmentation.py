import re
import string
import pandas as pd

def doExtract():
    # spacy is an expensive import, don't add it unless you really need to
    from DocExtract import DocExtract
    allDocs = DocExtract()
    return allDocs.get_text(doc_type='all', test=True)

def parseTOCSection(tocLine):
    tocLine = re.sub(r'[\.]{3,}.*[0-9]+', '', tocLine.lower()).strip()
    return tocLine.split(':')[-1].strip()

def hasTOC(df):
    """

    :param dictionary:
    :return:
    """

    TOC = []
    noTOC = []

    pattern = re.compile("table of contents", flags=re.IGNORECASE)

    for i, text in enumerate(df["cleaned_text"]):
        # text = json.loads(text)
        # Change text from str type to list type
        text = text.lstrip("[")
        text = text.rstrip("]")
        text = text.split("\r\n")

        noMatch = []
        match = []
        new_text = []
        for j, line in enumerate(text):
            # Search for table of contents, append to appropriate list
            line = line.lstrip("'")
            line = line.replace(" '", "", 1)
            new_text.append(line)

            # Search for table of contents, append to appropriate list
            if not re.search(pattern, line):
                noMatch.append(j)
            else:
                match.append(j)
        if match:
            TOC.append((new_text, df["cleaned_text"][i], match[0], df["file_name"][i]))
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
        for text, cleaned_text, tocStartIndex, fname in docs:
            cleaned_text = cleaned_text.split('\r\n')

            # Pull the first section index to know when the Table of contents ends
            # Cleans any extra periods or numbers after the text
            first_section = ""
            searchIndex = tocStartIndex + 1
            while searchIndex < len(cleaned_text):
                if "..." in cleaned_text[searchIndex]:
                    first_section = parseTOCSection(cleaned_text[searchIndex])
                    break
                searchIndex += 1

            # Collect following lines
            fudge_factor = 15
            time_since_toc_line = 0
            table_of_contents = []
            for lineIdx in range(searchIndex, len(cleaned_text)):
                line = cleaned_text[lineIdx]
                if time_since_toc_line > fudge_factor:
                    break
                time_since_toc_line += 1

                if "..." in line:
                    table_of_contents.append(parseTOCSection(line))
                    time_since_toc_line = 0

            
            if len(table_of_contents) < 5:
                print("First section could not be found - Table of Contents could not be separated.")
                print("Document unable to be segmented.")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
                unsegmented_count += 1
                continue

            def collectSection(prevPat, curPat, text):
                stIdx, edIdx = None, None
                for lineIdx, line in enumerate(text):
                    if stIdx == None and prevPat and prevPat in line:
                        stIdx = lineIdx
                    if edIdx == None and curPat and curPat in line:
                        edIdx = lineIdx
                    if stIdx != None and edIdx != None:
                        break
                return text[stIdx:edIdx], text[edIdx:]

            segmented_text = {"Table of Contents": table_of_contents}
            text_no_toc = cleaned_text[:tocStartIndex] + cleaned_text[lineIdx - fudge_factor:]
            sections = []
            for i in range(len(table_of_contents)):
                nextTitle = table_of_contents[i + 1] if i + 1 < len(table_of_contents) else None
                newSection, text_no_toc = collectSection(table_of_contents[i], nextTitle, text_no_toc)
                if newSection:
                    segmented_text[table_of_contents[i]] = newSection
                else:
                    print('section not found: ' + table_of_contents[i])

            # Remove tables or figures from the sections
            table_figure = re.compile("table|figure", flags=re.IGNORECASE)
            sections = [section.lower() for section in sections if not re.search(table_figure, section)]

            if len(segmented_text) > len(table_of_contents) * 0.7:
                final_segmented_text.append(segmented_text)
                print("Document Complete")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
            else:
                unsegmented_count += 1
                print("3. Document unable to be segmented.")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
                continue

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

                for j, k in enumerate(section_index):
                    start = k
                    if j < (len(section_index) - 1):
                        end = section_index[j + 1]
                        segmented_text[sections[j]] = " ".join(text[start:end])
                    else:
                        segmented_text[sections[j]] = " ".join(text[start:])

                final_segmented_text.append(segmented_text)
                print("Document Complete")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
            except:
                unsegmented_count += 1
                print("4. Document unable to be segmented.")
                print("\n")
                print("------------------------------------------------------------------------------")
                print("\n")
                continue
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

    print(f"Total number of documents: {len(allDocs)}")
    print(f"Total TOC documents: {len(TOC)}")
    print(f"Total noTOC documents: {len(noTOC)}")

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
