from fpdf import FPDF


def main():
    name = input("Name: ")

    shirt = FPDF(orientation = "P", format = "A4")
    shirt.add_page()
    shirt.set_font("Arial", "B", 40)
    shirt.cell(0,40, "CS50 Shirtificate", new_x="LMARGIN", new_y="NEXT", align="C")

    shirt.image("shirtificate.png", x=5, y=50, w=200)
    shirt.set_font("Arial", "B", 24)
    shirt.set_text_color(255,255,255)
    shirt.cell(0,100,f"{name} took CS50",new_x="LMARGIN", new_y="NEXT", align="C")

    shirt.output("shirtificate.pdf")


main()
