from pathlib import Path

from fpdf import FPDF


def pdf_create(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(family="Arial", size=25)

    pdf.cell(w=200, h=20, txt=f"{data['full_name']}'s Resume", ln=1, align='C')

    pdf.set_font(family="Arial", size=15)
    pdf.cell(w=20, h=10, txt=f"Programming Languages: {data['p_languages']}", ln=1, align='L')
    pdf.cell(w=20, h=10, txt=f"Databases: {data['db']}", ln=1, align='L')
    pdf.cell(w=20, h=10, txt=f"Experience Year: {data['ex_year']}", ln=1, align='L')
    pdf.cell(w=20, h=10, txt=f"Languages: {data['languages']}", ln=1, align='L')
    pdf.cell(w=20, h=10, txt=f"Education Degree: {data['education_d']}", ln=1, align='L')
    pdf.cell(w=20, h=10, txt=f"Bio: {data['bio']}", ln=1, align='L')
    pdf.cell(w=20, h=15, txt=f"Contact: {data['phone_number']}", ln=1, align='L')

    root_dir = Path(__file__).parent.parent / "media/temp"
    pdf.output(f"{root_dir / str(data['telegram_id'])}_new.pdf")


if __name__ == '__main__':
    pdf_create({
        "p_languages": "Python, C++, GO",
        "db": "PostgreSql, MySql, Redis",
        "ex_year": "1year",
        "languages": "English little, Uzbek native",
        "education_d": "Bachelor",
        "bio": "About me",
        "full_name": "Solijonov Otabek",
        "phone_number": "998911144735",
        "telegram_id": 621383789
    })
