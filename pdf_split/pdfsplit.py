from PyPDF2 import PageObject

import os
import tkinter as tk
from tkinter import ttk
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter import filedialog


def split_and_rearrange_pdf_with_blank(input_pdf_path, output_pdf_path):
    pdf = PdfFileReader(input_pdf_path)
    pdf_writer = PdfFileWriter()

    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num)
        page_width = page.mediaBox.getUpperRight_x()
        page_height = page.mediaBox.getUpperRight_y()

        page_left = PageObject.createBlankPage(width=page_width, height=page_height)
        page_left.mergeTranslatedPage(page, -page_width / 2, 0)
        pdf_writer.addPage(page_left)

        page_right = PageObject.createBlankPage(width=page_width, height=page_height)
        page_right.mergeTranslatedPage(page, -page_width / 2, 0, expand=False)
        pdf_writer.addPage(page_right)

    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

def select_file_and_split():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_pdf_path = os.path.splitext(file_path)[0] + "_split.pdf"
        split_and_rearrange_pdf_with_blank(file_path, output_pdf_path)
        status_label.config(text="분할 완료: " + output_pdf_path)

# GUI 설정
root = tk.Tk()
root.title("PDF 세로분할기 by fdt.")
root.geometry('400x200')  # 윈도우 크기 설정
root.configure(bg='dark gray')  # 배경색 설정

# 스타일 설정
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), borderwidth='4')
style.theme_use("clam")
style.map('TButton', foreground=[('pressed', 'red'), ('active', 'blue')], background=[('pressed', '!disabled', 'black'), ('active', 'white')])

# 버튼 추가
split_button = ttk.Button(root, text="파일 불러오기", command=select_file_and_split, style="TButton")
split_button.pack(pady=20, ipadx=10, ipady=10)

# 상태 메시지 라벨 추가 (배경색과 텍스트 색상 조정)
status_label = tk.Label(root, text="", font=('Helvetica', 12), bg='dark gray', fg='white')
status_label.pack(pady=20)

# GUI 실행
root.mainloop()

# GUI 실행
root.mainloop()