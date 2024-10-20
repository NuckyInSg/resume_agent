import json

def generate_heading(data):
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
"""
    return latex

def generate_education(education_data):
    latex = r"""
%-----------EDUCATION-----------------
\section{Education}
  \resumeSubHeadingListStart
"""
    for edu in education_data:
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

    latex += r"  \resumeSubHeadingListEnd"
    return latex

def generate_experience(experience_data):
    latex = r"""
%-----------EXPERIENCE-----------------
\section{Experience}
  \resumeSubHeadingListStart
"""
    for exp in experience_data:
        latex += f"""    \\resumeSubheading
      {{{exp['company']}}}{{{exp['location']}}}
      {{{exp['position']}}}{{{exp['duration']}}}
      \\resumeItemListStart
"""
        for project in exp['projects']:
            latex += f"        \\resumeItem{{{project['title']}}}\n"
            latex += f"          {{{project['description']}}}\n"
        latex += r"      \resumeItemListEnd" + "\n\n"

    latex += r"  \resumeSubHeadingListEnd"
    return latex

def generate_projects(projects_data):
    if not projects_data:
        return ""
    
    latex = r"""
%-----------PROJECTS-----------------
\section{Projects}
  \resumeSubHeadingListStart
"""
    for project in projects_data:
        latex += f"    \\resumeSubItem{{{project['title']}}}\n"
        latex += f"      {{{project['description']}}}\n"

    latex += r"  \resumeSubHeadingListEnd"
    return latex

def generate_professional_summary(summary_data):
    if not summary_data:
        return ""
    
    latex = r"""
%-----------PROFESSIONAL SUMMARY-----------------
\section{Professional Summary}
"""
    latex += summary_data + "\n"
    return latex

def generate_awards(awards_data):
    if not awards_data:
        return ""
    
    latex = r"""
%-----------AWARDS-----------------
\section{Awards \& Achievements}
  \resumeSubHeadingListStart
"""
    for award in awards_data:
        latex += f"    \\resumeSubItem{{{award['title']}}}\n"
        if award.get('description'):
            latex += f"      {{{award['description']}}}\n"
    
    latex += r"  \resumeSubHeadingListEnd"
    return latex

def generate_academic_experience(academic_exp_data):
    if not academic_exp_data:
        return ""
    
    latex = r"""
%-----------ACADEMIC EXPERIENCE-----------------
\section{Academic Experience}
  \resumeSubHeadingListStart
"""
    for exp in academic_exp_data:
        latex += f"""    \\resumeSubheading
      {{{exp['institution']}}}{{{exp['location']}}}
      {{{exp['position']}}}{{{exp['duration']}}}
      \\resumeItemListStart
"""
        for item in exp['responsibilities']:
            latex += f"        \\resumeItem{{{item}}}\n"
        latex += r"      \resumeItemListEnd" + "\n\n"

    latex += r"  \resumeSubHeadingListEnd"
    return latex

def generate_skills(skills_data):
    if not skills_data:
        return ""
    
    skills = skills_data
    num_languages = len(skills.get('languages', []))
    num_technologies = len(skills.get('technologies', []))
    
    latex = ""
    if skills and (num_languages > 0 or num_technologies > 0):
        latex += r"""
%---------PROGRAMMING SKILLS------------
\section{Programming Skills}
 \resumeSubHeadingListStart
   \item{
"""
        if skills.get('languages'):
            latex += r"     \textbf{Languages}{: " + ", ".join(skills['languages']) + r"}"
        if skills.get('technologies'):
            latex += r"" + "\n" + r"     \hfill" + "\n" + r"     \textbf{Technologies}{: " + ", ".join(skills['technologies']) + r"}"
        latex += r"""
   }
 \resumeSubHeadingListEnd
"""
    return latex

def generate_latex(data):
    latex = generate_heading(data)

    if data.get('education'):
        latex += generate_education(data['education'])
    
    if data.get('experience'):
        latex += generate_experience(data['experience'])
    
    if data.get('academic_experience'):
        latex += generate_academic_experience(data['academic_experience'])
    
    if data.get('projects'):
        latex += generate_projects(data['projects'])
    
    if data.get('awards'):
        latex += generate_awards(data['awards'])
    
    if data.get('skills'):
        latex += generate_skills(data['skills'])

    if data.get('professional_summary'):
        latex += generate_professional_summary(data['professional_summary'])
    
    latex += r"""
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
