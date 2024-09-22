import json

def generate_latex(data):
    latex = r"""
\begin{document}

%----------HEADING-----------------
\begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
"""
    if data['name']:
        latex += r"  \textbf{\href{" + data['contact'].get('website', '') + r"}{\Large " + data['name'] + r"}}"
    
    contact_info = []
    if data['contact'].get('email'):
        contact_info.append(r"Email : \href{mailto:" + data['contact']['email'] + r"}{" + data['contact']['email'] + r"}")
    if data['contact'].get('mobile'):
        contact_info.append(r"Mobile : " + data['contact']['mobile'])
    
    latex += " & " + r" \\ ".join(contact_info) + r" \\"

    if data['contact'].get('website'):
        latex += r"\n  \href{" + data['contact']['website'] + r"}{" + data['contact']['website'] + r"}"

    latex += r"""
\end{tabular*}

%-----------EDUCATION-----------------
\section{Education}
  \resumeSubHeadingListStart
"""

    if data['education']:
        for edu in data['education']:
            latex += r"    \resumeSubheading"
            if edu.get('institution'):
                latex += r"{" + edu['institution'] + r"}"
            if edu.get('location'):
                latex += r"{" + edu['location'] + r"}"
            latex += "\n      "
            if edu.get('degree'):
                latex += r"{" + edu['degree']
                if edu.get('gpa'):
                    latex += r";  GPA: " + edu['gpa']
                latex += r"}"
            if edu.get('duration'):
                latex += r"{" + edu['duration'] + r"}"
            latex += "\n"

        latex += r"""  \resumeSubHeadingListEnd


%-----------EXPERIENCE-----------------
\section{Experience}
  \resumeSubHeadingListStart

"""

    if data['experience']:
        for exp in data['experience']:
            latex += f"""    \\resumeSubheading
      {{{exp['company']}}}{{{exp['location']}}}
      {{{exp['position']}}}{{{exp['duration']}}}
      \\resumeItemListStart
"""
            for project in exp['projects']:
                latex += f"        \\resumeItem{{{project['title']}}}\n"
                latex += f"          {{{project['description']}}}\n"
            latex += r"      \resumeItemListEnd" + "\n\n"

        latex += r"""  \resumeSubHeadingListEnd


%-----------PROJECTS-----------------
\section{Projects}
  \resumeSubHeadingListStart
"""

    if data['projects']:
        for project in data['projects']:
            latex += f"    \\resumeSubItem{{{project['title']}}}\n"
            latex += f"      {{{project['description']}}}\n"

        latex += r"""  \resumeSubHeadingListEnd

%-----------ACADEMIC EXPERIENCE-----------------
\section{Academic Experience}
  \resumeSubHeadingListStart
"""

    if data['academic_experience']:
        for academic_exp in data['academic_experience']:
            latex += f"    \\resumeSubItem{{{academic_exp['title']}}}\n"
            latex += f"      {{{academic_exp['description']}}}\n"

        latex += r"""  \resumeSubHeadingListEnd

%
%--------PROGRAMMING SKILLS------------
\section{Programming Skills}
 \resumeSubHeadingListStart
   \item{
"""
    if data['skills'].get('languages') or data['skills'].get('technologies'):
        if data['skills'].get('languages'):
            latex += r"     \textbf{Languages}{: " + ", ".join(data['skills']['languages']) + r"}"
        if data['skills'].get('technologies'):
            latex += r"" + "\n" + r"     \hfill" + "\n" + r"     \textbf{Technologies}{: " + ", ".join(data['skills']['technologies']) + r"}"
        latex += r"""
   }
 \resumeSubHeadingListEnd

%-------------------------------------------
\end{document}
"""
    return latex

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def json_to_latex(json_path: str, output_path: str, header_path: str = "header_eng.tex"):
    # 读取 header.tex 文件
    header_content = read_file(header_path)

    # 从文件读取JSON数据
    json_data = json.loads(read_file(json_path))

    # 生成LaTeX代码
    latex_output = generate_latex(json_data)

    # 将header.tex的内容和生成的LaTeX代码合并
    full_latex = header_content + "\n" + latex_output

    # 将完整的LaTeX代码写入文件
    write_file(output_path, full_latex)

    print(f"LaTeX file has been generated as '{output_path}'")


if __name__ == "__main__":
    json_to_latex("../input/original.json", "../output/output.tex")