from lxml import etree


class TmxFile(object):
    """A naive and simple implementation of tmx file 1.4 spec"""

    def __init__(self, src_lang, tgt_lang, src, tgt):
        super(TmxFile, self).__init__()
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.src = src
        self.tgt = tgt

    def generate(self):
        namespace_url = "http://www.w3.org/XML/1998/namespace"
        namespace = "{%s}" % namespace_url

        root = etree.Element("tmx", version="1.4")
        tree = etree.ElementTree(root)
        header = etree.SubElement(root, "header")
        header.set("creationtool", "bertalign")
        header.set("segtype", "sentence")
        header.set("o-tmf", "tmx")
        header.set("adminlang", self.src_lang)
        header.set("srclang", self.src_lang)
        header.set("datatype", "plaintext")

        body = etree.SubElement(root, "body")

        # assuming the length is the same for src and tgt
        for i in range(len(self.src)):
            if self.src[i] == "" or self.tgt[i] == "":
                print(
                    "Unaligned "
                    + i
                    + ":\nSource: "
                    + self.src[i]
                    + "\nTarget: "
                    + self.tgt[i]
                    + "\n"
                )

            tu = etree.SubElement(body, "tu")
            tu.set("tuid", str(i + 1))

            src_tuv = etree.SubElement(tu, "tuv")
            src_tuv.set(namespace + "lang", self.src_lang)
            src_seg = etree.SubElement(src_tuv, "seg")
            src_seg.text = self.src[i]

            tgt_tuv = etree.SubElement(tu, "tuv")
            tgt_tuv.set(namespace + "lang", self.tgt_lang)
            tgt_seg = etree.SubElement(tgt_tuv, "seg")
            tgt_seg.text = self.tgt[i]

        self.tree = tree

    def write(self, filename):
        self.generate()

        self.tree.write(
            filename, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )

        print("TMX file written.")
