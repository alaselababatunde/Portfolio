score = int(input("Score: "))

if score >= 95 and score <= 100:
    print("Grade: A+")
elif score >= 90 and score < 95:
    print("Grade: A-")
elif score >= 85 and score < 90:
    print("Grade: B+")
elif score >= 80 and score < 85:
    print("Grade: B-")
elif score >= 75 and score < 80:
    print("Grade: C+")
elif score >= 70 and score < 75:
    print("Grade: C-")
elif score >= 65 and score < 70:
    print("Grade: D+")
elif score >= 60 and score < 65:
    print("Grade: D-")
elif score >= 55 and score < 60:
    print("Grade: E+")
elif score >= 50 and score < 55:
    print("Grade: E-")
else:
    print("Grade: F")