# ==============================================================================
# title           :judgment_text_extraction.py
# description     :Extracts raw text <p> tags in ICLR XML reports.
# author          :Daniel Hoadley
# date            :20190403
# version         :0.1
# usage           :python judgment_text_extraction.py
# notes           :For Blackstone Project
# python_version  :3.6
# ==============================================================================

import os
import bs4 as BeautifulSoup
import tqdm as tqdm


path = "/Users/Daniel/export-searchables/judgments/xml"
os.chdir(path)

for filename in tqdm.tqdm(os.listdir(path)):
    if "xml" in filename:
        f = open(filename)
        content = f.read()
        soup = BeautifulSoup.BeautifulSoup(content, "lxml")
        paras = soup.find_all("p")
        for para in paras:
            para = para.text
            with open(
                "/Users/Daniel/PycharmProjects/ProjectBlackstone/data_extraction/text/paras.txt",
                "a",
            ) as outFile:
                outFile.write(para)
        f.close()
