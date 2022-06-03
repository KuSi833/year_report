from year_report.grade_report import Module, Activity, Year, Verbosity

# Uncertainties
algos_exam_grade = 50
plp_exam_grade = 60
seng1_total = 50
seng2_exam_grade = 50
kbai_exam_grade = 50
ml_exam_grade = 50
visual_exam_grade = 50

# full year
algos = Module("Algorithms and Data Structures", credits=20)
algos.add_activities(
    Activity("Courseworks", 50, 50),
    Activity("Exam 1", 15, 40),
    Activity("Exam 2", 35, algos_exam_grade, certain=False),
)

plp = Module("Programming Language Paradigms", credits=20)
plp.add_activities(
    Activity("Courseworks", 20, 80),
    Activity("Exam", 80, plp_exam_grade, certain=False),
)

# semester 1
logic_and_modeling = Module("Logic and Modeling", 60)
databases = Module("Database Systems", 60)
intro_to_ai = Module("Introduction to AI", 70)
seng1 = Module("Software Engieering 1", seng1_total, certain=False)

# semester 2
seng2 = Module("Software Engieering 2")
seng2.add_activities(
    Activity("Team Coursework", 70, 50),
    Activity("Exam", 30, seng2_exam_grade, certain=False),
)
kbai = Module("Knowledge Based AI")
kbai.add_activities(
    Activity("Courseworks", 70, 100),
    Activity("Exam", 30, kbai_exam_grade, certain=False),
)
ml = Module("Machine Learning")
ml.add_activities(
    Activity("Courseworks", 70, 80),
    Activity("exam", 30, ml_exam_grade, certain=False),
)
visual = Module("Introduction to Visual Computing")
visual.add_activities(
    Activity("Courseworks", 30, 90),
    Activity("Exam", 70, visual_exam_grade, certain=False),
)

year2 = Year(2)
year2.add_modules(
    logic_and_modeling,
    databases,
    intro_to_ai,
    seng1,
    algos,
    plp,
    seng2,
    kbai,
    ml,
    visual,
)

year2.report(Verbosity.PER_ACTIVITY)
# year2.report(Verbosity.PER_MODULE)
# year2.report(Verbosity.OVERALL)
