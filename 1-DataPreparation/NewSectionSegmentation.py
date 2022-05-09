import pandas as pd
import re
import string


class SectionSegmentation:

    def __init__(self):
        self.unsegmented_docs = 0
        self.docs = 0
        self.doc_names = 0
        self.segmented_docs = 0

    def documents(self, df):

        docs = []
        docs_name = []

        for i, text in enumerate(df["cleaned_text_list"]):
            # text = json.loads(text)
            # Change text from str type to list type
            text = text.lstrip("[")
            text = text.rstrip("]")
            text = text.split("',")

            new_text = []
            for j, k in enumerate(text):
                # Search for table of contents, append to appropriate list
                k = k.lstrip("'")
                k = k.replace(" '", "", 1)
                new_text.append(k)

            if new_text:
                docs.append(new_text)
                docs_name.append(df["file_name"][i])
            else:
                print("Empty text")

        self.docs = docs
        self.doc_names = docs_name

    def sectionSegmentation(self):
        final_segmented_text = {}
        for i, text in enumerate(self.docs):
            # Create pattern for common section beginnings
            # Numbers (1., 1.1., etc.), or
            # Letters [(a), (b), etc.), or
            # Mix (E1., E1.1., etc.)
            pattern = re.compile(
                r'''\d{1,2}\.(?:\d{1,2}\.)*\s+|[A-Z]+\s+[0-9]\s+|\s*GLOSSARY|\s*REFERENCES|\s*TABLE OF CONTENTS|
                    \s*Table of Contents|\s*SECTION\s[0-9]+|\s*PART [IV]+''')

            section_index = [j for j, k in enumerate(text) if re.match(pattern, k)]
            section_text = [text[j] for j in section_index]

            sections_dict = {}
            sections_list = []
            for k, j in enumerate(section_text):
                section = re.findall(pattern, j)
                sections_dict[section[0]] = section_index[k]
                sections_list.append(section[0])

            segmented_text = {}
            try:
                if "table of contents" in list(sections_dict.keys()):
                    segmented_text["Preamble"] = " ".join(text[:sections_dict["Table of Contents"]])
                    start_index = sections_dict["Table of Contents"]
                elif "TABLE OF CONTENTS" in list(sections_dict.keys()):
                   segmented_text["Preamble"] = " ".join(text[:sections_dict["TABLE OF CONTENTS"]])
                   start_index = sections_dict["TABLE OF CONTENTS"]
                else:
                    segmented_text["Preamble"] = " ".join(text[:section_index[0]])
                    start_index = section_index[0]

                for j, k in enumerate(section_index):
                    if k < start_index:
                        continue
                    elif k >= start_index:
                        start = k
                    if j < (len(section_index) - 1):
                        end = section_index[j + 1]
                        segmented_text[sections_list[j]] = " ".join(text[start:end])
                    else:
                        segmented_text[sections_list[j]] = " ".join(text[start:])

                segmentation_keys = list(map(lambda x: x.lower(), segmented_text.keys()))
                glossary_subsection_pattern = "part i"

                if glossary_subsection_pattern in segmentation_keys:
                    glossary = [x for x in segmented_text.keys() if re.findall("glossary", x, flags=re.IGNORECASE)]
                    print(glossary)
                    glossary_subsections = [x for x in segmented_text.keys() if re.findall(glossary_subsection_pattern, x, flags=re.IGNORECASE)]
                    print(glossary_subsections)

                    if glossary and len(glossary_subsections) == 2:
                        segmented_text[glossary[-1]] = segmented_text[glossary_subsections[0]] + segmented_text[glossary_subsections[1]]
                        del segmented_text[glossary_subsections[0]]
                        del segmented_text[glossary_subsections[1]]
                    elif len(glossary_subsections) == 2:
                        segmented_text["Glossary"] = segmented_text[glossary_subsections[0]] + segmented_text[glossary_subsections[0]]
                        del segmented_text[glossary_subsections[0]]
                        del segmented_text[glossary_subsections[1]]

                final_segmented_text[self.doc_names[i]] = segmented_text
            except:
                self.unsegmented_docs += 1
                continue

        self.segmented_docs = final_segmented_text


# if __name__ == "__main__":
#     allDocs = pd.read_csv("full_dataframe.csv")
#
#     segmented = SectionSegmentation()
#     segmented.documents(allDocs)
#     segmented.sectionSegmentation()
#
#     print(segmented.unsegmented_docs)
