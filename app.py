from flask import Flask, render_template, request, redirect, session, send_file
import mysql.connector
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

app = Flask(__name__)

# ============================================================
# FLASK SECRET KEY
# ============================================================

app.secret_key = "lingosphere_secret_key_2026"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tahreem",
        database="lingosphere"
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            return """
            <script>
                alert("Please fill all fields.");
                window.location.href="/register";
            </script>
            """

        try:
            db = get_db_connection()
            cursor = db.cursor()

            query = """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (name, email, password)
            )

            db.commit()

            cursor.close()
            db.close()

            return redirect("/login")

        except mysql.connector.Error as error:

            return f"""
            <h2>Registration Error</h2>
            <p>{error}</p>
            <a href="/register">Go Back</a>
            """

    return render_template("register.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        try:
            db = get_db_connection()
            cursor = db.cursor()

            query = """
                SELECT id, name, email
                FROM users
                WHERE email = %s AND password = %s
            """

            cursor.execute(
                query,
                (email, password)
            )

            user = cursor.fetchone()

            cursor.close()
            db.close()

            if user:

                session["user_id"] = user[0]
                session["user_name"] = user[1]
                session["user_email"] = user[2]

                return redirect("/dashboard")

            return """
            <script>
                alert("Invalid email or password.");
                window.location.href="/login";
            </script>
            """

        except mysql.connector.Error as error:

            return f"""
            <h2>Login Error</h2>
            <p>{error}</p>
            <a href="/login">Go Back</a>
            """

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name", "Student")
    )


# ============================================================
# COURSE
# ============================================================

@app.route("/course")
def course():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("course.html")


# ============================================================
# LEVEL 1
# ACADEMIC VOCABULARY
# File: vocabulary.html
# ============================================================

@app.route("/alphabet")
def alphabet():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("vocabulary.html")


@app.route("/level1")
def level1():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("vocabulary.html")


# ============================================================
# LEVEL 2
# ADVANCED GRAMMAR
# File: advanced_grammar.html
# ============================================================

@app.route("/vocabulary")
def vocabulary():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("advanced_grammar.html")


@app.route("/level2")
def level2():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("advanced_grammar.html")


# ============================================================
# LEVEL 3
# CRITICAL READING
# File: reading.html
# ============================================================

@app.route("/reading")
def reading():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("reading.html")


@app.route("/level3")
def level3():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("reading.html")


# ============================================================
# LEVEL 4
# PROFESSIONAL SPEAKING
# File: speaking.html
# ============================================================

@app.route("/speaking")
def speaking():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("speaking.html")


@app.route("/level4")
def level4():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("speaking.html")


# ============================================================
# LEVEL 5
# PROFESSIONAL WRITING
# File: professional_writing.html
# ============================================================

@app.route("/writing")
def writing():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("professional_writing.html")


@app.route("/level5")
def level5():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("professional_writing.html")


# ============================================================
# ENROLL
# ============================================================

@app.route("/enroll")
def enroll():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("enroll.html")


# ============================================================
# FINAL QUIZ
# ============================================================

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if "user_id" not in session:
        return redirect("/login")

    # --------------------------------------------------------
    # OPEN QUIZ
    # --------------------------------------------------------

    if request.method == "GET":
        return render_template("quiz.html")

    # --------------------------------------------------------
    # CORRECT ANSWERS
    # --------------------------------------------------------

    correct_answers = {

        "q1": "B",
        "q2": "B",
        "q3": "C",
        "q4": "B",
        "q5": "C",
        "q6": "A",
        "q7": "B",
        "q8": "B",
        "q9": "A",
        "q10": "A"

    }

    # --------------------------------------------------------
    # CALCULATE SCORE
    # --------------------------------------------------------

    score = 0

    for question, correct_answer in correct_answers.items():

        user_answer = request.form.get(question)

        if user_answer == correct_answer:
            score += 1

    total_questions = len(correct_answers)

    percentage = (score / total_questions) * 100

    # --------------------------------------------------------
    # PASSING CRITERIA
    # --------------------------------------------------------

    if percentage >= 60:

        status = "Passed"
        certificate_unlocked = True

    else:

        status = "Not Passed"
        certificate_unlocked = False

    # --------------------------------------------------------
    # SAVE RESULT IN SESSION
    # --------------------------------------------------------

    session["quiz_score"] = score
    session["quiz_total"] = total_questions
    session["quiz_percentage"] = percentage
    session["quiz_status"] = status
    session["certificate_unlocked"] = certificate_unlocked

    # --------------------------------------------------------
    # RESULT PAGE
    # --------------------------------------------------------

    return render_template(
        "quiz_result.html",
        score=score,
        total=total_questions,
        percentage=percentage,
        status=status,
        certificate_unlocked=certificate_unlocked
    )


# ============================================================
# CERTIFICATE PAGE
# ============================================================

@app.route("/certificate")
def certificate():

    if "user_id" not in session:
        return redirect("/login")

    # Certificate only after passing quiz

    if not session.get("certificate_unlocked", False):

        return """
        <script>
            alert("Complete the final quiz with at least 60% to unlock your certificate.");
            window.location.href="/quiz";
        </script>
        """

    return render_template(
        "certificate.html",

        student_name=session.get(
            "user_name",
            "Student"
        ),

        score=session.get(
            "quiz_score",
            0
        ),

        total=session.get(
            "quiz_total",
            10
        ),

        percentage=session.get(
            "quiz_percentage",
            0
        )
    )


# ============================================================
# REAL PDF CERTIFICATE DOWNLOAD
# ============================================================

@app.route("/download_certificate")
def download_certificate():

    if "user_id" not in session:
        return redirect("/login")

    # Only passed students can download certificate

    if not session.get("certificate_unlocked", False):

        return """
        <script>
            alert("Complete the final quiz with at least 60% to download your certificate.");
            window.location.href="/quiz";
        </script>
        """

    student_name = session.get("user_name", "Student")
    score = session.get("quiz_score", 0)
    total = session.get("quiz_total", 10)
    percentage = session.get("quiz_percentage", 0)

    # --------------------------------------------------------
    # CREATE PDF IN MEMORY
    # --------------------------------------------------------

    buffer = BytesIO()

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(
        buffer,
        pagesize=landscape(A4)
    )

    # --------------------------------------------------------
    # COLORS
    # --------------------------------------------------------

    dark_purple = colors.HexColor("#403047")
    purple = colors.HexColor("#705674")
    pink = colors.HexColor("#D18AAA")

    gold = colors.HexColor("#C99943")
    light_gold = colors.HexColor("#F2D58B")
    champagne = colors.HexColor("#FFF3C9")

    soft_bg = colors.HexColor("#FCF7FC")
    grey = colors.HexColor("#766B78")

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    pdf.setFillColor(soft_bg)

    pdf.rect(
        0,
        0,
        page_width,
        page_height,
        fill=1,
        stroke=0
    )

    # --------------------------------------------------------
    # OUTER GOLD BORDER
    # --------------------------------------------------------

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(7)

    pdf.rect(
        18,
        18,
        page_width - 36,
        page_height - 36,
        fill=0,
        stroke=1
    )

    pdf.setStrokeColor(light_gold)
    pdf.setLineWidth(2)

    pdf.rect(
        28,
        28,
        page_width - 56,
        page_height - 56,
        fill=0,
        stroke=1
    )

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(1)

    pdf.rect(
        40,
        40,
        page_width - 80,
        page_height - 80,
        fill=0,
        stroke=1
    )

    # --------------------------------------------------------
    # DECORATIVE GOLDEN CORNERS
    # --------------------------------------------------------

    corner_size = 45
    margin = 48

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(3)

    # Top-left
    pdf.line(margin, page_height - margin,
             margin + corner_size, page_height - margin)
    pdf.line(margin, page_height - margin,
             margin, page_height - margin - corner_size)

    # Top-right
    pdf.line(page_width - margin, page_height - margin,
             page_width - margin - corner_size, page_height - margin)
    pdf.line(page_width - margin, page_height - margin,
             page_width - margin, page_height - margin - corner_size)

    # Bottom-left
    pdf.line(margin, margin,
             margin + corner_size, margin)
    pdf.line(margin, margin,
             margin, margin + corner_size)

    # Bottom-right
    pdf.line(page_width - margin, margin,
             page_width - margin - corner_size, margin)
    pdf.line(page_width - margin, margin,
             page_width - margin, margin + corner_size)

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    pdf.setFillColor(purple)

    pdf.setFont("Helvetica-Bold", 13)

    logo_text = "LINGO SPHERE"

    logo_width = stringWidth(
        logo_text,
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        (page_width - logo_width) / 2,
        page_height - 85,
        logo_text
    )

    # Gold divider

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(2)

    pdf.line(
        page_width / 2 - 70,
        page_height - 102,
        page_width / 2 + 70,
        page_height - 102
    )

    # --------------------------------------------------------
    # CERTIFICATE TITLE
    # --------------------------------------------------------

    pdf.setFillColor(dark_purple)

    pdf.setFont("Times-Bold", 38)

    title = "CERTIFICATE"

    title_width = stringWidth(
        title,
        "Times-Bold",
        38
    )

    pdf.drawString(
        (page_width - title_width) / 2,
        page_height - 145,
        title
    )

    pdf.setFillColor(purple)

    pdf.setFont("Helvetica", 10)

    subtitle = "OF COMPLETION"

    subtitle_width = stringWidth(
        subtitle,
        "Helvetica",
        10
    )

    pdf.drawString(
        (page_width - subtitle_width) / 2,
        page_height - 165,
        subtitle
    )

    # --------------------------------------------------------
    # PRESENTED TO
    # --------------------------------------------------------

    pdf.setFillColor(grey)

    pdf.setFont("Helvetica", 10)

    presented = "This certificate is proudly presented to"

    presented_width = stringWidth(
        presented,
        "Helvetica",
        10
    )

    pdf.drawString(
        (page_width - presented_width) / 2,
        page_height - 205,
        presented
    )

    # --------------------------------------------------------
    # STUDENT NAME
    # --------------------------------------------------------

    pdf.setFillColor(colors.HexColor("#80536F"))

    pdf.setFont("Times-BoldItalic", 30)

    name_width = stringWidth(
        student_name,
        "Times-BoldItalic",
        30
    )

    pdf.drawString(
        (page_width - name_width) / 2,
        page_height - 245,
        student_name
    )

    # Golden line under name

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(1.5)

    pdf.line(
        page_width / 2 - 150,
        page_height - 255,
        page_width / 2 + 150,
        page_height - 255
    )

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    pdf.setFillColor(grey)

    pdf.setFont("Helvetica", 10)

    lines = [
        "has successfully completed the",
        "Advanced English Learning Programme",
        "offered by Lingo Sphere and demonstrated competency in",
        "academic vocabulary, advanced grammar, critical reading,",
        "professional speaking and professional writing."
    ]

    y = page_height - 285

    for index, line in enumerate(lines):

        if index == 1:

            pdf.setFillColor(dark_purple)
            pdf.setFont("Helvetica-Bold", 11)

        else:

            pdf.setFillColor(grey)
            pdf.setFont("Helvetica", 10)

        line_width = stringWidth(
            line,
            pdf._fontname,
            pdf._fontsize
        )

        pdf.drawString(
            (page_width - line_width) / 2,
            y,
            line
        )

        y -= 16

    # --------------------------------------------------------
    # ACHIEVEMENT BOXES
    # --------------------------------------------------------

    box_y = 115
    box_width = 135
    box_height = 48
    gap = 22

    total_boxes_width = (
        box_width * 3
        + gap * 2
    )

    start_x = (
        page_width - total_boxes_width
    ) / 2

    achievement_data = [
        (f"{score}/{total}", "ASSESSMENT SCORE"),
        (f"{percentage:.0f}%", "FINAL PERCENTAGE"),
        ("ADVANCED", "ACHIEVEMENT LEVEL")
    ]

    for index, (value, label) in enumerate(achievement_data):

        x = start_x + index * (box_width + gap)

        pdf.setFillColor(colors.white)
        pdf.setStrokeColor(colors.HexColor("#DFC98F"))
        pdf.setLineWidth(1)

        pdf.roundRect(
            x,
            box_y,
            box_width,
            box_height,
            8,
            fill=1,
            stroke=1
        )

        pdf.setFillColor(purple)

        pdf.setFont("Helvetica-Bold", 14)

        value_width = stringWidth(
            value,
            "Helvetica-Bold",
            14
        )

        pdf.drawString(
            x + (box_width - value_width) / 2,
            box_y + 27,
            value
        )

        pdf.setFillColor(grey)

        pdf.setFont("Helvetica", 6.5)

        label_width = stringWidth(
            label,
            "Helvetica",
            6.5
        )

        pdf.drawString(
            x + (box_width - label_width) / 2,
            box_y + 12,
            label
        )

    # --------------------------------------------------------
    # GOLDEN SEAL
    # --------------------------------------------------------

    seal_x = page_width - 120
    seal_y = 100
    seal_r = 38

    pdf.setFillColor(champagne)
    pdf.setStrokeColor(gold)
    pdf.setLineWidth(4)

    pdf.circle(
        seal_x,
        seal_y,
        seal_r,
        fill=1,
        stroke=1
    )

    pdf.setStrokeColor(colors.HexColor("#93651F"))
    pdf.setLineWidth(1)

    pdf.circle(
        seal_x,
        seal_y,
        seal_r - 7,
        fill=0,
        stroke=1
    )

    pdf.setFillColor(gold)

    pdf.setFont("Helvetica-Bold", 18)

    star = "★"

    star_width = stringWidth(
        star,
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        seal_x - star_width / 2,
        seal_y + 6,
        star
    )

    pdf.setFillColor(colors.HexColor("#5C4017"))

    pdf.setFont("Helvetica-Bold", 6)

    pdf.drawCentredString(
        seal_x,
        seal_y - 10,
        "VERIFIED"
    )

    pdf.drawCentredString(
        seal_x,
        seal_y - 19,
        "ACHIEVEMENT"
    )

    # --------------------------------------------------------
    # SIGNATURE
    # --------------------------------------------------------

    signature_x = 100

    pdf.setFillColor(purple)

    pdf.setFont("Times-Italic", 17)

    pdf.drawString(
        signature_x,
        105,
        "Lingo Sphere"
    )

    pdf.setStrokeColor(colors.HexColor("#8D7B90"))
    pdf.setLineWidth(1)

    pdf.line(
        signature_x,
        96,
        signature_x + 130,
        96
    )

    pdf.setFillColor(dark_purple)

    pdf.setFont("Helvetica-Bold", 8)

    pdf.drawString(
        signature_x,
        82,
        "LINGO SPHERE"
    )

    pdf.setFillColor(grey)

    pdf.setFont("Helvetica", 7)

    pdf.drawString(
        signature_x,
        71,
        "Programme Authority"
    )

    # --------------------------------------------------------
    # CERTIFICATE ID + DATE
    # --------------------------------------------------------

    clean_name = "".join(
        character
        for character in student_name.upper()
        if character.isalnum()
    )

    certificate_id = (
        f"LS-{clean_name}-2026"
    )

    pdf.setFillColor(colors.HexColor("#9A8A9C"))

    pdf.setFont("Helvetica", 6.5)

    pdf.drawCentredString(
        page_width / 2,
        48,
        f"Certificate ID: {certificate_id}"
    )

    pdf.drawCentredString(
        page_width / 2,
        37,
        f"Issued: {datetime.now().strftime('%d %B %Y')}"
    )

    # --------------------------------------------------------
    # FINISH PDF
    # --------------------------------------------------------

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    # --------------------------------------------------------
    # DIRECT DOWNLOAD
    # --------------------------------------------------------

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="Lingo_Sphere_Certificate.pdf"
    )


# ============================================================
# QUIZ RESULT
# ============================================================

@app.route("/quiz-result")
def quiz_result():

    if "user_id" not in session:
        return redirect("/login")

    if "quiz_score" not in session:
        return redirect("/quiz")

    return render_template(
        "quiz_result.html",

        score=session.get(
            "quiz_score",
            0
        ),

        total=session.get(
            "quiz_total",
            10
        ),

        percentage=session.get(
            "quiz_percentage",
            0
        ),

        status=session.get(
            "quiz_status",
            "Not Available"
        ),

        certificate_unlocked=session.get(
            "certificate_unlocked",
            False
        )
    )


# ============================================================
# 404 ERROR
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>Page Not Found | Lingo Sphere</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #faf7fc;
                color: #43304c;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                text-align: center;
            }

            .box {
                background: white;
                padding: 50px;
                border-radius: 25px;
                box-shadow:
                    0 15px 40px
                    rgba(65,45,75,0.10);
            }

            h1 {
                font-size: 70px;
                margin: 0;
                color: #6b5074;
            }

            h2 {
                margin: 10px 0;
            }

            p {
                color: #817583;
            }

            a {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 22px;
                background: #46334f;
                color: white;
                text-decoration: none;
                border-radius: 10px;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>404</h1>

            <h2>Page Not Found</h2>

            <p>
                The requested Lingo Sphere page does not exist.
            </p>

            <a href="/dashboard">
                Back to Dashboard
            </a>

        </div>

    </body>

    </html>
    """, 404


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
