from docxtpl import DocxTemplate

try:
    doc_input = input('\nEnter the name of the document to be modified, it must be a .docx file (example: document.docx)\n> ')
    doc = DocxTemplate(doc_input)

    tbc_input = input('\nEnter the marked parts to be modified separated by a comma (example: like, this\n> ')
    tbc_input_split = tbc_input.split(', ')

    change = input('\nEnter what they should be modified to, separated by a comma (example: like, this\n> ')
    change_split = change.split(', ')

    final_doc_name = input('\nEnter a name for the document to be created (don\'t add the .docx extension)\n> ')

    dic_blank = {}

    for item in range(len(tbc_input_split)):
        dic_content = {str(tbc_input_split[item]) : str(change_split[item])}
        dic_blank[str(tbc_input_split[item])] = str(change_split[item])

    doc.render(dic_blank)
    doc.save(f'{final_doc_name}.docx')
except:
    print('ouch')